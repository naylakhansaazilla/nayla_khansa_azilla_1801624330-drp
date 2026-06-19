from datetime import datetime

from manager.storage import connect_db
from manager.output import print_schedules


def add_schedule(id_user):
    tanggal = input('Masukkan tanggal: ')
    waktu = input('Masukkan waktu: ')
    kegiatan = input('Masukkan kegiatan: ')
    deskripsi = input('Masukkan deskripsi (boleh dikosongkan): ')

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