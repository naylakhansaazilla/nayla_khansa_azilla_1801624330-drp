import sqlite3

DB_NAME = 'cheki_cheki.db'


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            waktu TEXT,
            kegiatan TEXT,
            selesai INTEGER
        )
    ''')

    connection.commit()
    connection.close()