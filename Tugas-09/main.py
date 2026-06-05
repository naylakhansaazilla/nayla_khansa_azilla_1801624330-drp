# Penyimpanan data

# Komponen aplikasi perangkat lunak:
# 1. Create (Tambah Jadwal)
# 2. Read (Lihat Jadwal)
# 3. Update (Edit Jadwal / Checklist)
# 4. Delete (Hapus Jadwal)

# Aplikasi: Cheki-Cheki
# Aplikasi pengelola jadwal harian

from tools import display_menu, select_menu
from manager.storage import create_table

if __name__ == '__main__':

    create_table()
    
    print('================================')
    print('Selamat datang di Cheki-Cheki ^^')
    print('================================')

nama = input('Silakan masukkan namamu ya!')

print()
print(f'Baik, {nama}! Selamat mengatur jadwal harianmu di Cheki-Cheki ya!')
print('Yuk, susun kegiatanmu agar lebih teratur dan produktif!')
print()

while True:
    display_menu()
    
    menu = input('Masukkan menu yang dipilih: ')
    
    is_done = select_menu(menu)
    
    if is_done:
        break