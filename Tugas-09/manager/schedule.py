from datetime import datetime

from manager.storage import connect_db
from manager.output import print_schedules


_NAMA_BULAN = {
    'januari': 1, 'februari': 2, 'maret': 3, 'april': 4,
    'mei': 5, 'juni': 6, 'juli': 7, 'agustus': 8,
    'september': 9, 'oktober': 10, 'november': 11, 'desember': 12,
}


def _parse_tanggal(tanggal):
    """
    Mencoba mem-parsing tanggal dari berbagai format yang mungkin diinput user:
    - "2 Juli 2026" (nama bulan Indonesia)
    - "02-07-2026", "02/07/2026", "2026-07-02", dsb.
    Mengembalikan objek date, atau None kalau tidak berhasil dikenali.
    """
    teks = tanggal.strip().lower()

    # Coba format nama bulan Indonesia: "2 juli 2026"
    bagian = teks.split()
    if len(bagian) == 3 and bagian[1] in _NAMA_BULAN:
        try:
            hari = int(bagian[0])
            bulan = _NAMA_BULAN[bagian[1]]
            tahun = int(bagian[2])
            return datetime(tahun, bulan, hari).date()
        except ValueError:
            pass

    # Coba beberapa format numerik umum
    for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.strptime(tanggal.strip(), fmt).date()
        except ValueError:
            continue

    return None


def _parse_waktu(waktu):
    """Mencoba mem-parsing jam dari format 'HH:MM', 'HH.MM', atau 'HH:MM:SS'."""
    for fmt in ('%H:%M', '%H.%M', '%H:%M:%S'):
        try:
            return datetime.strptime(waktu.strip(), fmt).time()
        except ValueError:
            continue
    return None


def _parse_tanggal_waktu(tanggal, waktu):
    """
    Menggabungkan tanggal + waktu jadi satu objek datetime,
    supaya perbandingan dengan waktu sekarang akurat (bukan cuma bandingin jam,
    karena jadwalnya bisa untuk hari lain / masa depan).
    Mengembalikan None kalau salah satu (tanggal/waktu) gagal dikenali.
    """
    tgl = _parse_tanggal(tanggal)
    jam = _parse_waktu(waktu)

    if tgl is None or jam is None:
        return None

    return datetime.combine(tgl, jam)


