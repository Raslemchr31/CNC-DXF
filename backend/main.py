from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import json
import shutil
import uuid
import subprocess
from datetime import datetime

from database import get_db, engine
from models import Base, Conversion
from converter import DXFConverter
from validator import FileValidator

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="DXF Converter API",
    description="Convert images to DXF files for CNC cutting",
    version="1.0.0"
)

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize converter
converter = DXFConverter()

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
def root():
    """Health check"""
    return {"status": "ok", "message": "DXF Converter API is running"}

@app.post("/api/convert")
async def convert_image(
    file: UploadFile = File(...),
    threshold: int = Form(50),
    db: Session = Depends(get_db)
):
    """
    Upload and convert an image to DXF

    Args:
        file: Image file (JPG, PNG, BMP)
        threshold: Edge detection threshold (0-100)

    Returns:
        Conversion details with download URL
    """
    # Validate threshold
    if not 0 <= threshold <= 100:
        raise HTTPException(status_code=400, detail="Threshold must be between 0 and 100")

    # Sanitize filename
    safe_filename = FileValidator.sanitize_filename(file.filename)

    # Save uploaded file temporarily
    file_id = str(uuid.uuid4())
    temp_image_path = f"data/uploads/{file_id}_{safe_filename}"

    try:
        # Save uploaded file
        with open(temp_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Validate image
        validation = FileValidator.validate_image(temp_image_path)
        if not validation["valid"]:
            os.remove(temp_image_path)
            raise HTTPException(status_code=400, detail=validation["error"])

        # Convert to DXF
        result = converter.convert_image_to_dxf(
            image_path=temp_image_path,
            threshold=threshold
        )

        # Create database record
        conversion = Conversion(
            filename=os.path.splitext(safe_filename)[0],
            original_filename=safe_filename,
            image_path=temp_image_path,
            dxf_path=result["dxf_path"],
            thumbnail_path=result.get("thumbnail_path"),
            threshold=threshold,
            file_size=result["metadata"]["file_size"],
            conversion_metadata=json.dumps(result["metadata"]),
            status="completed"
        )

        db.add(conversion)
        db.commit()
        db.refresh(conversion)

        return {
            "success": True,
            "message": "Conversion successful",
            "data": conversion.to_dict()
        }

    except Exception as e:
        # Clean up on error
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

        # Log error
        print(f"Conversion error: {str(e)}")

        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.get("/api/history")
def get_history(
    search: str = "",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get conversion history with optional search

    Args:
        search: Search term for filename
        page: Page number (1-indexed)
        limit: Items per page

    Returns:
        List of conversions with pagination
    """
    # Build query
    query = db.query(Conversion)

    # Apply search filter
    if search:
        query = query.filter(Conversion.filename.contains(search))

    # Count total
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    conversions = query.order_by(Conversion.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "success": True,
        "data": [c.to_dict() for c in conversions],
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

@app.get("/api/download/{conversion_id}")
def download_dxf(conversion_id: str, db: Session = Depends(get_db)):
    """
    Download DXF file

    Args:
        conversion_id: Conversion UUID

    Returns:
        DXF file
    """
    conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()

    if not conversion:
        raise HTTPException(status_code=404, detail="Conversion not found")

    if not os.path.exists(conversion.dxf_path):
        raise HTTPException(status_code=404, detail="DXF file not found")

    return FileResponse(
        path=conversion.dxf_path,
        filename=f"{conversion.filename}.dxf",
        media_type="application/dxf"
    )

@app.get("/api/thumbnail/{conversion_id}")
def get_thumbnail(conversion_id: str, db: Session = Depends(get_db)):
    """
    Get thumbnail image

    Args:
        conversion_id: Conversion UUID

    Returns:
        Thumbnail image
    """
    conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()

    if not conversion or not conversion.thumbnail_path:
        raise HTTPException(status_code=404, detail="Thumbnail not found")

    if not os.path.exists(conversion.thumbnail_path):
        raise HTTPException(status_code=404, detail="Thumbnail file not found")

    return FileResponse(
        path=conversion.thumbnail_path,
        media_type="image/jpeg"
    )

@app.delete("/api/delete/{conversion_id}")
def delete_conversion(conversion_id: str, db: Session = Depends(get_db)):
    """
    Delete a conversion and its files

    Args:
        conversion_id: Conversion UUID

    Returns:
        Success message
    """
    conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()

    if not conversion:
        raise HTTPException(status_code=404, detail="Conversion not found")

    # Delete files
    for path in [conversion.image_path, conversion.dxf_path, conversion.thumbnail_path]:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Failed to delete {path}: {e}")

    # Delete database record
    db.delete(conversion)
    db.commit()

    return {"success": True, "message": "Conversion deleted"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Get application statistics

    Returns:
        Stats about conversions
    """
    total_conversions = db.query(Conversion).count()

    # Calculate total storage
    total_storage = 0
    for conversion in db.query(Conversion).all():
        if conversion.file_size:
            total_storage += conversion.file_size

    return {
        "total_conversions": total_conversions,
        "total_storage_bytes": total_storage,
        "total_storage_mb": round(total_storage / (1024 * 1024), 2)
    }

# ============================================
# STARTUP/SHUTDOWN
# ============================================

@app.on_event("startup")
async def startup():
    print("DXF Converter API started")
    print("Data directory: data/")
    print("Checking dependencies...")

    # Check if Potrace is installed
    try:
        subprocess.run([r"C:\Users\DELL\scoop\shims\potrace.exe", "--version"], check=True, capture_output=True)
        print("[OK] Potrace installed")
    except:
        print("[WARNING] Potrace NOT installed!")

    # Check if ImageMagick is installed
    try:
        subprocess.run([r"C:\Users\DELL\scoop\apps\imagemagick\current\magick.exe", "--version"], check=True, capture_output=True)
        print("[OK] ImageMagick installed")
    except:
        print("[WARNING] ImageMagick NOT installed!")

@app.on_event("shutdown")
async def shutdown():
    print("DXF Converter API shutting down")
