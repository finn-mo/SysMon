# SysMon

**SysMon** is a simple, cross-platform system monitoring CLI tool written in Python using `psutil`, `tabulate`, and `colorama`. It displays disk usage, memory status, CPU load per core, and both local and public IP addresses in a clean, colorized, tabulated format.

## Features
- Disk usage summary for each mounted partition
- Memory usage breakdown (total, used, available)
- Per-core CPU load with percent usage
- Local and public IP address with system hostname
- Clean tabular formatting for output
- Color-coded section headers and error messages
- CLI flags to select which metrics to display

## CLI Usage

```bash
python sysmon.py [--disk] [--mem] [--cpu] [--net] [--all] [--version] [--log]
```

- `--disk` – Show disk usage
- `--mem` – Show memory usage
- `--cpu` – Show CPU usage
- `--net` – Show network information (hostname, local/public IP)
- `--all` – Show all metrics (default)
- `--version` – Show the current version of SysMon
- `--log` – Save output and errors to a timestamped log file (`logs/sysmon.log`)

## Example Output

```
================== System Monitor - v1.2.0 ==================

Disk Usage:
| Filesystem | Size | Used | Avail | Use% | Mounted on |
|------------|------|------|-------|------|-------------|
| /dev/sda1  | 120G | 85G  | 35G   | 71%  | /           |

Memory Usage:
| Total   | Used  | Free  |
|---------|-------|--------|
| 16.0 GB | 9.3 GB | 6.7 GB |

CPU Load:
| Core   | Usage |
|--------|--------|
| Core 0 | 12.5% |
| Core 1 | 17.8% |
| Core 2 |  9.2% |
| Core 3 | 10.1% |

Network Info:
| Hostname | Local IP Address | Public IP Address |
|----------|------------------|-------------------|
| my-pc    | 192.168.1.100    | 203.0.113.42      |
```

## Requirements
- Python 3.8+
- `psutil`
- `tabulate`
- `colorama`

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python sysmon.py --all
```

## Logging

To optionally log output and errors to a file for later review:

```bash
python sysmon.py --all --log
```

## License

MIT – see [`LICENSE`](LICENSE) file for details.