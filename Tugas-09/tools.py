import sqlite3
from manager.search import search_schedule
from manager.output import print_schedules

DB_NAME = 'cheki_cheki.db'


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            waktu TEXT,
            kegiatan TEXT,
            selesai INTEGER
        )
    ''')

    connection.commit()
    connection.close()


def display_menu():
    print('================================')
    print('Selamat datang di Cheki-Cheki')
    print('1. Tambah Jadwal')
    print('2. Lihat Daftar Jadwal')
    print('3. Checklist Jadwal')
    print('4. Cek Pengingat')
    print('5. Edit Jadwal')
    print('6. Hapus Jadwal')
    print('7. Selesai')
    print('================================')


def select_menu(menu):
    if menu == '1':
        add_schedule()

    elif menu == '2':
        show_schedules()

    elif menu == '3':
        checklist_schedule()

    elif menu == '4':
        check_reminder()

    elif menu == '5':
        edit_schedule()

    elif menu == '6':
        delete_schedule()

    elif menu == '7':
        print('Keluar dari program Cheki-Cheki')
        return True

    else:
        print('Menu tidak ada')

    return False


def add_schedule():
    print('Anda mengakses menu "Tambah Jadwal"')

    tanggal = input('Masukkan tanggal kegiatan: ')
    waktu = input('Masukkan waktu kegiatan: ')
    kegiatan = input('Masukkan nama kegiatan: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO schedules (tanggal, waktu, kegiatan, selesai)
        VALUES (?, ?, ?, ?)
    ''', (tanggal, waktu, kegiatan, 0))

    connection.commit()
    connection.close()

    print('Jadwal berhasil ditambahkan.')


def show_schedules():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM schedules')
    schedules = cursor.fetchall()

    connection.close()

    print_schedules(schedules)


def checklist_schedule():
    show_schedules()

    nomor = input('Masukkan ID jadwal yang sudah selesai: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE schedules
        SET selesai = ?
        WHERE id = ?
    ''', (1, nomor))

    connection.commit()
    connection.close()

    print('Jadwal berhasil ditandai selesai.')


def check_reminder():
    waktu = input('Masukkan waktu yang ingin dicek, contoh 07.00: ')

    schedules = search_schedule(waktu)

    if len(schedules) == 0:
        print('Tidak ada jadwal pada waktu tersebut.')
    else:
        print('Pengingat Jadwal:')
        print_schedules(schedules)


def edit_schedule():
    show_schedules()

    nomor = input('Masukkan ID jadwal yang ingin diedit: ')

    tanggal_baru = input('Masukkan tanggal baru: ')
    waktu_baru = input('Masukkan waktu baru: ')
    kegiatan_baru = input('Masukkan nama kegiatan baru: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE schedules
        SET tanggal = ?, waktu = ?, kegiatan = ?
        WHERE id = ?
    ''', (tanggal_baru, waktu_baru, kegiatan_baru, nomor))

    connection.commit()
    connection.close()

    print('Jadwal berhasil diedit.')


def delete_schedule():
    show_schedules()

    nomor = input('Masukkan ID jadwal yang ingin dihapus: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM schedules WHERE id = ?', (nomor,))

    connection.commit()
    connection.close()

    print('Jadwal berhasil dihapus.')