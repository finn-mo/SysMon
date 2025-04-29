# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.1.1] - 2025-04-29
### Changed
- Added docstrings to functions, following PEP 257 formatting guidelines for documentation

## [1.1.0] – 2025-04-24
### Added
- `--disk`, `--mem`, `--cpu`, `--net`, and `--all` flags to selectively display system metrics
- `--version` flag to display the current SysMon version
- `show_network_info()` now displays:
  - System hostname
  - Local IP address
  - Public IP address (using Python's standard `urllib` library)
- Colorized output using `colorama`:
  - Section headers are cyan
  - Errors are printed in red for visibility

### Changed
- All system display functions now include error handling with consistent output formatting
- Public IP detection uses only standard library (no third-party dependencies)
- Output of `show_network_info()` is now tabulated to match the rest of the utility
- Section headers standardized across all display functions

## [1.0.0] – 2025-04-23
- Initial release of SysMon
- Displays disk, memory, CPU, and network IP information
- Clean tabulated output using `tabulate`
- Modular design with separate functions for each system stat
- Project structured for cross-platform support (Linux, macOS, Windows)
- Includes MIT License, `.gitignore`, `CHANGELOG.md`, and complete `README.md`