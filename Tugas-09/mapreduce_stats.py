from functools import reduce
from datetime import datetime

from manager.storage import connect_db

# =========================================================
# TUGAS 14 - MapReduce sederhana (tanpa PySpark)
# Menghitung statistik jadwal yang SAMA seperti Tugas 13,
# tapi datanya dibagi dulu ke minimal 2 "node" sebelum diolah.
# =========================================================

JUMLAH_NODE = 2


def baca_data():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT tanggal, status
        FROM schedules
    """)

    rows = cursor.fetchall()
    connection.close()

    # Ubah hasil query menjadi list of dictionary
    data = []

    for row in rows:
        data.append({
            'tanggal': row[0],
            'status': row[1]
        })

    return data


def bagi_node(data, jumlah_node=2):
    """
    Membagi data jadi beberapa kelompok (simulasi banyak node/komputer).
    Contoh: 40.000 data dibagi 2 node -> masing-masing 20.000 data.
    """
    ukuran = len(data) // jumlah_node
    node_list = []
    for i in range(jumlah_node):
        if i == jumlah_node - 1:
            # node terakhir ambil sisa data supaya tidak ada yang kelewat
            node_list.append(data[i * ukuran:])
        else:
            node_list.append(data[i * ukuran: (i + 1) * ukuran])
    return node_list


def hitung_statistik_node(node_data, today):
    """
    Ini bagian MAP - FILTER - REDUCE yang dijalankan
    secara terpisah untuk SATU node saja.
    """
    # MAP: ambil kolom status dari setiap schedule
    status_list = list(map(lambda s: s['status'], node_data))

    # FILTER: pisahkan yang selesai (1) dan belum (0)
    selesai_list = list(filter(lambda s: s == 1, status_list))
    belum_list = list(filter(lambda s: s == 0, status_list))

    # REDUCE: jumlahkan total yang selesai
    total_selesai = reduce(lambda x, y: x + y, selesai_list, 0)

    # FILTER: aktivitas hari ini (khusus node ini)
    aktivitas_hari_ini = list(filter(lambda s: s['tanggal'] == today, node_data))

    return {
        'total': len(status_list),
        'selesai': total_selesai,
        'belum': len(belum_list),
        'aktivitas_hari_ini': len(aktivitas_hari_ini)
    }


def gabungkan_hasil(daftar_hasil_node):
    """
    Ini bagian REDUCE terakhir - menggabungkan hasil
    dari semua node jadi satu kesimpulan akhir.
    """
    total = reduce(lambda x, y: x + y['total'], daftar_hasil_node, 0)
    selesai = reduce(lambda x, y: x + y['selesai'], daftar_hasil_node, 0)
    belum = reduce(lambda x, y: x + y['belum'], daftar_hasil_node, 0)
    aktivitas_hari_ini = reduce(lambda x, y: x + y['aktivitas_hari_ini'], daftar_hasil_node, 0)

    rate = round((selesai / total) * 100, 2) if total > 0 else 0

    return {
        'total': total,
        'selesai': selesai,
        'belum': belum,
        'rate': rate,
        'aktivitas_hari_ini': aktivitas_hari_ini
    }


if __name__ == '__main__':
    print('Membaca data dari database SQLite...')
    data = baca_data()
    print(f'Total data dibaca: {len(data)}\n')

    today = datetime.now().strftime('%Y-%m-%d')

    # 1. Bagi data ke beberapa node
    node_list = bagi_node(data, JUMLAH_NODE)
    for i, node in enumerate(node_list, start=1):
        print(f'Node {i} mendapat {len(node)} data')

    # 2. Tiap node hitung statistiknya sendiri-sendiri
    print('\nMenghitung statistik per node...')
    hasil_per_node = []
    for i, node in enumerate(node_list, start=1):
        hasil = hitung_statistik_node(node, today)
        hasil_per_node.append(hasil)
        print(f'Hasil Node {i}: {hasil}')

    # 3. Gabungkan semua hasil node jadi kesimpulan akhir
    hasil_akhir = gabungkan_hasil(hasil_per_node)

    print('\n================================')
    print('   STATISTIK JADWAL (MapReduce)')
    print('================================')
    print(f'Total Schedule  : {hasil_akhir["total"]}')
    print(f'Completed       : {hasil_akhir["selesai"]}')
    print(f'Pending         : {hasil_akhir["belum"]}')
    print(f'Completion Rate : {hasil_akhir["rate"]}%')
    print(f'Activity Today  : {hasil_akhir["aktivitas_hari_ini"]}')
    print('================================')