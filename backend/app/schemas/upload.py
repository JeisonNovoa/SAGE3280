from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    status: str
    total_rows: int
    processed_rows: int
    success_rows: int
    error_rows: int
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UploadStats(BaseModel):
    upload_id: int
    total_patients: int
    patients_by_age_group: dict
    patients_by_sex: dict
    patients_with_risks: dict
    controls_generated: int
    alerts_generated: int
    processing_time_seconds: float
