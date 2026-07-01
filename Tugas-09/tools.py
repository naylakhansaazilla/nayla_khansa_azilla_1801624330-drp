from manager.schedule import (
    add_schedule,
    show_schedule,
    edit_schedule,
    toggle_selesai,
    delete_schedule
)

from manager.reminder import show_reminder
from manager.storage import export_data, import_data


def display_menu():
    # Tampilan pilihan menu (UI)
    print('================================')
    print('         CHEKI-CHEKI')
    print('================================')
    print('1. Tambah Jadwal')
    print('2. Daftar Kegiatan')
    print('3. Pengingat')
    print('4. Edit Jadwal')
    print('5. Hapus Jadwal')
    print('6. Status Jadwal')
    print('7. Export Data')
    print('8. Import Data')
    print('9. Statistik Jadwal')
    print('10. Keluar')
    print('================================')


def select_menu(menu, id_user):
    # Seleksi menu

    if menu == '1':
        # Logic untuk tambah jadwal
        print('Anda mengakses menu "Tambah Jadwal"')
        add_schedule(id_user)

    elif menu == '2':
        # Logic untuk melihat daftar kegiatan
        print('Anda mengakses menu "Daftar Kegiatan"')
        print('Di menu ini Anda dapat melihat dan checklist kegiatan.')
        show_schedule()

    elif menu == '3':
        # Logic untuk pengingat
        print('Anda mengakses menu "Pengingat"')
        show_reminder()

    elif menu == '4':
        # Logic untuk edit jadwal
        print('Anda mengakses menu "Edit Jadwal"')
        edit_schedule()

    elif menu == '5':
        # Logic untuk hapus jadwal
        print('Anda mengakses menu "Hapus Jadwal"')
        delete_schedule()

    elif menu == '6':
        # Logic untuk mengakses jadwal terbaru
        print('Anda mengakses menu "Status Jadwal"')
        toggle_selesai()

    elif menu == '7':
        # Logic untuk export data
        print('Anda mengakses menu "Export Data"')
        export_data()

    elif menu == '8':
        # Logic Import Data
        print('Anda mengakses menu "Import Data"')
        import_data()

      elif menu == '9':
        # Logic untuk melakukan statistik jadwal yang ada
        print('Anda mengakses menu "Statistik Jadwal"')
        show_statistik()
 
    elif menu == '10':
         # Logic untuk keluar program
        print('Terima kasih telah menggunakan Cheki-Cheki ^^')
        return True
 
    else:
        # Logic jika input tidak sesuai menu
        print('Menu tidak tersedia')
 
    return False

  