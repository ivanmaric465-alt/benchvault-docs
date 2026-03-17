---
layout: default
title: API Setup Guide
---

# BenchVault v3.1.0 - Mobile App & API Setup Guide

Complete guide for setting up the mobile app and API server.

---

## Overview

BenchVault includes a Flutter mobile app that connects to the desktop app's API server for:
- **Experiments**: Browse, view details, add photos/voice recordings
- **Inventory**: Search chemicals, scan QR codes
- **Equipment**: View and create reservations
- **Samples**: Browse and search samples

**Authentication**: JWT-based login using BenchVault credentials

---

## Quick Start (Recommended)

### Option 1: Start API from Desktop App (Easiest)

1. Launch BenchVault desktop app
2. User menu → Start API Server
3. Note the API URL shown (e.g., `http://192.168.1.100:8000`)
4. On mobile app login screen, expand "API Server Settings"
5. Enter the API URL
6. Login with your BenchVault credentials

**Done!** The desktop app manages the API server for you - no environment variables needed.

---

## Option 2: Run API Server Standalone

For advanced users who want to run the API server independently.

### Prerequisites

1. PostgreSQL 16 installed and running
2. Python 3.8+ installed
3. BenchVault database exists (created via desktop app or manually)

### Environment Variables Setup

**Required environment variables:**

```bash
API_DB_HOST=localhost       # Database server address
API_DB_PORT=5432           # PostgreSQL port
API_DB_NAME=lab_notebook   # Your database name
API_DB_USER=postgres       # PostgreSQL username
API_DB_PASSWORD=your_pass  # PostgreSQL password
JWT_SECRET_KEY=random-32-char-secret  # For JWT tokens
```

### Setting Environment Variables (Windows)

**Method 1: System Variables (Permanent)**

1. Press Win+R, type `sysdm.cpl`, press Enter
2. Advanced tab → Environment Variables
3. Under "System variables", click "New"
4. Add each variable:
   ```
   Variable name: API_DB_HOST
   Variable value: localhost
   ```
5. Repeat for all 6 variables
6. Click OK, restart Command Prompt

**Method 2: Command Line (Session Only)**

```cmd
set API_DB_HOST=localhost
set API_DB_PORT=5432
set API_DB_NAME=lab_notebook
set API_DB_USER=postgres
set API_DB_PASSWORD=your_password
set JWT_SECRET_KEY=your-secret-key-here
python api_server.py
```

### Running the Standalone API Server

**From Source:**
```cmd
cd C:\Users\YourName\eln_project
pip install -r requirements.txt
python api_server.py
```

**From Compiled Executable:**
```cmd
cd "C:\Program Files\BenchVault"
BenchVault_API_Server.exe
```

Server starts on `http://0.0.0.0:8000` by default.

---

## Network Access Methods

### Method 1: Local Network (WiFi)

**Best for**: Lab testing, same network as desktop

1. Start API server (desktop app or standalone)
2. Find server IP address:
   ```cmd
   ipconfig
   ```
   Look for IPv4 Address (e.g., `192.168.1.100`)
3. On mobile app, enter API URL: `http://192.168.1.100:8000`
4. Ensure mobile device on same WiFi network

**Firewall**: Allow port 8000:
```cmd
netsh advfirewall firewall add rule name="BenchVault API" dir=in action=allow protocol=TCP localport=8000
```

### Method 2: ngrok (Internet Access)

**Best for**: Remote access, testing from anywhere

1. Download ngrok: https://ngrok.com/download
2. Extract and run:
   ```cmd
   ngrok http 8000
   ```
3. Note the HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. On mobile app, enter this URL
5. Works from anywhere with internet

**Pros**: No firewall/router config needed
**Cons**: URL changes each restart (unless using paid ngrok)

### Method 3: Port Forwarding (Internet Access)

**Best for**: Production deployment, permanent access

1. Configure router port forwarding:
   - External port: 8000
   - Internal IP: Your server IP
   - Internal port: 8000
2. Find public IP: https://whatismyip.com
3. On mobile app, enter: `http://your-public-ip:8000`

**Security**: Use HTTPS in production (reverse proxy with SSL)

---

## Mobile App Configuration

### Android APK Installation

1. Download `BenchVault_Mobile.apk` to your phone
2. Enable "Install from Unknown Sources" in Settings
3. Open the APK file
4. Click "Install"

### First Launch

1. Open BenchVault mobile app
2. On login screen, tap the settings icon
3. Expand "API Server Settings"
4. Enter API URL:
   - Local network: `http://192.168.1.100:8000`
   - ngrok: `https://your-subdomain.ngrok.io`
   - Public IP: `http://your-public-ip:8000`
5. Login with BenchVault credentials

**Note**: URL is saved - you only configure it once.

### Permissions

Mobile app requests:
- **Camera**: For QR scanning and photo capture
- **Microphone**: For voice recording
- **Storage**: For saving photos/audio

Grant all permissions for full functionality.

---

## API Endpoints Reference

### Authentication

**POST /api/v1/auth/login**
- Body: `{"username": "user", "password": "pass"}`
- Returns: JWT access token
- Mobile app handles this automatically

