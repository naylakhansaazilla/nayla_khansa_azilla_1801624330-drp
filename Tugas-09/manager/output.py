def print_schedules(schedules):

    if len(schedules) == 0:
        print('Belum ada jadwal.')
        return

    for schedule in schedules:
        # schedule[6] = check_status, schedule[7] = check_date
        # (hasil JOIN dari tabel checklist)
        check_status = schedule[6] if len(schedule) > 6 else None
        check_date = schedule[7] if len(schedule) > 7 else None

        status = '✓ Selesai' if check_status == 1 else '✗ Belum Selesai'
        info_tambahan = f' (ditandai pada {check_date})' if check_date else ''

        print(
            f'{schedule[0]}. '
            f'{schedule[1]} | '
            f'{schedule[2]} | '
            f'{schedule[3]} | '
            f'{status}{info_tambahan}'
        )