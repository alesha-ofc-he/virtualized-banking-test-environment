# Virtualized Banking Test Environment

A Python-based tool to automate VM setup for banking application testing, inspired by my internship at Forte Bank.

## Features
- Automate VM creation with VMware Fusion.
- Configure bridged networking.
- Test connectivity to a mock API.
- Automate snapshots.
- Log results in PostgreSQL and generate reports.

## Installation
1. Install Python 3.11+: https://www.python.org/downloads/macos/
2. Install PostgreSQL 16: https://www.postgresql.org/download/macosx/
3. Create database: `psql -U postgres` then `CREATE DATABASE vm_test_db;`
4. Install VMware Fusion: https://www.vmware.com/products/fusion/fusion-evaluation.html
5. Install dependencies: `pip3 install -r requirements.txt`
6. Configure credentials in `main.py` and `database.py`.

## Usage
```bash
python3 main.py