---
layout: default
title: Linux Installation Guide
---

# BenchVault Linux Installation Guide

BenchVault can run on Linux from source after PostgreSQL 16 and Python dependencies are installed. Packaged Linux builds are separate from the Windows Inno Setup installers.

## Tested Baseline

- Ubuntu 22.04 or newer
- Debian 12 or newer
- PostgreSQL 16
- Python 3.12
- PyQt6 desktop environment dependencies

## Install PostgreSQL

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

## Create Python Environment

```bash
cd ~/benchvault
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configure Database Environment

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=benchvault_project
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=your_postgres_password
```

## Start Desktop App

```bash
source venv/bin/activate
python main.py
```

## Start API Server

```bash
source venv/bin/activate
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

## Linux Data Locations

- Config: `~/.config/benchvault`
- Data and attachments: `~/.local/share/BenchVault`
- Logs: `~/.local/state/BenchVault/logs`
- Cache: `~/.cache/BenchVault`