def add_schedule(id_user):
    tanggal = input('Masukkan tanggal: ')
    waktu = input('Masukkan waktu: ')
    kegiatan = input('Masukkan kegiatan: ')
    deskripsi = input('Masukkan deskripsi (boleh dikosongkan): ')

    # TAMBAHAN: pengecekan jadwal, berlaku untuk KEGIATAN APAPUN,
    # TANGGAL APAPUN, dan JAM BERAPAPUN sesuai input user.
    # Tanggal & jam digabung dulu supaya perbandingannya akurat
    waktu_jadwal = _parse_tanggal_waktu(tanggal, waktu)

    if waktu_jadwal is None:
        print(f'(Format tanggal/waktu "{tanggal} {waktu}" tidak dikenali, pengecekan jadwal dilewati)')
    else:
        waktu_sekarang = datetime.now()
        print(f'jadwal "{kegiatan}" pada {waktu_jadwal.strftime("%d-%m-%Y")} jam {waktu_jadwal.strftime("%H.%M")}')
        print(f'sekarang sudah menunjukkan {waktu_sekarang.strftime("%d-%m-%Y %H:%M:%S")}')

        if waktu_sekarang < waktu_jadwal:
            print("wah masih ada waktu nih, nanti kalo sudah waktunya aku ingatkan ya!")
        elif waktu_sekarang.replace(second=0, microsecond=0) == waktu_jadwal.replace(second=0, microsecond=0):
            print(f'yah, sayang sekali waktu sudah menunjukkan jam {waktu_jadwal.strftime("%H.%M")}:(')
        else:
            print("yah, waktunya sudah lewat, silahkan isi waktu yang masih berjalan ya!")

    connection = connect_db()
    cursor = connection.cursor()

    # id_user TIDAK diminta dengan input() -- sudah didapat otomatis dari main.py
    # status TIDAK diminta dengan input() -- otomatis 0 (belum selesai) saat jadwal baru dibuat
    cursor.execute(
        '''
        INSERT INTO schedules
        (id_user, tanggal, waktu, kegiatan, deskripsi, status)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (id_user, tanggal, waktu, kegiatan, deskripsi, 0)
    )

    id_schedule = cursor.lastrowid

    # TAMBAHAN: setiap jadwal baru otomatis punya 1 baris CHECKLIST
    cursor.execute(
        'INSERT INTO checklist (id_schedule, check_status, check_date) VALUES (?, ?, ?)',
        (id_schedule, 0, None)
    )

    connection.commit()
    connection.close()

    print('Jadwal berhasil ditambahkan!')

    # Menambahkan pengingat (REMINDER) untuk jadwal ini
    mau_pengingat = input('Tambahkan pengingat untuk jadwal ini? (y/n): ')
    if mau_pengingat.lower() == 'y':
        reminder_time = input('Masukkan waktu pengingat: ')

        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            'INSERT INTO reminders (id_schedule, reminder_time, reminder_status) VALUES (?, ?, ?)',
            (id_schedule, reminder_time, 'pending')
        )

        connection.commit()
        connection.close()

        print('Pengingat berhasil ditambahkan!')


def show_schedule():
    connection = connect_db()
    cursor = connection.cursor()

    # JOIN ke tabel checklist supaya status checklist ikut tampil
    cursor.execute('''
        SELECT s.id, s.tanggal, s.waktu, s.kegiatan, s.deskripsi,
               s.status, c.check_status, c.check_date
        FROM schedules s
        LEFT JOIN checklist c ON s.id = c.id_schedule
        ORDER BY s.tanggal, s.waktu
    ''')
    schedules = cursor.fetchall()

    connection.close()

    print_schedules(schedules)


def edit_schedule():
    show_schedule()

    id_jadwal = input('Masukkan ID jadwal yang ingin diedit: ')

    tanggal = input('Tanggal baru: ')
    waktu = input('Waktu baru: ')
    kegiatan = input('Kegiatan baru: ')
    deskripsi = input('Deskripsi baru: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        '''
        UPDATE schedules
        SET tanggal=?, waktu=?, kegiatan=?, deskripsi=?
        WHERE id=?
        ''',
        (tanggal, waktu, kegiatan, deskripsi, id_jadwal)
    )

    connection.commit()
    connection.close()

    print('Jadwal berhasil diperbarui!')


def toggle_selesai():
    show_schedule()

    id_jadwal = input('Masukkan ID yang ingin ditandai selesai: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT check_status FROM checklist WHERE id_schedule=?', (id_jadwal,))
    data = cursor.fetchone()

    if data is None:
        print("Checklist untuk jadwal ini tidak ditemukan!")
        connection.close()
        return

    current = data[0] if data[0] is not None else 0
    new_status = 0 if current == 1 else 1

    # check_date diisi otomatis pakai datetime.now()
    # tanpa meminta input() dari user
    check_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S') if new_status == 1 else None

    cursor.execute(
        'UPDATE checklist SET check_status=?, check_date=? WHERE id_schedule=?',
        (new_status, check_date, id_jadwal)
    )

    # status di tabel schedules ikut disamakan dengan checklist
    cursor.execute(
        'UPDATE schedules SET status=? WHERE id=?',
        (new_status, id_jadwal)
    )

    connection.commit()
    connection.close()

    print("Status jadwal berhasil diupdate!")


def delete_schedule():
    show_schedule()

    id_jadwal = input('Masukkan ID jadwal yang ingin dihapus: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM checklist WHERE id_schedule=?', (id_jadwal,))
    cursor.execute('DELETE FROM reminders WHERE id_schedule=?', (id_jadwal,))
    cursor.execute('DELETE FROM schedules WHERE id=?', (id_jadwal,))

    connection.commit()
    connection.close()

    print('Jadwal berhasil dihapus!')