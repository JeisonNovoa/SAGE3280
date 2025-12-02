from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class PatientBase(BaseModel):
    document_number: str
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    alert_name: str
    priority: str
    status: str
    reason: Optional[str] = None
    due_date: Optional[date] = None

    class Config:
        from_attributes = True


class ControlResponse(BaseModel):
    id: int
    control_type: str
    control_name: str
    status: str
    due_date: Optional[date] = None
    is_urgent: bool

    class Config:
        from_attributes = True


class PatientResponse(BaseModel):
    id: int
    document_number: str
    full_name: str
    age: Optional[int] = None
    sex: Optional[str] = None
    age_group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    # Health status
    is_pregnant: bool = False
    is_hypertensive: bool = False
    is_diabetic: bool = False
    has_cardiovascular_risk: bool = False
    cardiovascular_risk_level: Optional[str] = None

    # Controls and Alerts
    controls: List[ControlResponse] = []
    alerts: List[AlertResponse] = []

    # Contact status
    is_contacted: bool = False
    contact_attempts: int = 0
    contact_status: Optional[str] = None

    created_at: datetime

    class Config:
        from_attributes = True


class PatientList(BaseModel):
    total: int
    page: int
    page_size: int
    patients: List[PatientResponse]


class PatientFilter(BaseModel):
    age_group: Optional[str] = None
    sex: Optional[str] = None
    is_pregnant: Optional[bool] = None
    is_hypertensive: Optional[bool] = None
    is_diabetic: Optional[bool] = None
    has_cardiovascular_risk: Optional[bool] = None
    control_type: Optional[str] = None
    alert_type: Optional[str] = None
    is_contacted: Optional[bool] = None
