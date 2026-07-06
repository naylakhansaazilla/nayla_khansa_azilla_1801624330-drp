import json
import random
from datetime import datetime, timedelta

# =========================================================
# GENERATE DATA DUMMY JADWAL (untuk simulasi "data raya")
# Struktur mengikuti tabel `schedules` di Cheki-Cheki
# =========================================================

KEGIATAN_LIST = [
    'Rapat', 'Kuliah', 'Olahraga', 'Belanja', 'Nonton',
    'Mengerjakan Tugas', 'Meeting Klien', 'Istirahat',
    'Membaca Buku', 'Memasak', 'Jalan-jalan', 'Ibadah'
]

DESKRIPSI_LIST = [
    'Kegiatan rutin mingguan', 'Perlu persiapan sebelumnya',
    'Dilakukan bersama teman', 'Agenda penting bulan ini',
    'Sudah dijadwalkan sejak lama', ''
]


def random_tanggal():
    start = datetime(2026, 1, 1)
    delta_hari = random.randint(0, 364)
    tanggal = start + timedelta(days=delta_hari)
    return tanggal.strftime('%Y-%m-%d')


def random_waktu():
    jam = random.randint(0, 23)
    menit = random.randint(0, 59)
    return f'{jam:02d}:{menit:02d}'


def generate_data(jumlah):
    data = []
    for i in range(1, jumlah + 1):
        data.append({
            'id': i,
            'id_user': random.randint(1, 10),
            'tanggal': random_tanggal(),
            'waktu': random_waktu(),
            'kegiatan': random.choice(KEGIATAN_LIST),
            'deskripsi': random.choice(DESKRIPSI_LIST),
            'status': random.choice([0, 1])
        })
    return data


if __name__ == '__main__':
    # 1 baris data kira-kira ~110-130 byte dalam JSON.
    # 40.000 baris biasanya sudah menghasilkan file > 3 MB.
    JUMLAH_DATA = 40000
    NAMA_FILE = 'schedules_dummy.json'

    print(f'Membuat {JUMLAH_DATA} data dummy...')
    data_dummy = generate_data(JUMLAH_DATA)

    with open(NAMA_FILE, 'w') as f:
        json.dump(data_dummy, f, indent=2)

    print(f'Selesai! File tersimpan sebagai "{NAMA_FILE}"')
    print('Cek ukuran file dengan menjalankan: ls -lh schedules_dummy.json (Mac/Linux)')
    print('atau lihat properties file di File Explorer (Windows)')