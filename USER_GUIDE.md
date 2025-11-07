# CNC DXF Converter - User Guide

Complete guide for using the CNC DXF Converter application.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Converting Images](#converting-images)
3. [Understanding Threshold](#understanding-threshold)
4. [Managing Conversions](#managing-conversions)
5. [Working with DXF Files](#working-with-dxf-files)
6. [Best Practices](#best-practices)
7. [Tips and Tricks](#tips-and-tricks)

---

## Getting Started

### Accessing the Application

1. **Start the servers** (see INSTALLATION.md if not running)
2. **Open your browser** to: http://localhost:5173
3. You should see the **CNC DXF Converter** interface

### Interface Overview

The application has three main sections:

1. **Upload Area** (top):
   - Drag-and-drop zone for images
   - File browser button
   - Threshold slider

2. **Conversion History** (middle):
   - List of past conversions
   - Thumbnail previews
   - Download buttons

3. **Statistics** (bottom):
   - Total conversions count
   - Storage usage

---

## Converting Images

### Step-by-Step Conversion Process

#### 1. Prepare Your Image

**Supported Formats**:
- JPG/JPEG
- PNG
- BMP

**Recommended Image Properties**:
- Resolution: 500x500 to 2000x2000 pixels
- Color: Any (will be converted to grayscale)
- Content: Clear, high-contrast images work best
- File size: Under 10MB for best performance

**Good Image Candidates**:
- Company logos
- Text and lettering
- Simple shapes and silhouettes
- Line drawings
- High-contrast photographs

**Avoid**:
- Very low resolution images (< 300x300px)
- Extremely detailed photographs
- Low-contrast images
- Blurry or unclear images

#### 2. Upload Image

**Method 1: Drag and Drop**
1. Click and drag your image file
2. Drop it onto the upload area
3. You'll see the filename appear

**Method 2: File Browser**
1. Click "Choose File" button
2. Navigate to your image
3. Select and click "Open"

#### 3. Adjust Threshold

Move the slider to set edge detection sensitivity:

- **Position 1 (Far Left - 0%)**: Everything becomes white (no cutting)
- **Position 2 (25%)**: Very sensitive, captures subtle details
- **Position 3 (50% - DEFAULT)**: Balanced, good starting point
- **Position 4 (75%)**: Only strong contrasts
- **Position 5 (Far Right - 100%)**: Everything becomes black (full cutting)

**Tip**: Start at 50% and adjust based on preview results.

#### 4. Convert

1. Click **"Convert to DXF"** button
2. Wait 2-5 seconds for processing
3. Conversion complete! File appears in history below

#### 5. Download

1. Locate your conversion in the history list
2. Click the **Download** button (arrow icon)
3. DXF file saves to your Downloads folder
4. Filename format: `[original_name].dxf`

---

## Understanding Threshold

The threshold parameter is **critical** for getting usable CNC cutting files.

### How Threshold Works

The conversion process:
1. **Grayscale**: Color image → shades of gray (0-255)
2. **Threshold**: Pick a cutoff point (e.g., 50% = 128)
3. **Binary**: Pixels above threshold → white (no cut)
4. **Binary**: Pixels below threshold → black (cut line)
5. **Vectorize**: Trace black areas to create cutting paths

### Threshold Examples

Let's say you're converting a company logo:

#### Example 1: Logo with Background

**Original**: Black logo on light gray background

- **20% threshold**:
  - Result: Logo + background texture captured
  - CNC will cut: Logo outline + background noise
  - Use case: Not ideal - too much unwanted detail

- **50% threshold** (RECOMMENDED):
  - Result: Clean logo outline
  - CNC will cut: Just the logo shape
  - Use case: Perfect for most logos

- **80% threshold**:
  - Result: Only darkest parts of logo
  - CNC will cut: Partial logo (missing details)
  - Use case: Logo may be incomplete

#### Example 2: Text on White Background

**Original**: Black text on pure white

- **30% threshold**:
  - Result: Text + paper texture + shadows
  - CNC will cut: Text + noise
  - Use case: Avoid unless you want texture

- **50% threshold** (RECOMMENDED):
  - Result: Clean text characters
  - CNC will cut: Just the letters
  - Use case: Perfect for signage

- **70% threshold**:
  - Result: Text with slightly thinner strokes
  - CNC will cut: Refined, cleaner text
  - Use case: Good for bold fonts

#### Example 3: Photograph Portrait

**Original**: Person's face photo

- **30% threshold**:
  - Result: Face with hair, shadows, clothing
  - CNC will cut: Very detailed silhouette
  - Use case: Artistic portrait cutout

- **50% threshold**:
  - Result: Main facial features + outline
  - CNC will cut: Recognizable profile
  - Use case: Balanced portrait

- **70% threshold**:
  - Result: Strong features only (eyes, nose outline)
  - CNC will cut: Minimalist portrait
  - Use case: Abstract/artistic

### Finding the Right Threshold

**Process**:
1. Start at 50%
2. Convert and download DXF
3. Preview in CAD software
4. If too much detail → increase threshold (60%, 70%)
5. If missing detail → decrease threshold (40%, 30%)
6. Repeat until satisfied

**Tips**:
- Most images work well between 40-60%
- Simple logos: try 50-60%
- Detailed artwork: try 30-40%
- Text: try 50-70%
- Photographs: try 40-50%

---

## Managing Conversions

### Conversion History

Every conversion is saved and displayed in the history list.

**Information Displayed**:
- **Filename**: Original image name
- **Thumbnail**: Visual preview
- **Date/Time**: When conversion was created
- **Threshold**: Value used for this conversion
- **File Size**: DXF file size in KB/MB
- **Actions**: Download and Delete buttons

### Searching History

1. Use the **Search** box at top of history
2. Type filename or part of filename
3. Results filter in real-time
4. Clear search to see all conversions

### Downloading Files

**Single Download**:
1. Click download icon on desired conversion
2. File saves to your Downloads folder
3. Filename: `[original_name].dxf`

**Re-downloading**:
- Files remain available indefinitely
- Download same file multiple times if needed
- Each download creates a copy

### Deleting Conversions

**Important**: Deletion is permanent!

1. Click **Delete** button (trash icon)
2. Conversion removed from history
3. Original image deleted from server
4. Generated DXF file deleted from server
5. Thumbnail deleted from server

**When to Delete**:
- Test conversions you don't need
- Wrong threshold values
- Incorrect source images
- Free up storage space

---

## Working with DXF Files

### Opening DXF Files

**Compatible Software**:
- **AutoCAD** (Commercial)
- **LibreCAD** (Free, Open Source)
- **DraftSight** (Free/Commercial)
- **QCAD** (Free/Commercial)
- **Inkscape** (Free, with DXF import)
- **Your CNC Software** (Mach3, LinuxCNC, etc.)

**Opening Steps** (LibreCAD example):
1. Open LibreCAD
2. File → Open
3. Select your DXF file
4. View the cutting paths

### Verifying DXF Content

**Check for POLYLINES** (Required for CNC):
1. Open DXF in CAD software
2. Select an entity (cutting path)
3. Check entity type in properties
4. Should say: **POLYLINE** or **LWPOLYLINE**
5. Should NOT say: **SPLINE** or **CURVE**

**Why POLYLINES Matter**:
- CNC machines need straight line segments
- SPLINES are curves that many CNC controllers can't process
- This converter ONLY produces POLYLINES
- Your CNC machine will work correctly

### Importing to CNC Software

**General Process** (varies by software):
1. Open your CNC control software
2. Import/Load DXF file
3. Review cutting paths
4. Set cutting parameters:
   - Feed rate
   - Cutting speed
   - Material thickness
   - Kerf compensation
5. Generate G-code
6. Send to CNC machine

**Note**: CNC-specific settings are beyond this guide's scope. Consult your CNC machine documentation.

### Editing DXF Files

You can modify DXF files before cutting:

**Common Edits**:
- Scale to desired size
- Rotate or mirror
- Combine multiple DXFs
- Add registration marks
- Offset paths for kerf compensation

**Tools**:
- Any CAD software listed above
- Your CNC software's built-in editor

---

## Best Practices

### Image Preparation

1. **Start Simple**:
   - Test with simple shapes first
   - Logos and text are ideal starting points
   - Build complexity gradually

2. **High Contrast**:
   - Increase contrast in image editor before upload
   - Clear distinction between subject and background
   - Remove gradients if possible

3. **Clean Background**:
   - Plain white or black backgrounds work best
   - Remove busy backgrounds in image editor
   - Crop tightly around subject

4. **Appropriate Resolution**:
   - Minimum: 500x500 pixels
   - Optimal: 1000x1000 to 1500x1500 pixels
   - Avoid excessive resolution (>3000x3000)

### Conversion Workflow

1. **Test First**:
   - Convert at 50% threshold
   - Download and preview
   - Adjust threshold if needed

2. **Keep Notes**:
   - Record successful threshold values
   - Note which image types work best
   - Build your own reference guide

3. **Iterate**:
   - Don't expect perfect first try
   - Small threshold adjustments (5-10%) at a time
   - Compare multiple versions

### File Management

1. **Naming Convention**:
   - Use descriptive filenames
   - Include version numbers: `logo_v1.jpg`, `logo_v2.jpg`
   - Date large batches: `project_2024-01-15.jpg`

2. **Organize Conversions**:
   - Delete test conversions regularly
   - Keep final versions
   - Download important files immediately

3. **Backup**:
   - Keep original images
   - Save successful DXF files elsewhere
   - Don't rely solely on conversion history

---

## Tips and Tricks

### Getting Better Results

**For Logos**:
- Start with vector logos (SVG, AI) when possible
- Rasterize at high resolution
- Use 50-60% threshold
- Increase threshold if too much detail captured

**For Text**:
- Use bold, sans-serif fonts
- Minimum font size: 24pt
- High contrast: black text on white
- Try 50-70% threshold

**For Photographs**:
- Convert to grayscale first in image editor
- Increase contrast dramatically
- Simplify details manually
- Try 40-50% threshold
- Expect more experimentation needed

**For Line Drawings**:
- Ensure lines are thick enough (2px minimum)
- Clean up stray marks in image editor
- Use 50% threshold as starting point
- Usually converts cleanly

### Speed Tips

1. **Batch Processing**:
   - Prepare multiple images
   - Upload and convert in sequence
   - Download all at once from history

2. **Parallel Testing**:
   - Convert same image at 40%, 50%, 60%
   - Compare all three versions
   - Pick the best one
   - Delete the others

3. **Templates**:
   - Save successful threshold values
   - Create similar images with same settings
   - Reuse proven approaches

### Common Mistakes to Avoid

1. **Don't**:
   - Use extremely low resolution images
   - Expect photos to convert like logos
   - Skip the preview step
   - Forget to adjust threshold
   - Delete before downloading

2. **Always**:
   - Start with 50% threshold
   - Preview DXF before sending to CNC
   - Keep original images
   - Test on scrap material first
   - Verify POLYLINES in CAD software

### Troubleshooting Results

**Problem**: Too much detail, noisy output
- **Solution**: Increase threshold by 10-20%
- **Solution**: Clean up image in editor first
- **Solution**: Simplify source image

**Problem**: Missing important details
- **Solution**: Decrease threshold by 10-20%
- **Solution**: Increase image contrast
- **Solution**: Use higher resolution image

**Problem**: Broken or disconnected paths
- **Solution**: Increase image resolution
- **Solution**: Clean up source image
- **Solution**: Ensure lines are thick enough

**Problem**: File too complex for CNC
- **Solution**: Increase threshold to simplify
- **Solution**: Reduce image resolution slightly
- **Solution**: Simplify image manually first

---

## Advanced Usage

### API Integration

If you're a developer, you can integrate the API into your own tools:

**Endpoint**: `POST http://localhost:8000/api/convert`

**Example** (Python):
```python
import requests

files = {'file': open('logo.jpg', 'rb')}
data = {'threshold': 50}
response = requests.post('http://localhost:8000/api/convert', files=files, data=data)
result = response.json()
dxf_url = result['data']['download_url']
```

See README.md for full API documentation.

### Automation

**Batch Conversion Script** (PowerShell):
```powershell
# Convert all JPG files in a folder
$images = Get-ChildItem *.jpg
foreach ($img in $images) {
    curl -X POST http://localhost:8000/api/convert `
      -F "file=@$($img.Name)" `
      -F "threshold=50"
}
```

---

## Support

Need help?
- Check INSTALLATION.md for setup issues
- Review Troubleshooting section above
- Check backend terminal for error messages
- Open GitHub issue with sample image

---

## Summary

**Quick Reference**:
1. Upload image (JPG, PNG, BMP)
2. Set threshold (start at 50%)
3. Click Convert
4. Download DXF
5. Preview in CAD software
6. Adjust threshold if needed
7. Send to CNC machine

**Remember**:
- Simple images work best
- 50% threshold is a good starting point
- Always preview before cutting
- Files contain POLYLINES (CNC-compatible)
- Experiment and iterate

Happy cutting!
