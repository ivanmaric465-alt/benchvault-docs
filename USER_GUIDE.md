---
layout: default
title: User Guide
---

# BenchVault v3.5.0 - User Guide

Daily usage guide for all BenchVault users.

---

## Getting Started

### Launching BenchVault
1. Double-click "BenchVault" desktop icon
2. Select your project (if multiple exist)
3. Login with username and password
4. Dashboard opens

### Dashboard Overview
- **Recent Experiments**: Last 5 experiments with quick access
- **Inventory Alerts**: Low stock items (red = critical, orange = low)
- **Statistics**: Total counts for experiments, samples, inventory
- **Calendar**: Monthly view with equipment reservations
- **Quick Actions**: Create new experiment

---

## Experiments Module

### Creating an Experiment
1. Click **Experiments** button (or Ctrl+N)
2. Click **New Experiment**
3. Fill in basic information:
   - **Title**: Descriptive name
   - **Date**: Auto-set to today

### Adding Parameters
1. Select parameter type from dropdown (Final Volume, Temperature, pH, etc.)
2. Click **Add Parameter**
3. Enter value in the editable cell (blue cells are editable)

**Tip**: Add "Final Volume" first - it's required for molarity calculations.

### Adding Reactants
1. Click **Add Reactant**
2. Select chemical from inventory list
3. Choose calculation type:
   | Type | Use Case |
   |------|----------|
   | Reactant (calculate mass) | Enter molarity, calculates mass to weigh |
   | Stock Solution | Enter target molarity + stock concentration |
   | Solvent (volume only) | For liquid solvents (mL only) |
   | Other (mass) | Direct mass entry |

4. Enter values, click OK
5. Calculated summary updates automatically

**Note**: If inventory module is disabled, Add Reactant is not available.

### Procedure Notes
- Use the **Procedure & Notes** tab
- Rich text editing supported
- Attach files (photos, PDFs, data files)

### Saving and Inventory
- Click **Save** to save experiment
- If auto-deduct is enabled, inventory quantities are automatically reduced
- Original amounts tracked - editing only deducts the difference

### Exporting
- **Export PDF**: Single experiment to PDF
- **Save as Template**: Save structure for reuse
- **Load Template**: Apply saved template

---

## Inventory Module

### Importing from Excel
Click **Import from Excel** to bulk-import inventory from a spreadsheet:
1. Click **Browse** and select your `.xlsx` file
2. Column headers are read automatically and mapped to BenchVault fields using keyword matching
3. Adjust any incorrect mappings via the dropdowns
4. Check the live preview (first 5 rows)
5. Click **Import**

After import, a summary shows any items imported with a `"?"` unit placeholder or zero quantities — edit those rows to correct the values.

**Don't have a template?** Click **Download Template** to get a pre-formatted `.xlsx` with the standard column headers.

### Adding Items Manually
1. Click **Inventory** button
2. Click **Add New Item**
3. Fill in:
   | Field | Description |
   |-------|-------------|
   | Name | Chemical name |
   | Supplier | Where purchased |
   | Quantity | Current amount |
   | Units | g, mL, L, kg, etc. |
   | Molar Mass | For calculations (g/mol) |
   | Location | Storage location |
   | Reorder Threshold | Alert level |

### Stock Alerts
Items are color-coded:
- **Red background**: Critical (< 10% of reorder threshold)
- **Orange background**: Low (< reorder threshold)
- **Normal**: Adequate stock

### Editing Items
- Double-click item or click **Edit**
- Update quantities after use
- Track order status for low items

### Auto-Refresh
Inventory auto-refreshes every 30 seconds to show changes from other users.

---

## Samples Module

### Creating Samples
1. Click **Samples** button
2. Click **Add Sample**
3. Fill in:
   - **Sample Name**: Unique identifier
   - **Parent Experiment**: Link to source experiment (optional)
   - **Tags**: For organization

### Adding Analyses
1. Select a sample
2. Click **Add Analysis**
3. Choose analysis type: NMR, HPLC, MS, IR, UV-Vis, etc.
4. Enter results
5. Attach data files (PDFs, images, raw data)

### Tag Inheritance
When a sample is linked to an experiment:
- Sample inherits experiment's tags automatically
- Changes to experiment tags sync to linked samples

---

## Equipment Scheduler

### Viewing Schedule
1. Click **Equipment Scheduler** button
2. Select equipment from dropdown
3. View weekly calendar with time slots

### Making Reservations
1. Click on desired time slot
2. Fill in:
   - **Date**: Selected date
   - **Start/End Time**: Duration
   - **Purpose**: What you're doing
3. Click **Save**

### Conflict Detection
- System prevents double-booking
- Overlapping reservations are blocked
- Warning shown if conflict exists

### Calendar Colors
Each equipment type has a unique color for easy identification.

---

## Statistics Module

### Activity Trends
- View experiments/samples created over time
- Filter by date range
- Switch between line and bar charts

### Top Users
- Rankings by activity
- Medals for top 3 contributors

### Database Health
- Database size
- Active connections
- Record counts

---

## Search and Filtering

### Quick Search
- Use search boxes in each module
- Searches across relevant fields

### Advanced Search
1. Click **Advanced Search** button
2. Set filters:
   - Date range
   - Tags (AND/OR/NOT logic)
   - Creator
   - Status
3. Click **Search**

### Tag Filtering
- **AND**: Must have all selected tags
- **OR**: Must have any selected tag
- **NOT**: Exclude items with selected tags

---

## File Attachments

### Supported Files
**Any file type can be attached** - select "All Files" in the file dialog.

