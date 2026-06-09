---
layout: default
title: Installation Guide
---

# BenchVault — Installation Guide

Simple installation for Windows users. BenchVault is a multi-user lab data management system with an API-first desktop app. The same Windows installer is used for single-PC/server installs and client workstations.

For Linux source-run setup, see **docs/LINUX_INSTALLATION_GUIDE.md**.
For VPS/cloud deployment, see **deploy/VPS_DEPLOY_INSTRUCTIONS.md**.

---

## Table of Contents
1. [Quick Start (Single PC)](#quick-start-single-pc)
2. [Server + Client PCs (lab/team)](#server--client-pcs-labteam)
3. [Voice Transcription Setup](#voice-transcription-setup)
4. [AI Assistant Setup](#ai-assistant-setup)
5. [Troubleshooting](#troubleshooting)
6. [Silent Installation (IT Deployment)](#silent-installation-it-deployment)

---

## Quick Start (Single PC)

Everything runs on one computer: PostgreSQL, the BenchVault API server, and the desktop app. This is the simplest setup.

### Step 1: Install PostgreSQL

1. Download PostgreSQL 16 from https://www.postgresql.org/download/windows/
2. Run the installer as administrator
3. Use default directory: `C:\Program Files\PostgreSQL\16`
4. Keep all components checked (Server, pgAdmin, Command Line Tools)
5. Set a strong password for the `postgres` user — **write it down**, you'll need it
6. Use default port `5432`, complete installation

### Step 2: Install BenchVault

1. Download `BenchVault_Setup_4.1.1.exe`
2. Right-click → Run as administrator
3. Follow the installation wizard
4. Click Finish — a desktop shortcut is created

### Step 3: Launch the Setup Wizard

1. Double-click the BenchVault desktop icon
2. The **Setup Wizard** opens and automatically detects PostgreSQL
3. If PostgreSQL is running, the wizard shows a **Database Configuration** dialog:
   - Host: `localhost` (default)
   - Port: `5432` (default)
   - User: `postgres` (default)
   - Password: your PostgreSQL password (set during PostgreSQL install)
   - Database name: `benchvault_lab` (default, or choose your own)
4. Click **Test Connection** — should show ✅
5. Click **Save & Continue** — the database is created automatically
6. Click **Launch Local BenchVault**

The API server starts automatically and the login dialog appears.

> **What if I skip?** Click **Skip Local DB Setup** only if you will configure the local API server manually via environment variables (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`). Client workstations should use **Connect to Existing Server** instead.

### Step 4: Login

1. The login dialog appears with `http://localhost:8000` pre-filled
2. Click the **Register** tab
3. Enter a username, password, and email
4. Click **Create Account** — the first user becomes Master (administrator)
5. You're logged in

---

## Server + Client PCs (lab/team)

Use the same `BenchVault_Setup_4.1.1.exe` installer everywhere. One computer runs PostgreSQL and the API server. Other computers are client workstations that connect through the API URL and do **not** need PostgreSQL.

### On the Server PC

1. Install PostgreSQL 16 (same as Quick Start Step 1)
2. Install BenchVault and run the Setup Wizard (same as Quick Start Steps 2–4)
   - The Setup Wizard will configure the database for you
   - Register the Master user
3. Open Windows Firewall for API access from other devices:
   ```cmd
   netsh advfirewall firewall add rule name="BenchVault API" dir=in action=allow protocol=TCP localport=8000
   ```
   - Port `8000` is used by desktop, mobile, standalone/server, and VPS API deployments.
   - By default the desktop auto-starts the API in local/tunnel mode (`127.0.0.1`). A Master user can enable **User -> Allow Direct LAN Access** to rebind the same API for direct LAN clients (`0.0.0.0`).
   - If you use ngrok, you can leave the API in local/tunnel mode and point ngrok at `http://localhost:8000`.
4. Find your server IP:
   ```cmd
   ipconfig
   ```
   Note the IPv4 Address (e.g., `192.168.1.50`)
5. To keep the API server running when you close the desktop, see [Windows Service Setup](#windows-service-setup) below

### On Each Client PC

1. Download and install `BenchVault_Setup_4.1.1.exe` (same installer)
2. Launch BenchVault — the Setup Wizard runs
3. Click **Connect to Existing Server**
   - PostgreSQL is not required on client workstations
   - The desktop app opens directly to the login dialog
4. In the login dialog, replace `http://localhost:8000` with the server's API URL:
   ```
   http://192.168.1.50:8000
   ```
   If the server PC is using **Allow Direct LAN Access** from the desktop User menu, use the URL shown by the app, typically:
   ```
   http://192.168.1.50:8000
   ```
5. Login with your BenchVault account (or register if you're new)
6. You're connected

---

### Windows Service Setup

To run the API server as a background service on Windows Server:

#### Option A: Task Scheduler (simplest)
1. Open Task Scheduler (`taskschd.msc`)
2. Create a Basic Task → Trigger: "At startup"
3. Action: Start a program → `C:\Program Files\BenchVault\BenchVault_API_Server.exe`

#### Option B: NSSM (more robust)
1. Download NSSM from https://nssm.cc/
2. Run: `nssm install BenchVaultAPI`
3. Set Application path to `C:\Program Files\BenchVault\BenchVault_API_Server.exe`
4. Set Startup directory to `C:\Program Files\BenchVault`
5. On the **Environment** tab, add `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` matching the database configured in the Setup Wizard
6. Click "Install service"
7. Run: `nssm start BenchVaultAPI`

---

## Voice Transcription Setup

**Optional feature.** Voice transcription uses OpenAI Whisper AI and is not included in the main BenchVault installer due to its large size (~400 MB). It is installed separately via the **Transcription Pack**.

> **Running from Python source?** See [Option B: Direct Install (Source/Dev)](#option-b-direct-install-sourcedev) below.

---

### Option A: Transcription Pack (Installed App — Recommended)

The Transcription Pack is a self-contained portable Python environment with Whisper and FFmpeg bundled. It does **not** require Python to be installed on the machine.

#### Step 1: Download the Transcription Pack
1. Open BenchVault
2. Go to **Tools -> Transcription Settings**
3. Click **Download Transcription Pack**
4. Wait for the download to complete (~400 MB)
5. The pack installs automatically to the app's data directory:
   - Windows: `%LOCALAPPDATA%\BenchVault\transcription_pack\`
   - Linux: `~/.local/share/BenchVault/transcription_pack/`

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
3. Models are cached in the Whisper cache directory (`~/.cache/whisper/` on both platforms)

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
3. Add to PATH: System Properties -> Environment Variables -> Edit PATH -> Add `C:\ffmpeg\bin`
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

**Optional feature.** The AI Assistant lets users ask natural-language questions about their lab data. Requires an API key from Anthropic or OpenRouter and internet access.

### Step 1: Get an API Key
- **Anthropic**: https://console.anthropic.com/ → create account → generate API key
- **OpenRouter**: https://openrouter.ai/ → create account → generate API key

### Step 2: Configure in BenchVault
1. Login as Master user
2. Go to **Tools → Application Settings**
3. Select your provider (Anthropic or OpenRouter) and paste the API key
4. Set the **Monthly Budget per User** (default: $5)
5. Go to **AI Models** tab to manage models
6. Click **Save AI Settings**

The AI Assistant is available to all users via **Tools → AI Assistant** (Ctrl+Shift+A).

---

## Troubleshooting

### "Cannot connect to API server"

- Check the server URL on the login screen is correct
- For client workstations, use the server's API URL, not a PostgreSQL host/port
- Try `http://SERVER_IP:8000/api/status` in a web browser — you should see the BenchVault API status response
- If nothing responds, make sure the API server is running on the host PC/VPS and port 8000 is allowed through the firewall

### "PostgreSQL not found"

PostgreSQL is only required on the server/single-PC host. If this is a client workstation, click **Connect to Existing Server** in the Setup Wizard and enter the API server URL on the login screen.

### "Database does not exist" or local API fails to start

- On the server/single-PC host, rerun the Setup Wizard and verify the saved database configuration
- Confirm PostgreSQL is running and the database name matches the configured name
- For source-run deployments, verify `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` are set

### "Login Failed"

- Make sure you're using the correct password
- If this is a fresh install, register a new account on the Register tab
- First user is always Master

### "Only Master accounts can..."

Some features (email settings, password reset, application settings, AI model management) are restricted to Master users. The first registered user is always Master. A Master can promote other users in Application Settings.

---

## Silent Installation (IT Deployment)

### Desktop Installer
```cmd
BenchVault_Setup.exe /SILENT /DIR="C:\BenchVault"
```

### API Server (Windows Service)
```cmd
nssm install BenchVaultAPI "C:\Program Files\BenchVault\BenchVault_API_Server.exe"
nssm set BenchVaultAPI AppDirectory "C:\Program Files\BenchVault"
nssm set BenchVaultAPI AppEnvironmentExtra POSTGRES_HOST=localhost POSTGRES_PORT=5432 POSTGRES_DB=benchvault POSTGRES_USER=postgres POSTGRES_PASSWORD=your_password
nssm start BenchVaultAPI
```

### Register First User via API
```cmd
curl -X POST http://localhost:8000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"master\",\"password\":\"master123\",\"email\":\"admin@lab.com\",\"full_name\":\"Lab Admin\"}"
```

---

## Post-Installation Checklist

- [ ] PostgreSQL installed and running on the API/database host only
- [ ] Database created by the Setup Wizard or server provisioning script
- [ ] BenchVault installed with the single Windows installer
- [ ] API server auto-starts on localhost login or runs as a service on the host
- [ ] Master user registered
- [ ] Firewall rule for port 8000 configured if clients connect over the LAN
- [ ] Client workstations use **Connect to Existing Server** and the API URL

### Optional
- [ ] Email settings configured (User → Email Settings, Master only)
- [ ] Cloud backup configured (File → Cloud Backup)
- [ ] Voice transcription pack installed
- [ ] AI Assistant configured (Tools → Application Settings → AI Models tab)
