def print_schedules(schedules):

    if len(schedules) == 0:
        print('Belum ada jadwal.')
        return

    for schedule in schedules:

        status = '✓ Selesai' if schedule[4] == 1 else '✗ Belum Selesai'

        print(
            f'{schedule[0]}. '
            f'{schedule[1]} | '
            f'{schedule[2]} | '
            f'{schedule[3]} | '
            f'{status}'
        )