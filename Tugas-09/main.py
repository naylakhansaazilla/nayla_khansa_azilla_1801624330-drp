from tools import display_menu, select_menu
from manager.storage import create_table, get_or_create_user

if __name__ == '__main__':

    create_table()

    print('================================')
    print('Selamat datang di Cheki-Cheki ^^')
    print('================================')

    nama = input('Silakan masukkan namamu ya! ')

    id_user = get_or_create_user(nama)

    print()
    print(f'Baik, {nama}! Selamat mengatur jadwal harianmu di Cheki-Cheki ya!')
    print('Yuk, susun kegiatanmu agar lebih teratur dan produktif!')
    print()

    while True:
        display_menu()

        menu = input('Masukkan menu yang dipilih: ')

        is_done = select_menu(menu, id_user)

        if is_done:
            break