# Quick Start Guide

Get the CNC DXF Converter running in 10 minutes.

## For Windows 11 Users

### Step 1: Install Scoop (2 minutes)

Open **PowerShell** (not as administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

### Step 2: Install Everything (3 minutes)

```powershell
scoop install git python nodejs potrace
```

Close and reopen PowerShell after installation.

### Step 3: Clone and Setup (5 minutes)

```powershell
# Clone repository
git clone https://github.com/Raslemchr31/CNC-DXF.git
cd CNC-DXF

# Setup backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Setup frontend (in same window)
cd frontend
npm install
cd ..
```

### Step 4: Run Application (30 seconds)

**Terminal 1** (Backend):
```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2** (Frontend - open a NEW PowerShell window):
```powershell
cd CNC-DXF/frontend
npm run dev
```

### Step 5: Use It!

Open browser to: **http://localhost:5173**

1. Drag and drop an image (JPG, PNG, BMP)
2. Adjust threshold slider (start at 50%)
3. Click "Convert to DXF"
4. Download your DXF file!

---

## Troubleshooting

**Issue**: Commands not found after install
- **Fix**: Close and reopen PowerShell

**Issue**: Port already in use
- **Fix Backend**: Use port 8001 instead:
  ```powershell
  uvicorn main:app --host 0.0.0.0 --port 8001
  ```
- **Fix Frontend**: Kill node and restart:
  ```powershell
  taskkill /F /IM node.exe
  npm run dev
  ```

**Issue**: Conversion fails
- **Fix**: Verify Potrace installed:
  ```powershell
  potrace --version
  ```
- Should show: `potrace 1.16`

---

## Need More Help?

- **Full Installation Guide**: See [INSTALLATION.md](INSTALLATION.md)
- **How to Use**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Technical Details**: See [README.md](README.md)

---

## What You Get

This application converts images to DXF files for CNC plasma cutting:

- **Input**: JPG, PNG, BMP images
- **Output**: DXF files with POLYLINES (CNC-compatible)
- **Features**:
  - Adjustable edge detection threshold
  - Conversion history with thumbnails
  - Easy download management
  - RESTful API for automation

Perfect for creating cutting files for:
- Company logos
- Custom signage
- Decorative metalwork
- Text and lettering
- Simple shapes and silhouettes
