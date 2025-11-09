# CNC DXF Converter

Professional web-based tool for converting images to DXF files for CNC plasma cutting machines.

## Overview

This application converts bitmap images (JPG, PNG, BMP) into DXF vector files containing LINE entities suitable for CNC plasma cutters. The system uses **Potrace** for vectorization and provides a modern web interface for managing conversions.

## Key Features

- **Image to DXF Conversion**: Convert raster images to vector DXF files
- **Adjustable Threshold**: Control edge detection sensitivity (0-100%)
- **CNC-Compatible Output**: Generates LINE entities (not SPLINES) for CNC compatibility
- **Conversion History**: Track and manage all conversions
- **Thumbnail Previews**: Visual preview of converted images
- **Download Management**: Easy DXF file downloads
- **RESTful API**: Backend API for integration

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: Database ORM
- **Pillow (PIL)**: Image preprocessing
- **ezdxf**: DXF file manipulation
- **Potrace**: Bitmap to vector conversion

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **React Dropzone**: Drag-and-drop file upload
- **TailwindCSS**: Styling (via CDN)

## Architecture

```
┌─────────────────┐
│  React Frontend │ (Port 5173)
│  - File Upload  │
│  - History View │
│  - Downloads    │
└────────┬────────┘
         │ HTTP/REST
┌────────┴────────┐
│  FastAPI Backend│ (Port 8000)
│  - API Endpoints│
│  - Conversion   │
│  - Database     │
└────────┬────────┘
         │
    ┌────┴─────┐
    │  Pillow  │ ──→ Grayscale + Threshold
    └────┬─────┘
         │
    ┌────┴─────┐
    │ Potrace  │ ──→ DXF (POLYLINES)
    └──────────┘
```

## Conversion Process

1. **Upload**: User uploads an image (JPG, PNG, BMP)
2. **Preprocessing**:
   - Convert to grayscale using Pillow
   - Apply threshold to create black/white bitmap
   - Save as PBM format
3. **Vectorization**:
   - Potrace traces bitmap to vector paths
   - Output DXF generating POLYLINES, then convert to LINEs
4. **Analysis**:
   - ezdxf analyzes DXF structure
   - Verifies entity types (no SPLINES)
   - Extracts metadata
5. **Storage**: Save to database with thumbnail
6. **Download**: User downloads DXF file for CNC

## Threshold Parameter

The threshold slider (0-100%) controls edge detection:

- **Low (20-40%)**: Captures more detail, including subtle edges
  - Use for: Detailed logos, complex artwork
  - Risk: May capture unwanted background noise

- **Medium (50%)**: Balanced approach (default)
  - Use for: General purpose, most images
  - Good starting point for testing

- **High (60-80%)**: Only strong contrasts
  - Use for: Bold text, simple shapes, silhouettes
  - Risk: May lose fine details

**Tip**: Try multiple threshold values on the same image to find the best cutting pattern for your needs.

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Scoop package manager (Windows)

### Install Dependencies

1. **Install Potrace**:
```bash
scoop install potrace
```

2. **Setup Backend**:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. **Setup Frontend**:
```bash
cd frontend
npm install
```

### Run Application

**Terminal 1 - Backend**:
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Open**: http://localhost:5173

## API Documentation

### Endpoints

#### `POST /api/convert`
Convert image to DXF
- **Body**: `multipart/form-data`
  - `file`: Image file (JPG, PNG, BMP)
  - `threshold`: Integer (0-100)
- **Response**: Conversion details with download URL

#### `GET /api/history`
Get conversion history
- **Query**: `search`, `page`, `limit`
- **Response**: Paginated conversion list

#### `GET /api/download/{conversion_id}`
Download DXF file
- **Response**: DXF file attachment

#### `GET /api/thumbnail/{conversion_id}`
Get thumbnail image
- **Response**: JPEG thumbnail

#### `DELETE /api/delete/{conversion_id}`
Delete conversion and files
- **Response**: Success message

#### `GET /api/stats`
Get application statistics
- **Response**: Total conversions, storage usage

## Project Structure

```
CNC-DXF/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── converter.py      # DXF conversion logic
│   ├── models.py         # Database models
│   ├── database.py       # Database configuration
│   ├── validator.py      # File validation
│   ├── requirements.txt  # Python dependencies
│   └── data/            # Upload/output storage
│       ├── uploads/     # Uploaded images
│       └── outputs/     # Generated DXF files
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main application
│   │   └── main.jsx     # Entry point
│   ├── index.html       # HTML template
│   ├── package.json     # Node dependencies
│   └── vite.config.js   # Vite configuration
└── README.md            # This file
```

## Troubleshooting

### Potrace Not Found
- Ensure Potrace is installed: `scoop install potrace`
- Verify installation: `potrace --version`
- Check PATH includes Scoop shims directory

### Backend Won't Start
- Check Python version: `python --version` (need 3.9+)
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Won't Start
- Check Node.js version: `node --version` (need 16+)
- Clear cache: `rm -rf node_modules && npm install`
- Check port 5173 is available

### Conversion Fails
- Verify Potrace is installed and accessible
- Check image format is supported (JPG, PNG, BMP)
- Review backend logs for detailed error messages
- Try different threshold values

## Development

### Backend Development
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload  # Auto-reload on changes
```

### Frontend Development
```bash
cd frontend
npm run dev  # Hot module replacement enabled
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup instructions including:
- Environment configuration
- Reverse proxy setup (Nginx)
- Process management (PM2, systemd)
- Security hardening
- Backup strategies

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/Raslemchr31/CNC-DXF/issues
- Email: support@example.com

## Credits

- **Potrace**: Peter Selinger (http://potrace.sourceforge.net/)
- **FastAPI**: Sebastián Ramírez (https://fastapi.tiangolo.com/)
- **React**: Meta (https://react.dev/)
