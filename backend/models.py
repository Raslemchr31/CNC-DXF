from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import json

Base = declarative_base()

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False, index=True)
    original_filename = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    dxf_path = Column(String, nullable=False)
    thumbnail_path = Column(String, nullable=True)
    threshold = Column(Integer, default=50)
    file_size = Column(Integer)  # DXF file size in bytes
    conversion_metadata = Column(Text)  # JSON string with entity counts
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String, default="completed")  # processing, completed, failed

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "created_at": self.created_at.isoformat(),
            "threshold": self.threshold,
            "file_size": self.file_size,
            "metadata": json.loads(self.conversion_metadata) if self.conversion_metadata else {},
            "status": self.status,
            "download_url": f"/api/download/{self.id}",
            "thumbnail_url": f"/api/thumbnail/{self.id}" if self.thumbnail_path else None
        }
