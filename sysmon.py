"""
SysMon - A cross-platform system monitoring tool built with psutil.

This utility provides:
- Disk usage statistics
- Memory usage information
- CPU load per core
- Local and public IP addresses

Output is formatted using tabulate and colorized using colorama for readability.
"""

import socket
import argparse
import urllib.request
import os
from datetime import datetime

import psutil
from tabulate import tabulate
from colorama import init, Fore
init(autoreset=True)

VERSION = 'v1.1.1'


def main():
    args = get_args()

    display_flags = ['disk', 'mem', 'cpu', 'net', 'all']
    any_display_flags = any(getattr(args, flag) for flag in display_flags)

    show_header()
    if args.all or not any_display_flags:
        show_disk_usage()
        show_memory_usage()
        show_cpu_load()
        show_network_info()
    else:
        if args.disk: show_disk_usage()
        if args.mem: show_memory_usage()
        if args.cpu: show_cpu_load()
        if args.net: show_network_info()


def get_args():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(description='SysMon: A simple CLI tool to monitor and log system performance.')

    parser.add_argument('--disk', action='store_true', help='Display disk usage')
    parser.add_argument('--mem', action='store_true', help='Display memory usage')
    parser.add_argument('--cpu', action='store_true', help='Display CPU load')
    parser.add_argument('--net', action='store_true', help='Display network usage')
    parser.add_argument('--all', action='store_true', help='Display all system metrics')
    parser.add_argument('--version', action='version', version=f'SysMon {VERSION}', help='Show version and exit')

    return parser.parse_args()


def show_header():
    """Show program header."""
    title = f'System Monitor - {VERSION}'
    print('\n' + Fore.GREEN + title.center(50, '=') + '\n')


def show_disk_usage():
    """Show total disk space, used, free, and usage %."""
    table = []
    headers = ['Filesystem', 'Size', 'Used', 'Avail', 'Use%', 'Mounted on']
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
            print(Fore.RED + f'Permission denied accessing {partition.mountpoint}')

    print(Fore.CYAN + 'Disk Usage:')
    print(tabulate(table, headers=headers, tablefmt='github'))
    print()


def show_memory_usage():
    """Show total system memory, used, available."""
    try:
        mem = psutil.virtual_memory()
        table = [[
            f'{mem.total / (1024 ** 3):.1f} GB',
            f'{mem.used / (1024 ** 3):.1f} GB',
            f'{mem.available / (1024 ** 3):.1f} GB'
        ]]
        headers = ['Total', 'Used', 'Free']

        print(Fore.CYAN + 'Memory Usage:')
        print(tabulate(table, headers=headers, tablefmt='github'))
        print()
    except Exception as e:
        print(Fore.RED + f'Error retrieving memory info: {e}')
        print()


def show_cpu_load():
    """Show % usage for each CPU core."""
    try:
        cores = psutil.cpu_percent(interval=1, percpu=True)
        table = [[f'Core {i}', f'{p:.1f}%'] for i, p in enumerate(cores)]

        print(Fore.CYAN + 'CPU Load:')
        print(tabulate(table, headers=['Core', 'Usage'], tablefmt='github'))
        print()
    except Exception as e:
        print(Fore.RED + f'Error retrieving CPU load: {e}')


def show_network_info():
    """Show hostname, local IP, and public IP."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = get_public_ip()
        table = [[
            hostname,
            local_ip, 
            public_ip
        ]]
        headers = ['Hostname', 'Local IP Address', 'Public IP Address']

        print(Fore.CYAN + 'Network Info:')
        print(tabulate(table, headers=headers, tablefmt='github'))
        print()
    except Exception as e:
        print(Fore.RED + f'Error retrieving network info: {e}')
        print()


def get_public_ip():
    """Get public IP address from ipify.org."""
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
            return response.read().decode('utf-8')
    except Exception:
        return 'Unavailable'


if __name__ == '__main__':
    main()
