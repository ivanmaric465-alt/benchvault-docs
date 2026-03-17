---
layout: default
title: Installation Guide
---

# BenchVault v3.2.0 - Installation Guide

Complete installation instructions for server and client computers.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [PostgreSQL Installation](#postgresql-installation)
3. [Server Installation](#server-installation)
4. [Client Installation](#client-installation)
5. [Network Configuration](#network-configuration)
6. [Voice Transcription Setup](#voice-transcription-setup)
7. [AI Assistant Setup](#ai-assistant-setup)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

| Component | Server | Client |
|-----------|--------|--------|
| OS | Windows 10/11 (64-bit) | Windows 10/11 (64-bit) |
| RAM | 8 GB recommended | 4 GB minimum |
| Disk | 500 MB + database | 100 MB |
| PostgreSQL | Required (installed locally) | Not required |
| Network | Static IP recommended | Access to server |

---

## PostgreSQL Installation

PostgreSQL must be installed on the **server computer** before BenchVault.

### Step 1: Download
1. Go to https://www.postgresql.org/download/windows/
2. Click "Download the installer"
3. Select version 16.x (or latest)
4. Download Windows x86-64 installer

### Step 2: Install
1. Run `postgresql-16.x-windows-x64.exe` as administrator
2. Use default installation directory: `C:\Program Files\PostgreSQL\16`
3. Keep all components checked (Server, pgAdmin, Command Line Tools)
4. Set a **strong password** for the `postgres` user
   - **IMPORTANT**: Write this down - you need it for BenchVault setup
5. Use default port: `5432`
6. Complete installation

### Step 3: Verify Installation
1. Open Windows Services (`Win+R` -> `services.msc`)
2. Find `postgresql-x64-16` (or your version)
3. Status should be **Running**
4. If stopped, right-click -> Start

**Optional Test:**
```cmd
psql -U postgres
-- Enter password when prompted
-- Type \q to quit
```

---

## Server Installation

Install on the computer that hosts the database.

### Step 1: Run Installer
1. Download `BenchVault_Setup_3.2.0.exe` (~50 MB)
2. Right-click -> Run as administrator
3. Follow installation wizard
4. Click Finish

### Step 2: First Launch
1. Setup Wizard runs automatically
2. Checks for PostgreSQL installation (green checkmark = found)
3. Checks PostgreSQL service is running
4. Click "Launch BenchVault" when all checks pass

### Step 3: Create Project
The **Project Selector** dialog appears:

1. Click "Create New Project"
2. Fill in ALL fields:
   | Field | Example | Notes |
   |-------|---------|-------|
   | Project Name | Chemistry Lab | Display name |
   | Database Name | chem_lab_2026 | Lowercase, no spaces |
   | Host | localhost | For local server |
   | Port | 5432 | PostgreSQL default |
   | User | postgres | PostgreSQL user |
   | Password | (your password) | From PostgreSQL install |

3. Click **Test Connection** - should show success
4. Click **Create Project**

### Step 4: Register First User
1. Click "Register" on login screen
2. Enter username, password, full name, email
3. Click "Register"

**Note**: First user becomes **Master** (administrator).

---

## Client Installation

Install on workstations that connect to the server.

### Step 1: Run Installer
1. Download `BenchVault_Setup_Client_3.2.0.exe` (~25-30 MB)
2. Run as administrator
3. Complete installation

### Step 2: Configure Server Connection
On first launch, **Server Configuration Dialog** appears:

| Field | Value |
|-------|-------|
| Server Address | Server's IP address (e.g., `192.168.1.100`) |
| Port | `5432` |
| Database | Same database name as server (e.g., `chem_lab_2026`) |
| Username | `postgres` |
| Password | PostgreSQL password |

1. Click **Test Connection**
2. Click **Save & Connect**

### Step 3: Login
Use your BenchVault account (created on server).

---

## Network Configuration

Required for clients to connect to server over network.

### On Server Computer

#### 1. Configure PostgreSQL for Network Access

**Edit postgresql.conf:**
```
Location: C:\Program Files\PostgreSQL\16\data\postgresql.conf
```

Find and modify:
```conf
# Uncomment and change from 'localhost' to '*'
listen_addresses = '*'
```

**Edit pg_hba.conf:**
```
Location: C:\Program Files\PostgreSQL\16\data\pg_hba.conf
```

Add at the end:
```conf
# Allow connections from any IP (for lab network)
host    all    all    0.0.0.0/0    md5

# Or restrict to specific subnet (more secure):
# host    all    all    192.168.1.0/24    md5
```

#### 2. Restart PostgreSQL Service
```cmd
net stop postgresql-x64-16
net start postgresql-x64-16
```

Or via Services (`services.msc`): Right-click -> Restart

#### 3. Configure Windows Firewall
```cmd
netsh advfirewall firewall add rule name="PostgreSQL" dir=in action=allow protocol=TCP localport=5432
netsh advfirewall firewall add rule name="BenchVault API" dir=in action=allow protocol=TCP localport=8000
```

Or use Windows Firewall GUI:
- Inbound Rules -> New Rule -> Port -> TCP -> 5432 -> Allow

#### 4. Find Server IP Address
```cmd
ipconfig
```
Note the IPv4 Address (e.g., `192.168.1.100`)

### On Client Computers

#### Test Connectivity
```cmd
ping 192.168.1.100
```

Should receive replies. If timeout:
- Check both on same network
- Check firewall rules on server
- Verify correct IP address

---

## Voice Transcription Setup

**Optional feature.** Voice transcription uses OpenAI Whisper AI and is not included in the main BenchVault installer due to its large size (~400 MB) and a known conflict with the PyInstaller build (OpenMP DLL clash). It is installed separately via the **Transcription Pack**.

> **Running from Python source?** See [Option B: Direct Install (Source/Dev)](#option-b-direct-install-sourcedev) below.

---

### Option A: Transcription Pack (Installed App — Recommended)

The Transcription Pack is a self-contained portable Python environment with Whisper and FFmpeg bundled. It does **not** require Python to be installed on the machine and does **not** conflict with the main BenchVault application.

#### Step 1: Download the Transcription Pack
1. Open BenchVault
2. Go to **Tools -> Transcription Settings**
3. Click **Download Transcription Pack**
4. Wait for the download to complete (~400 MB)
5. The pack installs automatically to `%LOCALAPPDATA%\BenchVault\transcription_pack\`

#### Step 2: Download a Whisper Model
1. Still in **Tools -> Transcription Settings**, select a model:

   | Model | Size | Speed | Accuracy |
   |-------|------|-------|----------|
   | tiny | 75 MB | Fastest | Basic |
   | base | 145 MB | Fast | Good |
   | small | 488 MB | Medium | Better |
   | medium | 1.5 GB | Slow | High |
   | large | 3.1 GB | Slowest | Best |

   **Recommendation**: Start with `base` — good balance of speed and accuracy.

2. Click **Download** next to your chosen model
3. Models are cached in `~\.cache\whisper\`

#### Step 3: Transcribe Audio
1. Open an experiment with an audio file attached
2. Select the audio file
3. Click **Transcribe**
4. Wait for processing (first run loads the model — may take a few seconds)
5. Choose **Insert into Notes** or **Copy to Clipboard**

---

### Option B: Direct Install (Source/Dev)

For users running BenchVault from the Python source rather than the installer.

#### Step 1: Install FFmpeg
1. Download from https://ffmpeg.org/download.html (Windows builds)
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Open System Properties -> Environment Variables
   - Edit PATH -> Add `C:\ffmpeg\bin`
4. Verify: `ffmpeg -version`

#### Step 2: Install Whisper
```cmd
pip install openai-whisper torch --index-url https://download.pytorch.org/whl/cpu
```

For GPU acceleration (NVIDIA):
```cmd
pip install openai-whisper torch --index-url https://download.pytorch.org/whl/cu118
```

#### Step 3: Download a Model and Transcribe
Follow Steps 2–3 from Option A above (Tools -> Transcription Settings).

---

## AI Assistant Setup

**Optional feature.** The AI Assistant uses the Claude API (by Anthropic) to let users ask natural-language questions about their lab data. It requires an API key and internet access.

### Step 1: Get an API Key
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Go to API Keys and create a new key
4. Copy the key (starts with `sk-ant-...`)

### Step 2: Configure in BenchVault
**Option A — Application Settings (recommended):**
1. Login as Master user
2. Go to **Tools -> Application Settings**
3. Paste the API key in the **Claude API Key** field
4. Set the **Monthly Budget per User** (default: $5)
5. Click Save

**Option B — Environment Variable:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```
The environment variable takes priority over the database-stored key.

### Step 3: Use the Assistant
- Any user can open **Tools -> AI Assistant** (or **Ctrl+Shift+A**)
- Select a model (Haiku is default and cheapest)
- Ask questions about experiments, inventory, samples, equipment, etc.

---

## Troubleshooting

### PostgreSQL Issues

#### "PostgreSQL Not Found" in Setup Wizard
- Verify PostgreSQL installed: Check `C:\Program Files\PostgreSQL\16` exists
- Restart computer after PostgreSQL installation
- Run BenchVault as administrator

#### "PostgreSQL Service Not Running"
1. Open Services (`services.msc`)
2. Find `postgresql-x64-16`
3. Right-click -> Start
4. Set Startup Type to "Automatic"

### Connection Issues

#### Client Can't Connect to Server
1. **Verify server works locally**: Open BenchVault on server
2. **Ping server**: `ping SERVER_IP`
3. **Check firewall**: Temporarily disable to test
4. **Check pg_hba.conf**: Ensure network rule is added
5. **Restart PostgreSQL**: After any config changes

#### "Database does not exist"
- Verify exact database name (case-sensitive)
- Create project on server first, then connect clients

### Installation Issues

#### Installer Won't Run
- Right-click -> Run as administrator
- Check Windows SmartScreen isn't blocking

#### "Cannot write to Program Files"
- Must run as administrator
- Or install to different location (e.g., `C:\BenchVault`)

### Transcription Issues

#### Transcription Pack download fails
- Check internet connection
- Retry — the download is ~400 MB and may time out on slow connections
- Verify `%LOCALAPPDATA%\BenchVault\` folder is writable

#### "Model download failed"
- Check internet connection
- Try a smaller model first (`tiny` or `base`)
- Models are cached in `~\.cache\whisper\`

#### Transcription produces no output or errors
- Ensure the audio file is a supported format (MP3, WAV, M4A, OGG, FLAC, AAC)
- Verify the Transcription Pack is fully installed (Tools -> Transcription Settings should show pack status)
- Try the `tiny` model to rule out memory issues

---

## Silent Installation (IT Deployment)

### Server
```cmd
BenchVault_Setup_3.2.0.exe /SILENT /DIR="C:\BenchVault"
```

### Client
```cmd
BenchVault_Setup_Client_3.2.0.exe /SILENT /DIR="C:\BenchVault Client"
```

Then configure via `%LOCALAPPDATA%\BenchVault_Client\server_config.json`:
```json
{
  "host": "192.168.1.100",
  "port": "5432",
  "database": "chem_lab_2026",
  "user": "postgres",
  "password": "your_password"
}
```

---

## Post-Installation Checklist

### Server
- [ ] PostgreSQL installed and running
- [ ] BenchVault server installed
- [ ] Project created successfully
- [ ] Master user registered
- [ ] Firewall rules configured (multi-user)
- [ ] pg_hba.conf updated (multi-user)

### Client
- [ ] BenchVault client installed
- [ ] Server connection configured
- [ ] Can login with BenchVault account
- [ ] Can view experiments/inventory

### Optional
- [ ] Email settings configured (notifications)
- [ ] Cloud backup configured
- [ ] Voice transcription setup
- [ ] AI Assistant configured (Tools -> Application Settings -> Claude API Key)
- [ ] Backup schedule established
