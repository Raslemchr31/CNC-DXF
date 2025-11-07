# CNC DXF Converter - Installation Guide

Complete step-by-step installation instructions for Windows 11.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Install Prerequisites](#install-prerequisites)
3. [Clone Repository](#clone-repository)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for application + dependencies
- **Internet**: Required for initial setup

### Software Requirements
- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher
- **Git**: For cloning repository
- **Scoop**: Package manager for Windows

---

## Install Prerequisites

### Step 1: Install Scoop Package Manager

Scoop simplifies software installation on Windows.

1. **Open PowerShell** (as regular user, NOT administrator):
   - Press `Win + X`
   - Select "Windows PowerShell" or "Terminal"

2. **Run installation command**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

3. **Verify installation**:
```powershell
scoop --version
```

Expected output: `Current Scoop version: v0.x.x`

### Step 2: Install Git

```powershell
scoop install git
```

Verify:
```powershell
git --version
```

### Step 3: Install Python

```powershell
scoop install python
```

Verify:
```powershell
python --version
```

Expected: `Python 3.9.x` or higher

### Step 4: Install Node.js

```powershell
scoop install nodejs
```

Verify:
```powershell
node --version
npm --version
```

### Step 5: Install Potrace (CRITICAL)

Potrace is required for DXF conversion.

```powershell
scoop install potrace
```

Verify:
```powershell
potrace --version
```

Expected output: `potrace 1.16`

---

## Clone Repository

Open a new PowerShell window (to ensure PATH is updated):

```powershell
# Navigate to desired installation directory
cd C:\Users\YourUsername\Desktop

# Clone repository
git clone https://github.com/Raslemchr31/CNC-DXF.git

# Navigate into directory
cd CNC-DXF
```

---

## Backend Setup

### Step 1: Create Virtual Environment

```powershell
cd backend
python -m venv venv
```

This creates an isolated Python environment.

### Step 2: Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

Your prompt should now show `(venv)` prefix.

### Step 3: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (database)
- Pillow (image processing)
- ezdxf (DXF manipulation)
- Other utilities

**Expected duration**: 1-2 minutes

### Step 4: Create Data Directories

```powershell
mkdir data
mkdir data/uploads
mkdir data/outputs
```

These directories store uploaded images and generated DXF files.

### Step 5: Verify Backend Installation

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
DXF Converter API started
Data directory: data/
Checking dependencies...
[OK] Potrace installed
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Press `Ctrl+C`** to stop the server (we'll restart it later).

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

Open a **NEW** PowerShell window:

```powershell
cd C:\Users\YourUsername\Desktop\CNC-DXF\frontend
```

### Step 2: Install Node Dependencies

```powershell
npm install
```

This installs:
- React 18
- Vite (build tool)
- Axios (HTTP client)
- React Dropzone (file upload)
- Other utilities

**Expected duration**: 2-3 minutes

### Step 3: Verify Frontend Installation

```powershell
npm run dev
```

**Expected output**:
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

**Press `Ctrl+C`** to stop the dev server.

---

## Running the Application

You need **TWO** terminal windows running simultaneously.

### Terminal 1: Start Backend

```powershell
cd C:\Users\YourUsername\Desktop\CNC-DXF\backend
.\venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Keep this window open**. You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Frontend

```powershell
cd C:\Users\YourUsername\Desktop\CNC-DXF\frontend
npm run dev
```

**Keep this window open**. You should see:
```
➜  Local:   http://localhost:5173/
```

### Access Application

Open your web browser and navigate to:

**http://localhost:5173**

You should see the CNC DXF Converter interface.

---

## Verification

### Test Conversion

1. **Prepare a test image**:
   - Use any JPG, PNG, or BMP image
   - Simple logo or text works best for first test

2. **Upload image**:
   - Drag and drop image onto upload area
   - OR click "Choose File" button

3. **Set threshold**:
   - Keep default (50%) for first test
   - Adjust as needed for your image

4. **Click "Convert to DXF"**

5. **Check results**:
   - Conversion should complete in 2-5 seconds
   - You should see thumbnail preview
   - File appears in conversion history

6. **Download DXF**:
   - Click download button
   - DXF file should download to your Downloads folder

7. **Verify DXF**:
   - Open DXF in CAD software (AutoCAD, LibreCAD, etc.)
   - Check that shapes are made of POLYLINES (not SPLINES)

### Check Backend Logs

In Terminal 1 (backend), you should see:
```
Converting image to bitmap (threshold=50%)...
Converting bitmap to DXF...
Analyzing DXF file...
Generating thumbnail...
INFO:     127.0.0.1:XXXXX - "POST /api/convert HTTP/1.1" 200 OK
```

### Test API Directly

Open browser to: **http://localhost:8000**

You should see:
```json
{
  "status": "ok",
  "message": "DXF Converter API is running"
}
```

---

## Troubleshooting

### Issue: "potrace: command not found"

**Cause**: Potrace not installed or not in PATH

**Solution**:
1. Install via Scoop: `scoop install potrace`
2. Close and reopen PowerShell
3. Verify: `potrace --version`
4. If still fails, restart computer

### Issue: "Python not found" or "pip not found"

**Cause**: Python not installed or PATH not updated

**Solution**:
1. Install via Scoop: `scoop install python`
2. Close and reopen PowerShell
3. Verify: `python --version`

### Issue: "npm: command not found"

**Cause**: Node.js not installed

**Solution**:
1. Install via Scoop: `scoop install nodejs`
2. Close and reopen PowerShell
3. Verify: `node --version` and `npm --version`

### Issue: "venv\Scripts\activate: cannot be loaded"

**Cause**: PowerShell execution policy

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Backend starts but conversions fail

**Cause**: Potrace not accessible or image format issue

**Solution 1 - Check Potrace**:
```powershell
where.exe potrace
```

Should show path like: `C:\Users\YourUsername\scoop\shims\potrace.exe`

**Solution 2 - Check Image Format**:
- Ensure image is JPG, PNG, or BMP
- Try different image if current one fails
- Check image isn't corrupted

### Issue: "Port 8000 already in use"

**Cause**: Another application using port 8000

**Solution 1 - Use different port**:
```powershell
uvicorn main:app --host 0.0.0.0 --port 8001
```

Update frontend API URL in `src/App.jsx`:
```javascript
const API_URL = 'http://localhost:8001/api';
```

**Solution 2 - Kill process on port 8000**:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Issue: "Port 5173 already in use"

**Cause**: Another Vite instance running

**Solution**:
```powershell
# Stop all node processes
taskkill /F /IM node.exe

# Restart frontend
npm run dev
```

### Issue: Slow conversion or timeout

**Cause**: Large image or complex details

**Solutions**:
- Resize image to smaller dimensions (max 2000x2000px)
- Increase threshold value (60-80%) for simpler output
- Use simpler images for testing

### Issue: DXF contains SPLINES instead of POLYLINES

**Cause**: Should NOT happen with this implementation

**Investigation**:
1. Check backend logs for warnings
2. Open DXF in text editor, search for "SPLINE"
3. Report issue with image sample

### Still Having Issues?

1. **Check all requirements**:
```powershell
python --version    # Should be 3.9+
node --version      # Should be 16+
npm --version       # Should be 8+
potrace --version   # Should be 1.16
git --version       # Any recent version
```

2. **Restart everything**:
   - Close all terminals
   - Restart computer
   - Follow installation steps again

3. **Check logs**:
   - Backend terminal shows detailed error messages
   - Frontend browser console (F12) shows client errors

4. **Clean reinstall**:
```powershell
# Backend
cd backend
rm -rf venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

---

## Next Steps

- Read [README.md](README.md) for usage instructions
- Experiment with different threshold values
- Test with various image types
- Integrate with your CNC workflow

## Support

For additional help:
- Check GitHub Issues: https://github.com/Raslemchr31/CNC-DXF/issues
- Review backend logs for detailed error messages
- Test with simple images first before complex ones
