import random
from datetime import datetime, timedelta

from manager.storage import connect_db

KEGIATAN = [
    "Kuliah",
    "Belajar",
    "Olahraga",
    "Rapat",
    "Mengerjakan Tugas",
    "Belanja",
    "Meeting",
    "Memasak",
    "Membaca Buku",
    "Jalan-jalan"
]

def generate_dummy(jumlah=50):
    connection = connect_db()
    cursor = connection.cursor()

    today = datetime.now()

    for i in range(jumlah):
        tanggal = (today + timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        waktu = f"{random.randint(7,21):02d}:{random.choice([0,15,30,45]):02d}"
        kegiatan = random.choice(KEGIATAN)
        deskripsi = "Dummy Data"
        status = random.randint(0, 1)
        cursor.execute(
            '''
            INSERT INTO schedules
            (id_user, tanggal, waktu, kegiatan, deskripsi, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                1,
                tanggal,
                waktu,
                kegiatan,
                deskripsi,
                status
            )
        )
    
    connection.commit()
    connection.close()

    print(f"{jumlah} dummy data berhasil ditambahkan!")

if __name__ == "__main__":
    generate_dummy(50)