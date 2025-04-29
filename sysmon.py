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

VERSION = 'v1.2.0'


def main():
    """Get CLI arguments and display selected system info."""
    args = get_args()
    display_flags = ['disk', 'mem', 'cpu', 'net', 'all']
    any_display_flags = any(getattr(args, flag) for flag in display_flags)
    log_enabled = args.log

    show_header()
    if args.all or not any_display_flags:
        show_disk_usage(log_enabled)
        show_memory_usage(log_enabled)
        show_cpu_load(log_enabled)
        show_network_info(log_enabled)
    else:
        if args.disk: show_disk_usage(log_enabled)
        if args.mem: show_memory_usage(log_enabled)
        if args.cpu: show_cpu_load(log_enabled)
        if args.net: show_network_info(log_enabled)


def get_args():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(description='SysMon: A simple CLI tool to monitor and log system performance.')

    parser.add_argument('--disk', action='store_true', help='Display disk usage')
    parser.add_argument('--mem', action='store_true', help='Display memory usage')
    parser.add_argument('--cpu', action='store_true', help='Display CPU load')
    parser.add_argument('--net', action='store_true', help='Display network usage')
    parser.add_argument('--all', action='store_true', help='Display all system metrics')
    parser.add_argument('--log', action='store_true', help='Log program output to "logs/sysmon.log"')
    parser.add_argument('--version', action='version', version=f'SysMon {VERSION}', help='Show version and exit')

    return parser.parse_args()


def log_to_file(section_title, content, log_path='logs/sysmon.log'):
    """Append a section and content to the log file with a timestamp."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

    with open(log_path, 'a') as f:
        f.write(f'{timestamp} {section_title}\n')
        f.write(content)
        f.write('\n' + '-'*60 + '\n')


def show_header():
    """Show program header."""
    title = f'System Monitor - {VERSION}'
    print('\n' + Fore.GREEN + title.center(50, '=') + '\n')


def show_disk_usage(log_enabled=False):
    """Show total disk space, used space, free space, and percentage of disk space used."""
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
            error_message = f'Permission denied accessing {partition.mountpoint}'
            print(Fore.RED + error_message)

            if log_enabled:
                log_to_file('Disk Usage Error', error_message)

    if table:
        output_text = tabulate(table, headers=headers, tablefmt='github')

        print(Fore.CYAN + 'Disk Usage:')
        print(output_text)
        print()

        if log_enabled:
            log_to_file('Disk Usage', output_text)
    else:
        print() # break between sections if all disks returned errors


def show_memory_usage(log_enabled=False):
    """Show total system memory, used memory, and available memory."""
    try:
        mem = psutil.virtual_memory()
        table = [[
            f'{mem.total / (1024 ** 3):.1f} GB',
            f'{mem.used / (1024 ** 3):.1f} GB',
            f'{mem.available / (1024 ** 3):.1f} GB'
        ]]
        headers = ['Total', 'Used', 'Free']
        output_text = tabulate(table, headers=headers, tablefmt='github')

        print(Fore.CYAN + 'Memory Usage:')
        print(output_text)
        print()

        if log_enabled:
            log_to_file('Memory Usage', output_text)
    except Exception as e:
        error_message = f'Error retrieving memory info: {e}'
        print(Fore.RED + error_message)
        print()

        if log_enabled:
            log_to_file('Memory Usage Error', error_message)


def show_cpu_load(log_enabled=False):
    """Show CPU load percentage for each core."""
    try:
        cores = psutil.cpu_percent(interval=1, percpu=True)
        table = [[f'Core {i}', f'{p:.1f}%'] for i, p in enumerate(cores)]
        headers = ['Core', 'Usage']
        output_text = tabulate(table, headers=headers, tablefmt='github')

        print(Fore.CYAN + 'CPU Load:')
        print(output_text)
        print()

        if log_enabled:
            log_to_file('CPU Load', output_text)
    except Exception as e:
        error_message = f'Error retrieving CPU load: {e}'
        print(Fore.RED + error_message)

        if log_enabled:
            log_to_file('CPU Load Error', error_message)


def show_network_info(log_enabled=False):
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
        output_text = tabulate(table, headers=headers, tablefmt='github')

        print(Fore.CYAN + 'Network Info:')
        print(output_text)
        print()

        if log_enabled:
            log_to_file('Network Info', output_text)
    except Exception as e:
        error_message = f'Error retrieving network info: {e}'
        print(Fore.RED + error_message)
        print()

        if log_enabled:
            log_to_file('Network Info Error', error_message)


def get_public_ip():
    """Get public IP address from ipify.org."""
    try:
        with urllib.request.urlopen('https://api.ipify.org', timeout=5) as response:
            return response.read().decode('utf-8')
    except Exception:
        return 'Unavailable'


if __name__ == '__main__':
    main()
