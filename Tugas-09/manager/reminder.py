from manager.storage import connect_db
from manager.output import print_schedules


def show_reminder():
    print('================================')
    print('       PENGINGAT JADWAL')
    print('================================')

    waktu = input('Masukkan waktu yang ingin dicek: ')

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM schedules WHERE waktu=?',
        (waktu,)
    )

    schedules = cursor.fetchall()

    connection.close()

    print_schedules(schedules)