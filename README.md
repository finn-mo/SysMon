# SysMon

**SysMon** is a simple, cross-platform system monitoring CLI tool written in Python using `psutil` and `tabulate`. It displays disk usage, memory status, CPU load per core, and your IP address in a clean, tabulated format.

## Features
- Disk usage summary for each partition
- Memory usage breakdown
- Per-core CPU load with percent usage
- Network hostname and IP address
- Tabular formatting for easy reading

## Example Output

```
================ System Monitor - v1.0 ================

Disk Usage:
| Filesystem | Size | Used | Avail | Use% | Mounted on |
|------------|------|------|-------|------|-------------|
| /dev/sda1  | 120G | 85G  | 35G   | 71%  | /           |
| /dev/sdb1  | 500G | 400G | 100G  | 80%  | /home       |

Memory Usage:
| Total   | Used  | Free  |
|---------|-------|--------|
| 16.0 GB | 9.3 GB | 6.7 GB |

CPU Load:
| Core    | Usage |
|---------|--------|
| Core 0 | 12.5%  |
| Core 1 | 17.8%  |
| Core 2 |  9.2%  |
| Core 3 | 10.1%  |

IP Address: 192.168.1.100
```

## Requirements
- Python 3.8+
- psutil
- tabulate

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python sysmon.py
```

## License

MIT – see [`LICENSE`](LICENSE) file for details.