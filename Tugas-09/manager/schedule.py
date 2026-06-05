from manager.storage import connect_db
from manager.output import print_schedules


def add_schedule():
    tanggal = input('Masukkan tanggal: ')
    waktu = input('Masukkan waktu: ')
    kegiatan = input('Masukkan kegiatan: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        '''
        INSERT INTO schedules
        (tanggal, waktu, kegiatan)
        VALUES (?, ?, ?)
        ''',
        (tanggal, waktu, kegiatan)
    )

    connection.commit()
    connection.close()

    print('Jadwal berhasil ditambahkan!')


def show_schedule():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM schedules')
    schedules = cursor.fetchall()

    connection.close()

    print_schedules(schedules)


def edit_schedule():
    show_schedule()

    id_jadwal = input('Masukkan ID jadwal yang ingin diedit: ')

    tanggal = input('Tanggal baru: ')
    waktu = input('Waktu baru: ')
    kegiatan = input('Kegiatan baru: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        '''
        UPDATE schedules
        SET tanggal=?, waktu=?, kegiatan=?
        WHERE id=?
        ''',
        (tanggal, waktu, kegiatan, id_jadwal)
    )

    connection.commit()
    connection.close()

    print('Jadwal berhasil diperbarui!')

def toggle_selesai():
    show_schedule()

    id_jadwal = input('Masukkan ID yang ingin ditandai selesai: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT selesai FROM schedules WHERE id=?', (id_jadwal,))
    data = cursor.fetchone()

    if data is None:
        print("Jadwal tidak ditemukan!")
        return

    current = data[0] if data[0] is not None else 0
    new_status = 0 if current == 1 else 1

    cursor.execute(
        'UPDATE schedules SET selesai=? WHERE id=?',
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

    cursor.execute(
        'DELETE FROM schedules WHERE id=?',
        (id_jadwal,)
    )

    connection.commit()
    connection.close()

    print('Jadwal berhasil dihapus!')

