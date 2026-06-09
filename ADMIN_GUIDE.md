---
layout: default
title: Admin Guide
---

# BenchVault v4.1.1 - Administrator Guide

Guide for Master users: account management, backups, maintenance, and security.

---

## Account Management

### Creating User Accounts
Users self-register on the login screen:
1. Click "Register"
2. Enter username, password, full name, email
3. New accounts are **Regular** role by default

**Note**: First registered user becomes Master automatically.

### Resetting User Passwords

#### From Application
1. Go to **User menu -> Manage Users**
2. Select user
3. Click **Reset Password**
4. Temporary password is generated
5. Give password to user
6. User must change password on next login

#### Emergency Reset (Master Account Locked Out)
Use the **Password Reset Utility**:

1. Open Start Menu -> BenchVault -> Password Reset Utility
2. Or run from command line:
   ```cmd
   cd "C:\Program Files\BenchVault"
   BenchVault_Password_Reset.exe
   ```
3. Enter database connection details (auto-detected from config)
4. Select Master user to reset
5. Choose to generate or enter new password
6. User will be prompted to change on next login

### Changing User Roles
Currently roles are set at registration:
- First user = Master
- Subsequent users = Regular

To change a user's role, update directly in database:
```sql
UPDATE Users SET Role = 'Master' WHERE Username = 'username';
```

---

## Application Settings

Access: **Tools -> Application Settings** (Master only)

### Inventory Module
- **Enable Inventory Module**: Show/hide inventory button
- **Auto-deduct inventory**: Automatically reduce stock when creating experiments

**Note**: When inventory is disabled, Add Reactant in experiments is also disabled.

