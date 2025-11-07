from PIL import Image
import os

class FileValidator:
    # Security: Allowed file extensions
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def validate_image(file_path: str) -> dict:
        """
        Validate uploaded image file
        Returns: {"valid": bool, "error": str or None, "info": dict}
        """
        # Check file exists
        if not os.path.exists(file_path):
            return {"valid": False, "error": "File not found"}

        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > FileValidator.MAX_FILE_SIZE:
            return {"valid": False, "error": f"File too large (max 10MB)"}

        # Check file extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in FileValidator.ALLOWED_EXTENSIONS:
            return {"valid": False, "error": f"Invalid file type. Allowed: {', '.join(FileValidator.ALLOWED_EXTENSIONS)}"}

        # Validate it's actually an image
        try:
            with Image.open(file_path) as img:
                img.verify()  # Verify it's an image

            # Re-open to get info (verify() closes the file)
            with Image.open(file_path) as img:
                width, height = img.size
                format_type = img.format

                return {
                    "valid": True,
                    "error": None,
                    "info": {
                        "width": width,
                        "height": height,
                        "format": format_type,
                        "size": file_size
                    }
                }
        except Exception as e:
            return {"valid": False, "error": f"Invalid or corrupted image: {str(e)}"}

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Remove dangerous characters from filename
        """
        # Remove path separators and special chars
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')

        # Limit length
        name, ext = os.path.splitext(filename)
        if len(name) > 100:
            name = name[:100]

        return name + ext
