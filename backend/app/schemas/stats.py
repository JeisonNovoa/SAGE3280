from pydantic import BaseModel
from typing import Dict, List


class GroupStats(BaseModel):
    name: str
    count: int
    percentage: float


class AlertStats(BaseModel):
    alert_type: str
    count: int
    priority_breakdown: Dict[str, int]


class ControlStats(BaseModel):
    control_type: str
    pending: int
    completed: int
    overdue: int


class RiskStats(BaseModel):
    hypertensive: int
    diabetic: int
    pregnant: int
    cardiovascular_risk: int
    total_with_risks: int


class ContactStats(BaseModel):
    contacted: int
    not_contacted: int
    contact_rate: float
    by_status: Dict[str, int]


class DashboardStats(BaseModel):
    # General
    total_patients: int
    last_upload_date: str

    # Demographics
    patients_by_age_group: List[GroupStats]
    patients_by_sex: List[GroupStats]

    # Health risks
    risk_stats: RiskStats

    # Controls
    total_controls_pending: int
    controls_by_type: List[ControlStats]

    # Alerts
    total_active_alerts: int
    alerts_by_type: List[AlertStats]
    alerts_by_priority: Dict[str, int]

    # Contact status
    contact_stats: ContactStats

    # Coverage metrics
    coverage_by_age_group: List[GroupStats]