### AI Assistant
- **Anthropic (Claude)**: Select provider and enter your Anthropic API key (https://console.anthropic.com/)
- **OpenRouter**: Toggle provider to OpenRouter and enter an OpenRouter API key (https://openrouter.ai/)
  - The key is encrypted (Fernet) before being stored in the database
  - Alternatively, set `ANTHROPIC_API_KEY` or `OPENROUTER_API_KEY` environment variables (takes priority over DB key)
- **Monthly Budget per User**: Set maximum spending per user per month (default: $5)
  - Budget is tracked automatically based on token usage
  - Users are blocked from using the assistant when their budget is reached
  - Resets at the start of each calendar month
- **AI Model Management**: Models are stored in the `AIModels` database table
  - Default models (Haiku, Sonnet, Opus) are auto-seeded on first run
  - Master users can add, edit, delete, and reorder models in the AI Models tab
  - Supports both Anthropic and OpenRouter model IDs

### Dashboard
- **Show Recent Activities**: Toggle activity feed visibility

Changes require application restart to take full effect.

---

## Backup and Restore

### Server-side Backup

The desktop connects through the API and no longer performs raw PostgreSQL backup/restore operations locally.

#### Creating Backup
1. Go to **File -> Cloud Backup**
2. Configure the cloud provider credentials
3. Click **Backup Now**
4. The API server creates the database backup and uploads it to the configured provider

#### Restoring Backup
Restore operations must be performed on the API server using server-side tooling so the database and attachment folders are restored consistently.

**Recommended**: Backup weekly or before major changes.

**Warning**: Restore overwrites current data. Create a backup first!

### Cloud Backup

#### Supported Providers
| Provider | Configuration |
|----------|--------------|
| Koofr | Email + App Password (generate in account settings) |
| Nextcloud | Server URL + username + password |
| pCloud | Email + password |
| Box | Email + password |
| WebDAV | Full URL + username + password |

#### Setup
1. Go to **File -> Cloud Backup**
2. Select provider
3. Enter credentials
4. Set remote folder (default: `BenchVault/backups`)
5. Click **Test Connection**
6. Click **Save Configuration**

#### Manual Backup
- Click **Backup Now** in Cloud Backup dialog

#### Checking Backup Status
- **Server -> Server Info** shows API connection details and backup status when available

### Backup Best Practices
- Schedule regular backups (weekly minimum)
- Store backups off-site (cloud backup)
- Test restores periodically
- Keep multiple backup generations
- Document restore procedures for team

---

## Database Maintenance

### Audit Log Cleanup
The audit log grows over time. Clean up old records:

1. Go to **Tools -> Database Maintenance** (Master only)
2. View audit log statistics
3. Click **Clean Up Old Records**
4. Enter days to keep (default: 365)
5. Confirm deletion

**Recommendation**: Keep at least 1 year for compliance.

### Orphan File Cleanup
Files may remain on disk after being deleted from the app (e.g., interrupted deletions, manual testing). Clean them up:

1. Go to **Tools -> Database Maintenance** (Master only)
2. Click **Clean Up Orphan Files**
3. Review the count and size of orphan files found
4. Confirm deletion

This scans `experiment_files/` and `analysis_files/` directories for files not referenced in the database.

### Viewing Audit Log
1. Go to **Tools -> View Audit Log** (Master only)
2. Use filters:
   - Date range
   - Action type (CREATE, UPDATE, DELETE)
   - Entity type (Experiment, Sample, Inventory, etc.)
   - User
3. Click **Apply Filters**
4. Export to CSV for compliance records

### What's Logged
| Action | Examples |
|--------|----------|
| CREATE | New user registered, experiment created |
| UPDATE | Password changed, item modified |
| DELETE | Experiment deleted, sample removed |

### Database Statistics
View in **Statistics** module:
- Database size
- Active connections
- Table record counts

---

## Email Notifications

### Setup
1. Go to **Settings -> Email Settings** (Master only)
2. Configure SMTP:
   | Field | Example (Gmail) |
   |-------|-----------------|
   | SMTP Server | smtp.gmail.com |
   | Port | 587 |
   | Sender Email | lab@example.com |
   | Password | App password (not regular password) |
   | Use TLS | Yes |

**Gmail Note**: Use App Passwords, not your regular password.
Generate at: Google Account -> Security -> App Passwords

### Notification Types
- **Equipment Reservations**: Email when equipment is reserved
- **Low Stock Alerts**: Email when inventory falls below threshold
- **Weekly Summary**: Optional digest of activity

### Testing
Click **Send Test Email** to verify configuration.

---

## Server Management

The desktop uses a single API connection at a time. To connect to another server, log out or restart the desktop and enter the new API URL on the login screen.

### Server Info
**Server -> Server Info** shows:
- API server URL
- Record counts
- Database size
- Cloud backup status
- Local API process status

---

## Security Best Practices

### Password Policies
- Require minimum 6 characters
- Users prompted to change temporary passwords
- Regular password changes recommended

### Access Control
- Only give Master role to administrators
- Regular users can only delete their own items
- Review audit log for suspicious activity

### Data Protection
- Regular backups (local + cloud)
- Restrict PostgreSQL network access
- Use strong PostgreSQL password
- Keep firewall enabled

### Audit Trail
- All deletions are logged
- All user changes are logged
- Export audit log for compliance
- Retain logs per your organization's policy

---

## Troubleshooting (Admin)

### User Can't Login
1. Verify account exists (Manage Users)
2. Reset password if needed
3. Check account not locked

### Master Account Locked Out
Use Password Reset Utility (see Account Management section)

### Database Connection Issues
1. Check PostgreSQL service running
2. Verify credentials in project config
3. Check network connectivity
4. Review PostgreSQL logs

### Performance Issues
- Clean up old audit logs
- Archive old experiments if needed
- Check database size (Statistics)
- Consider increasing connection pool (advanced)

### Backup Fails
- Check disk space
- Verify PostgreSQL user has backup permissions
- Check network (for cloud backup)
- Review error message for specifics

---

## Advanced: Running from Source

For developers or advanced users running from Python source:

### Environment Variables
```cmd
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432
set POSTGRES_DB=lab_notebook
set POSTGRES_USER=postgres
set POSTGRES_PASSWORD=your_password
python main.py
```

### Dependencies
```cmd
pip install -r requirements.txt
```

For transcription:
```cmd
pip install -r requirements-transcription.txt
```

### API Server
```cmd
python api_server.py
```
Runs on port 8000, API docs at `/docs`.

---

## Quick Reference

### Menu Locations
| Task | Location |
|------|----------|
| Cloud backup | File -> Cloud Backup |
| Change API server | Server -> Change Server on Next Login |
| Application settings | Tools -> Application Settings |
| AI Assistant | Tools -> AI Assistant (Ctrl+Shift+A) |
| Database maintenance | Tools -> Database Maintenance |
| View audit log | Tools -> View Audit Log |
| Email settings | Settings -> Email Settings |
| Manage users | User menu -> Manage Users |
| Reset password | User menu -> Manage Users -> Reset Password |

### File Locations

| Item | Windows | Linux |
|------|---------|-------|
| Project config | `%LOCALAPPDATA%\BenchVault\projects.json` | `~/.config/benchvault/projects.json` |
| Server config | `%LOCALAPPDATA%\BenchVault\server_config.json` | `~/.config/benchvault/server_config.json` |
| Cloud backup config | `%LOCALAPPDATA%\BenchVault\cloud_backup_config.json` | `~/.config/benchvault/cloud_backup_config.json` |
| Attachments (experiments) | `%LOCALAPPDATA%\BenchVault\experiment_files\` | `~/.local/share/BenchVault/experiment_files/` |
| Attachments (analyses) | `%LOCALAPPDATA%\BenchVault\analysis_files\` | `~/.local/share/BenchVault/analysis_files/` |
| Local backups | `%LOCALAPPDATA%\BenchVault\backups\` | `~/.local/share/BenchVault/backups/` |
| Encryption key | `%LOCALAPPDATA%\BenchVault\encryption.key` | `~/.config/benchvault/encryption.key` |
| Whisper models | `~/.cache/whisper/` | `~/.cache/whisper/` |
| Transcription pack | `%LOCALAPPDATA%\BenchVault\transcription_pack\` | `~/.local/share/BenchVault/transcription_pack/` |

### Emergency Contacts
Document your organization's:
- IT support contact
- Database administrator
- Backup restoration procedures
- Escalation path
