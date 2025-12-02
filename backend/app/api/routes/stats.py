from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.stats import DashboardStats
from app.utils.stats import calculate_statistics

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get comprehensive statistics for the dashboard.
    """
    stats = calculate_statistics(db)
    return stats


@router.get("/summary")
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Get quick summary statistics.
    """
    from app.models import Patient, Control, Alert
    from app.models.control import ControlStatusEnum
    from app.models.alert import AlertStatusEnum, AlertPriorityEnum

    total_patients = db.query(Patient).filter(Patient.is_active == True).count()

    pending_controls = db.query(Control).join(Patient).filter(
        Patient.is_active == True,
        Control.status == ControlStatusEnum.PENDIENTE
    ).count()

    active_alerts = db.query(Alert).join(Patient).filter(
        Patient.is_active == True,
        Alert.status == AlertStatusEnum.ACTIVA
    ).count()

    urgent_alerts = db.query(Alert).join(Patient).filter(
        Patient.is_active == True,
        Alert.status == AlertStatusEnum.ACTIVA,
        Alert.priority == AlertPriorityEnum.URGENTE
    ).count()

    contacted = db.query(Patient).filter(
        Patient.is_active == True,
        Patient.is_contacted == True
    ).count()

    contact_rate = round((contacted / total_patients * 100) if total_patients > 0 else 0, 2)

    return {
        'total_patients': total_patients,
        'pending_controls': pending_controls,
        'active_alerts': active_alerts,
        'urgent_alerts': urgent_alerts,
        'contacted_patients': contacted,
        'contact_rate': contact_rate
    }
