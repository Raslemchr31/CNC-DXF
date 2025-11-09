import os
import subprocess
import uuid
import json
from pathlib import Path
from PIL import Image
import ezdxf

class DXFConverter:
    def __init__(self, upload_dir="data/uploads", output_dir="data/outputs"):
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)

        # Create directories
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def convert_image_to_dxf(
        self,
        image_path: str,
        threshold: int = 50
    ) -> dict:
        """
        Convert image to DXF using ImageMagick + Potrace

        Process:
        1. Convert image to PBM (bitmap) with threshold
        2. Use Potrace to convert PBM to DXF (generates POLYLINES)
        3. Analyze DXF to verify entity types
        4. Generate thumbnail

        Args:
            image_path: Path to input image
            threshold: Edge detection threshold (0-100)

        Returns:
            dict with dxf_path, thumbnail_path, metadata
        """
        # Generate unique IDs
        file_id = str(uuid.uuid4())
        pbm_path = self.output_dir / f"{file_id}.pbm"
        dxf_path = self.output_dir / f"{file_id}.dxf"
        thumbnail_path = self.output_dir / f"{file_id}_thumb.jpg"

        try:
            # Step 1: Convert to bitmap with threshold using PIL (Python)
            print(f"Converting image to bitmap (threshold={threshold}%)...")

            # Open image with PIL
            with Image.open(image_path) as img:
                # Convert to grayscale
                img_gray = img.convert('L')

                # Apply threshold
                threshold_value = int(255 * threshold / 100)
                img_bw = img_gray.point(lambda x: 255 if x > threshold_value else 0, mode='1')

                # Save as PBM (bitmap format for Potrace)
                img_bw.save(str(pbm_path), 'PPM')

            if not pbm_path.exists():
                raise Exception("Failed to create bitmap file")

            # Step 2: Convert bitmap to DXF using Potrace
            # Potrace generates POLYLINES (not SPLINES) - critical for CNC
            print("Converting bitmap to DXF...")
            potrace_args = [
                r"C:\Users\DELL\scoop\shims\potrace.exe",
                "-b", "dxf",  # Output format: DXF
                "--longcurve",  # More line segments = smoother curves
                "-u", "10",  # Units: 10 DXF units per pixel
                "-t", "2",  # Corner threshold (lower = sharper corners)
                str(pbm_path),
                "-o", str(dxf_path)
            ]
            result = subprocess.run(potrace_args, check=True, capture_output=True, text=True)

            if not dxf_path.exists():
                raise Exception("Failed to create DXF file")

            # Step 3: Convert POLYLINES to LINEs for CNC compatibility
            print("Converting POLYLINES to LINEs...")
            self.convert_polylines_to_lines(str(dxf_path))

            # Step 4: Verify DXF and extract metadata
            print("Analyzing DXF file...")
            metadata = self.analyze_dxf(str(dxf_path))

            # CRITICAL: Check for SPLINES (should not exist)
            if metadata.get("has_splines", False):
                raise Exception("DXF contains SPLINES! CNC incompatible. This should not happen with Potrace.")

            # Step 5: Generate thumbnail from original image
            print("Generating thumbnail...")
            self.generate_thumbnail(image_path, str(thumbnail_path))

            # Clean up temporary bitmap
            pbm_path.unlink()

            return {
                "dxf_path": str(dxf_path),
                "thumbnail_path": str(thumbnail_path),
                "metadata": metadata
            }

        except subprocess.CalledProcessError as e:
            # Command failed
            error_msg = e.stderr if e.stderr else str(e)
            raise Exception(f"Conversion failed: {error_msg}")
        except Exception as e:
            # Clean up on error
            for path in [pbm_path, dxf_path, thumbnail_path]:
                if path.exists():
                    path.unlink()
            raise

    def convert_polylines_to_lines(self, dxf_path: str):
        """
        Convert all POLYLINE entities to individual LINE entities

        This is critical for CNC machines that require LINE entities
        instead of POLYLINES. Each polyline is "exploded" into
        individual line segments.

        Args:
            dxf_path: Path to DXF file to convert (will be modified in-place)
        """
        # Read the original DXF
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()

        # Get all current entities
        entities_to_convert = []
        for entity in msp:
            if entity.dxftype() == 'POLYLINE':
                entities_to_convert.append(entity)

        # Convert each POLYLINE to LINEs
        for polyline in entities_to_convert:
            # Get all vertices from the polyline
            points = list(polyline.points())

            # Create LINE for each segment
            for i in range(len(points) - 1):
                start = points[i]
                end = points[i + 1]
                msp.add_line(start, end)

            # If polyline is closed, connect last point to first
            if polyline.is_closed and len(points) > 2:
                msp.add_line(points[-1], points[0])

            # Remove the original polyline
            msp.delete_entity(polyline)

        # Save the modified DXF back to the same file
        doc.saveas(dxf_path)

    def analyze_dxf(self, dxf_path: str) -> dict:
        """
        Analyze DXF file and extract metadata

        Returns:
            dict with entity counts, types, file size, etc.
        """
        doc = ezdxf.readfile(dxf_path)
        msp = doc.modelspace()
        entities = list(msp)

        # Count entity types
        entity_types = {}
        for entity in entities:
            etype = entity.dxftype()
            entity_types[etype] = entity_types.get(etype, 0) + 1

        # Get file info
        file_size = os.path.getsize(dxf_path)

        # Check for problematic entity types
        has_splines = "SPLINE" in entity_types
        has_arcs = "ARC" in entity_types
        has_polylines = "POLYLINE" in entity_types or "LWPOLYLINE" in entity_types

        return {
            "total_entities": len(entities),
            "entity_types": entity_types,
            "has_splines": has_splines,
            "has_arcs": has_arcs,
            "has_polylines": has_polylines,
            "file_size": file_size,
            "dxf_version": doc.dxfversion,
            "units": str(doc.units)
        }

    def generate_thumbnail(self, image_path: str, thumbnail_path: str, size=(200, 200)):
        """Generate thumbnail from original image"""
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')

            # Create thumbnail
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, "JPEG", quality=85)