Common categories with quick-select filters:
- **Raw Data (Instruments)**: XY, XRDML, RAW, DAT, ASC, DIF, CIF, SPC, SP, SPA, JDX, DX, FID, MZML, MZXML, MGF, CDF (XRD, NMR, MS, IR, HPLC, etc.)
- **Data**: CSV, XLSX, XLS, TXT, XML, JSON, TSV
- **Images**: JPG, PNG, GIF, BMP, TIF/TIFF, WebP, ICO, SVG
- **Documents**: PDF, DOC, DOCX, ODT, ODP, ODS, ODC, ODG, RTF, PPT, PPTX, XPS
- **Audio**: MP3, WAV, M4A, OGG, FLAC, AAC (for voice recordings)
- **Video**: MP4, AVI, MOV, MKV, WMV, WebM
- **Archives**: ZIP, RAR, 7Z, TAR, GZ

**Tip**: Files with non-standard extensions (e.g., instrument-specific formats) work fine - just select "All Files (*.*)" in the dialog.

### Attaching Files
1. In experiment/sample/analysis dialog
2. Click **Attach File** or drag-and-drop
3. File is copied to `experiment_files` folder

### Viewing Files
- Double-click to open with default application
- Right-click for options (open, delete)

---

## Voice Transcription

**Requires Whisper AI** - see INSTALLATION_GUIDE.md for setup.

### Transcribing Audio
1. Open experiment with audio file attached
2. Select the audio file
3. Click **Transcribe**
4. Wait for processing (first time may be slow)
5. Choose action:
   - **Insert into Notes**: Add to procedure notes
   - **Copy to Clipboard**: Paste elsewhere

### Model Selection
Go to **Tools -> Transcription Settings** to:
- Download different models
- Select active model
- View model details

---

## AI Assistant

**Requires Claude API key** — ask your Master user to configure it in Application Settings.

The AI Assistant lets you ask questions about your lab data using natural language. It can search experiments, inventory, samples, equipment schedules, and even read text-based analysis files.

### Opening AI Assistant
- **Tools -> AI Assistant** or press **Ctrl+Shift+A**

### Choosing a Model
Select from the dropdown at the top of the chat:
| Model | Best For | Cost |
|-------|----------|------|
| Haiku (default) | Quick questions, simple lookups | Cheapest |
| Sonnet | Detailed analysis, longer responses | Moderate |
| Opus | Complex reasoning, multi-step queries | Most expensive |

**Tip**: Haiku is sufficient for most day-to-day queries. Switch to Sonnet or Opus for complex questions.

### What You Can Ask
- "How many experiments did I create this month?"
- "Show me all inventory items with less than 10 units"
- "What samples are linked to experiment #42?"
- "What equipment reservations are scheduled for next week?"
- "Summarize recent lab activity"
- "Which analyses contain electrochemistry data?"

### Token Budget
Each user has a monthly token budget (set by Master user, default $5/month). The current usage is shown in the chat window. When the budget is reached, the assistant is unavailable until the next month.

### Limitations
- **Read-only**: The AI cannot modify any data — it can only search and read
- **Text files only**: Can read CSV, TXT, JSON, XML, and similar text-based attachments (not binary files like images or PDFs)
- **No external access**: The AI only sees your BenchVault database, not the internet

---

## Keyboard Shortcuts

### General
| Shortcut | Action |
|----------|--------|
| F1 | Show keyboard shortcuts help |
| F5 | Refresh dashboard |
| Ctrl+Shift+V | Toggle compact view |
| Ctrl+Shift+A | Open AI Assistant |
| Ctrl+F | Open advanced search |

### Navigation
| Shortcut | Action |
|----------|--------|
| Ctrl+N | Open experiments window |
| Ctrl+I | Open inventory |
| Ctrl+Shift+S | Open samples |
| Ctrl+E | Open equipment scheduler |
| Ctrl+T | Open statistics |

### In Dialogs
| Shortcut | Action |
|----------|--------|
| Esc | Close dialog |
| Enter | Confirm / OK |
| Tab | Next field |

---

## User Roles

### Regular User
- Create/edit own experiments, samples, inventory
- View all data (read-only for others' items)
- **Can only delete items you created**
- Reserve equipment
- Export data

### Master User (Administrator)
All regular permissions plus:
- Delete any item
- Reset user passwords
- Manage email settings
- View audit log
- Configure application settings
- Perform database maintenance

---

## Best Practices

### Data Entry
- Use descriptive experiment titles
- Update inventory immediately after use
- Link samples to parent experiments
- Use consistent tag naming

### Organization
- Create meaningful tags for categorization
- Use storage location consistently
- Reserve equipment in advance

### Data Safety
- Regular backups (ask Master user)
- Don't delete others' data

### Multi-User Etiquette
- Refresh data before making changes
- Communicate about equipment reservations
- Update inventory after using chemicals
- Use consistent naming conventions

---

## Troubleshooting

### "Cannot connect to database"
- Check if PostgreSQL service is running
- Verify network connection (for clients)
- Contact system administrator

### Data not refreshing
- Click refresh button or press F5
- Check network connection
- Auto-refresh runs every 30 seconds

### File attachment issues
- Check file isn't too large (< 50 MB recommended)
- Verify file isn't open in another application
- Check disk space

### Transcription not working
- Verify Whisper is installed (Tools -> Transcription Settings)
- Check FFmpeg is installed
- Try smaller model first

---

## Getting Help

- **In-App**: Help menu -> About
- **Documentation**: See other .md files in installation folder
- **Admin Tasks**: Contact your Master user
- **Technical Issues**: Contact IT department