### Experiments

**GET /api/v1/experiments**
- List all experiments
- Query params: `?limit=20&offset=0`

**GET /api/v1/experiments/{id}**
- Get experiment details including reactants

**POST /api/v1/experiments/{id}/photo**
- Upload photo to experiment
- Multipart form data: `file`

**POST /api/v1/experiments/{id}/voice**
- Upload voice recording
- Multipart form data: `file`

### Inventory

**GET /api/v1/inventory**
- List all inventory items

**GET /api/v1/inventory/search?q=acetone**
- Search inventory by name

**GET /api/v1/inventory/{id}**
- Get inventory item details

### Samples

**GET /api/v1/samples**
- List all samples

**GET /api/v1/samples/{id}**
- Get sample details with analyses

### Equipment

**GET /api/v1/reservations/today**
- Get today's equipment reservations

**POST /api/v1/reservations**
- Create new reservation

### Interactive API Docs

Visit `http://your-server:8000/docs` for:
- Full API documentation
- Try-it-out interface
- Request/response schemas
- Authentication testing

---

## Troubleshooting

### Mobile App Can't Connect

**Error**: "Check your connection and API URL"

**Solutions**:
1. Verify API server is running
2. Check API URL is correct (include `http://` or `https://`)
3. Test URL in phone browser - should show `{"message":"BenchVault API Server"}`
4. If local network: Ensure phone on same WiFi
5. If ngrok: Verify ngrok tunnel is active
6. Check firewall allows port 8000

### Authentication Fails

**Error**: "Invalid credentials" or 401

**Solutions**:
1. Verify username/password are correct (case-sensitive)
2. Check user exists in desktop app (User menu → Manage Users)
3. Ensure database is same one desktop app uses
4. Check API server logs for errors

### Photo/Voice Upload Fails

**Error**: 413 Payload Too Large or timeout

**Solutions**:
1. Reduce photo quality in mobile app settings
2. Limit voice recordings to <2 minutes
3. Check network connection is stable
4. Increase timeout in api_service.dart (developers)

### API Server Won't Start

**Error**: "Address already in use" or "Port 8000 in use"

**Solutions**:
1. Check if another API server instance is running
2. Kill process using port 8000:
   ```cmd
   netstat -ano | findstr :8000
   taskkill /PID <process_id> /F
   ```
3. Or use different port:
   ```cmd
   set API_PORT=8001
   python api_server.py
   ```

### Environment Variables Not Working

**Error**: "Database does not exist" or connection errors

**Solutions**:
1. Verify variables are set:
   ```cmd
   echo %API_DB_NAME%
   echo %API_DB_PASSWORD%
   ```
2. Restart Command Prompt after setting variables
3. Check database name matches exactly (case-sensitive)
4. Test PostgreSQL connection manually:
   ```cmd
   psql -h localhost -U postgres -d lab_notebook
   ```

---

## Development Tips

### Testing API Endpoints

**Using curl:**
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"test\",\"password\":\"test123\"}"

# Get experiments (with token)
curl http://localhost:8000/api/v1/experiments \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Using Postman/Insomnia:**
1. Import OpenAPI spec from `/docs`
2. Set up authentication with JWT token
3. Test all endpoints interactively

### Auto-Reload for Development

```cmd
# API server restarts on code changes
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

### Viewing Logs

API server logs to console. For production, redirect to file:
```cmd
python api_server.py > api.log 2>&1
```

---

## Security Best Practices

### Production Deployment

1. **Change JWT Secret**:
   ```cmd
   setx JWT_SECRET_KEY "$(openssl rand -hex 32)"
   ```

2. **Use HTTPS**: Set up reverse proxy with SSL (nginx/Apache)

3. **Restrict CORS**: Update CORS settings in api_server.py

4. **Strong Passwords**: Enforce strong BenchVault user passwords

5. **Firewall**: Only allow necessary IPs to access port 8000

### Mobile App Security

- JWT tokens expire after 60 minutes (default)
- Tokens stored in secure storage (flutter_secure_storage)
- HTTPS recommended for production
- Validate SSL certificates (don't allow self-signed in production)

---

## Environment Variables Reference

### Desktop App Launches API

When starting API from desktop app User menu:
- ✓ Automatically sets `API_DB_*` variables
- ✓ Uses current project's database
- ✓ Manages process lifecycle
- ✗ **No manual environment variable setup needed**

### Standalone API Server

When running `python api_server.py` or `BenchVault_API_Server.exe`:
- ✓ Must set environment variables manually
- ✓ Checks `API_DB_*` variables first
- ✓ Falls back to `POSTGRES_*` variables
- ✓ Uses defaults if neither set

**Variable Priority:**
1. `API_DB_*` (highest priority)
2. `POSTGRES_*` (fallback)
3. Defaults: `localhost:5432, lab_notebook, postgres/postgres` (lowest)

---

## Support

For installation help, see **INSTALLATION_GUIDE.md**.

For IT deployment, see **DEPLOYMENT_GUIDE.md**.

For end users, see **USER_GUIDE.md**.

---

**Last Updated:** 2026-03-11
**Version:** 3.1.0
