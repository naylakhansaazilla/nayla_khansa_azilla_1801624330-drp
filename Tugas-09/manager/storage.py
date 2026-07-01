import sqlite3
import json
from datetime import datetime
from functools import reduce

DB_NAME = 'cheki_cheki.db'


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    # Tabel USER (baru, sesuai ERD)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL
        )
    ''')

    # Tabel SCHEDULE (ditambah id_user, deskripsi, status)
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

    # Tabel CHECKLIST (baru, sesuai ERD)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checklist(
            id_checklist INTEGER PRIMARY KEY AUTOINCREMENT,
            id_schedule INTEGER,
            check_status INTEGER DEFAULT 0,
            check_date TEXT,
            FOREIGN KEY (id_schedule) REFERENCES schedules(id)
        )
    ''')

    # Tabel REMINDER (sebelumnya cuma query ke schedules, sekarang jadi tabel sendiri sesuai ERD)
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


def export_data():
    """
    TUGAS 12 - EXPORT: Mengambil seluruh data dari database
    (users, schedules, checklist, reminders) lalu menyimpannya ke file JSON.
    """
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute('SELECT id_user, user_name FROM users')
    users_rows = cursor.fetchall()

    cursor.execute('SELECT id, id_user, tanggal, waktu, kegiatan, deskripsi, status FROM schedules')
    schedules_rows = cursor.fetchall()

    cursor.execute('SELECT id_checklist, id_schedule, check_status, check_date FROM checklist')
    checklist_rows = cursor.fetchall()

    cursor.execute('SELECT id_reminder, id_schedule, reminder_time, reminder_status FROM reminders')
    reminders_rows = cursor.fetchall()

    connection.close()

    # Ubah hasil query (tuple) jadi list of dictionary, supaya bisa ditulis ke JSON
    users_list = []
    for row in users_rows:
        users_list.append({
            'id_user': row[0],
            'user_name': row[1]
        })

    schedules_list = []
    for row in schedules_rows:
        schedules_list.append({
            'id': row[0],
            'id_user': row[1],
            'tanggal': row[2],
            'waktu': row[3],
            'kegiatan': row[4],
            'deskripsi': row[5],
            'status': row[6]
        })

    checklist_list = []
    for row in checklist_rows:
        checklist_list.append({
            'id_checklist': row[0],
            'id_schedule': row[1],
            'check_status': row[2],
            'check_date': row[3]
        })

    reminders_list = []
    for row in reminders_rows:
        reminders_list.append({
            'id_reminder': row[0],
            'id_schedule': row[1],
            'reminder_time': row[2],
            'reminder_status': row[3]
        })

    data = {
        'users': users_list,
        'schedules': schedules_list,
        'checklist': checklist_list,
        'reminders': reminders_list
    }

    # Nama file dibuat OTOMATIS pakai datetime.now(), TIDAK pakai input() dari user
    nama_file = 'export_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'

    file = open(nama_file, 'w')
    json.dump(data, file, indent=4)
    file.close()

    print(f'Data berhasil di-export ke file "{nama_file}"')


def import_data():
    """
    TUGAS 12 - IMPORT: Membaca file JSON, lalu memasukkan
    seluruh data di dalamnya ke database (users, schedules, checklist, reminders).
    """
    nama_file = input('Masukkan nama file JSON yang ingin di-import: ')

    try:
        file = open(nama_file, 'r')
    except FileNotFoundError:
        print(f'File "{nama_file}" tidak ditemukan!')
        return

    data = json.load(file)
    file.close()

    connection = connect_db()
    cursor = connection.cursor()

    # INSERT OR REPLACE dipakai supaya id yang sama tidak duplikat/error,
    # tapi langsung menimpa data lama dengan data dari file JSON
    for user in data['users']:
        cursor.execute(
            'INSERT OR REPLACE INTO users (id_user, user_name) VALUES (?, ?)',
            (user['id_user'], user['user_name'])
        )

    for schedule in data['schedules']:
        cursor.execute(
            '''
            INSERT OR REPLACE INTO schedules
            (id, id_user, tanggal, waktu, kegiatan, deskripsi, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (schedule['id'], schedule['id_user'], schedule['tanggal'],
             schedule['waktu'], schedule['kegiatan'], schedule['deskripsi'],
             schedule['status'])
        )

    for item in data['checklist']:
        cursor.execute(
            '''
            INSERT OR REPLACE INTO checklist
            (id_checklist, id_schedule, check_status, check_date)
            VALUES (?, ?, ?, ?)
            ''',
            (item['id_checklist'], item['id_schedule'],
             item['check_status'], item['check_date'])
        )

    for reminder in data['reminders']:
        cursor.execute(
            '''
            INSERT OR REPLACE INTO reminders
            (id_reminder, id_schedule, reminder_time, reminder_status)
            VALUES (?, ?, ?, ?)
            ''',
            (reminder['id_reminder'], reminder['id_schedule'],
             reminder['reminder_time'], reminder['reminder_status'])
        )

    connection.commit()
    connection.close()

    print(f'Data dari "{nama_file}" berhasil di-import ke database!')

def get_dashboard():
    from functools import reduce

def get_dashboard_mapreduce():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT tanggal, status
        FROM schedules
    """)

    schedules = cursor.fetchall()

    connection.close()
    # Map: mengambil nilai status dari setiap schedule
    status_list = list(
        map(lambda schedule: schedule[1], schedules)
    )
    # Filter: ambil status Completed (1)
    completed_list = list(
        filter(lambda status: status == 1, status_list)
    )

    # Filter: ambil status Pending (0)
    pending_list = list(
        filter(lambda status: status == 0, status_list)
    )
    # Reduce: menghitung total Completed
    completed = reduce(lambda x, y: x + y, completed_list, 0)

    # Reduce: menghitung jumlah Pending
    pending = reduce(lambda x, y: x + 1, pending_list, 0)

    # Total Schedule
    total = len(status_list)

    # Completion Rate
    if total == 0:
        rate = 0
    else:
        rate = round((completed / total) * 100, 2)
        # Filter: aktivitas hari ini
    today = datetime.now().strftime("%Y-%m-%d")

    today_list = list(
        filter(lambda schedule: schedule[0] == today, schedules)
    )

    activity_today = len(today_list)

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "rate": rate,
        "today": activity_today
    }

    connection = connect_db()
    cursor = connection.cursor()

    # Total Schedule
    cursor.execute("SELECT COUNT(*) FROM schedules")
    total = cursor.fetchone()[0]

    # Completed
    cursor.execute("SELECT COUNT(*) FROM schedules WHERE status = 1")
    completed = cursor.fetchone()[0]

    # Pending
    cursor.execute("SELECT COUNT(*) FROM schedules WHERE status = 0")
    pending = cursor.fetchone()[0]

    # Completion Rate
    if total == 0:
        rate = 0
    else:
        rate = round((completed / total) * 100, 2)

    # Activity Today
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "SELECT COUNT(*) FROM schedules WHERE tanggal = ?",
        (today,)
    )

    activity_today = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "rate": rate,
        "today": activity_today
    }