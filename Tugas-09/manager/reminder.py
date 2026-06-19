from manager.storage import connect_db
from manager.output import print_schedules


def show_reminder():
    print('================================')
    print('       PENGINGAT JADWAL')
    print('================================')

    waktu = input('Masukkan waktu yang ingin dicek: ')

    connection = connect_db()
    cursor = connection.cursor()

    # sekarang query ke tabel reminders lalu JOIN ke schedules
    # mengubah reminder.py menjadi entitas baru

    cursor.execute('''
        SELECT s.id, s.tanggal, s.waktu, s.kegiatan, s.deskripsi,
               s.status, NULL, NULL
        FROM reminders r
        JOIN schedules s ON r.id_schedule = s.id
        WHERE r.reminder_time = ?
    ''', (waktu,))

    schedules = cursor.fetchall()

    connection.close()

    if len(schedules) == 0:
        print(f'Tidak ada pengingat pada pukul {waktu}.')
    else:
        print_schedules(schedules)