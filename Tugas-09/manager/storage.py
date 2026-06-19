import sqlite3

DB_NAME = 'cheki_cheki.db'


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    # Tabel USER
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL
        )
    ''')

    # Menambahkan id_user, deskripsi, status
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            tanggal TEXT,
            waktu TEXT,
            kegiatan TEXT,
            deskripsi TEXT,
            status INTEGER DEFAULT 0,
            FOREIGN KEY (id_user) REFERENCES users(id_user)
        )
    ''')

    # Tabel CHECKLIST 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checklist(
            id_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
            id_schedule INTEGER,
            check_status INTEGER DEFAULT 0,
            check_date TEXT,
            FOREIGN KEY (id_schedule) REFERENCES schedules(id)
        )
    ''')

    # Tabel REMINDER
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders(
            id_reminder INTEGER PRIMARY KEY AUTOINCREMENT,
            id_schedule INTEGER,
            reminder_time TEXT,
            reminder_status TEXT DEFAULT 'pending',
            FOREIGN KEY (id_schedule) REFERENCES schedules(id)
        )
    ''')

    connection.commit()
    connection.close()


def get_or_create_user(user_name):
    """
    TAMBAHAN: dipanggil otomatis dari main.py saat user input nama di awal.
    Tidak ada menu CRUD User terpisah -- cukup CREATE jika user baru,
    atau langsung READ id_user jika nama sudah pernah dipakai.
    """
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT id_user FROM users WHERE user_name = ?', (user_name,))
    data = cursor.fetchone()

    if data:
        id_user = data[0]
    else:
        cursor.execute('INSERT INTO users (user_name) VALUES (?)', (user_name,))
        connection.commit()
        id_user = cursor.lastrowid

    connection.close()
    return id_user