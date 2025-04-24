"""
SysMon.py - A cross-platform system monitoring tool using psutil.
Displays disk usage, memory status, CPU load, and network IP.
"""

import psutil
import socket
from tabulate import tabulate

VERSION = 'v1.0.0'

def main():
    show_header()
    show_disk_usage()
    show_memory_usage()
    show_cpu_load()
    show_network_info()

def show_header():
    title = f'System Monitor - {VERSION}'
    print('\n' + title.center(50, '=') + '\n')

def show_disk_usage():
    table = []
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            table.append([
                partition.device,
                f'{usage.total / (1024**3):.0f}G',
                f'{usage.used / (1024**3):.0f}G',
                f'{usage.free / (1024**3):.0f}G',
                f'{usage.percent:.0f}%',
                partition.mountpoint
            ])
        except PermissionError:
            continue

    headers = ['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']
    print('Disk Usage:')
    print(tabulate(table, headers=headers, tablefmt='github'))
    print()

def show_memory_usage():
    mem = psutil.virtual_memory()
    table = [[
        f'{mem.total / (1024 ** 3):.1f} GB',
        f'{mem.used / (1024 ** 3):.1f} GB',
        f'{mem.available / (1024 ** 3):.1f} GB'
    ]]
    headers = ['Total', 'Used', 'Free']
    print('Memory Usage:')
    print(tabulate(table, headers=headers, tablefmt='github'))
    print()

def show_cpu_load():
    cores = psutil.cpu_percent(interval=1, percpu=True)
    table = [[f'Core {i}', f'{p:.1f}%'] for i, p in enumerate(cores)]
    print('CPU Load:')
    print(tabulate(table, headers=['Core', 'Usage'], tablefmt='github'))
    print()

def show_network_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f'IP Address: {ip}')
    except socket.error:
        print('IP Address: [Error retrieving IP]')
    print()

if __name__ == '__main__':
    main()