from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.patient import Patient, AgeGroupEnum
from app.models.control import Control, ControlStatusEnum
from app.models.alert import Alert, AlertPriorityEnum, AlertStatusEnum
from typing import Dict, List


def calculate_statistics(db: Session) -> Dict:
    """
    Calculate comprehensive statistics for the dashboard.
    """

    # Total patients
    total_patients = db.query(Patient).filter(Patient.is_active == True).count()

    # Patients by age group
    age_group_stats = db.query(
        Patient.age_group,
        func.count(Patient.id).label('count')
    ).filter(
        Patient.is_active == True,
        Patient.age_group.isnot(None)
    ).group_by(Patient.age_group).all()

    patients_by_age_group = [
        {
            'name': group,
            'count': count,
            'percentage': round((count / total_patients * 100) if total_patients > 0 else 0, 2)
        }
        for group, count in age_group_stats
    ]

    # Patients by sex
    sex_stats = db.query(
        Patient.sex,
        func.count(Patient.id).label('count')
    ).filter(
        Patient.is_active == True,
        Patient.sex.isnot(None)
    ).group_by(Patient.sex).all()

    patients_by_sex = [
        {
            'name': sex,
            'count': count,
            'percentage': round((count / total_patients * 100) if total_patients > 0 else 0, 2)
        }
        for sex, count in sex_stats
    ]

    # Risk statistics
    risk_stats = {
        'hypertensive': db.query(Patient).filter(
            Patient.is_active == True,
            Patient.is_hypertensive == True
        ).count(),
        'diabetic': db.query(Patient).filter(
            Patient.is_active == True,
            Patient.is_diabetic == True
        ).count(),
        'pregnant': db.query(Patient).filter(
            Patient.is_active == True,
            Patient.is_pregnant == True
        ).count(),
        'cardiovascular_risk': db.query(Patient).filter(
            Patient.is_active == True,
            Patient.has_cardiovascular_risk == True
        ).count(),
    }
    risk_stats['total_with_risks'] = db.query(Patient).filter(
        Patient.is_active == True,
        (Patient.is_hypertensive == True) |
        (Patient.is_diabetic == True) |
        (Patient.is_pregnant == True) |
        (Patient.has_cardiovascular_risk == True)
    ).count()

    # Controls statistics
    total_controls_pending = db.query(Control).join(Patient).filter(
        Patient.is_active == True,
        Control.status == ControlStatusEnum.PENDIENTE
    ).count()

    controls_by_type = db.query(
        Control.control_type,
        func.sum(case((Control.status == ControlStatusEnum.PENDIENTE, 1), else_=0)).label('pending'),
        func.sum(case((Control.status == ControlStatusEnum.COMPLETADO, 1), else_=0)).label('completed'),
        func.sum(case((Control.status == ControlStatusEnum.VENCIDO, 1), else_=0)).label('overdue'),
    ).join(Patient).filter(
        Patient.is_active == True
    ).group_by(Control.control_type).all()

    controls_list = [
        {
            'control_type': control_type,
            'pending': int(pending or 0),
            'completed': int(completed or 0),
            'overdue': int(overdue or 0)
        }
        for control_type, pending, completed, overdue in controls_by_type
    ]

    # Alerts statistics
    total_active_alerts = db.query(Alert).join(Patient).filter(
        Patient.is_active == True,
        Alert.status == AlertStatusEnum.ACTIVA
    ).count()

    alerts_by_type = db.query(
        Alert.alert_type,
        func.count(Alert.id).label('count')
    ).join(Patient).filter(
        Patient.is_active == True,
        Alert.status == AlertStatusEnum.ACTIVA
    ).group_by(Alert.alert_type).all()

    alerts_by_type_list = []
    for alert_type, count in alerts_by_type:
        priority_breakdown = db.query(
            Alert.priority,
            func.count(Alert.id).label('count')
        ).join(Patient).filter(
            Patient.is_active == True,
            Alert.alert_type == alert_type,
            Alert.status == AlertStatusEnum.ACTIVA
        ).group_by(Alert.priority).all()

        alerts_by_type_list.append({
            'alert_type': alert_type,
            'count': count,
            'priority_breakdown': {priority: count for priority, count in priority_breakdown}
        })

    alerts_by_priority = db.query(
        Alert.priority,
        func.count(Alert.id).label('count')
    ).join(Patient).filter(
        Patient.is_active == True,
        Alert.status == AlertStatusEnum.ACTIVA
    ).group_by(Alert.priority).all()

    alerts_priority_dict = {priority: count for priority, count in alerts_by_priority}

    # Contact statistics
    contacted = db.query(Patient).filter(
        Patient.is_active == True,
        Patient.is_contacted == True
    ).count()

    not_contacted = total_patients - contacted

    contact_rate = round((contacted / total_patients * 100) if total_patients > 0 else 0, 2)

    contact_status_stats = db.query(
        Patient.contact_status,
        func.count(Patient.id).label('count')
    ).filter(
        Patient.is_active == True,
        Patient.contact_status.isnot(None)
    ).group_by(Patient.contact_status).all()

    by_status = {status: count for status, count in contact_status_stats}

    # Last upload date (placeholder - would need to query Upload table)
    from datetime import datetime
    last_upload = db.query(func.max(Patient.created_at)).scalar()
    last_upload_date = last_upload.strftime('%Y-%m-%d') if last_upload else 'N/A'

    # Coverage metrics (placeholder - would need more complex logic)
    coverage_by_age_group = patients_by_age_group  # Simplified

    return {
        'total_patients': total_patients,
        'last_upload_date': last_upload_date,
        'patients_by_age_group': patients_by_age_group,
        'patients_by_sex': patients_by_sex,
        'risk_stats': risk_stats,
        'total_controls_pending': total_controls_pending,
        'controls_by_type': controls_list,
        'total_active_alerts': total_active_alerts,
        'alerts_by_type': alerts_by_type_list,
        'alerts_by_priority': alerts_priority_dict,
        'contact_stats': {
            'contacted': contacted,
            'not_contacted': not_contacted,
            'contact_rate': contact_rate,
            'by_status': by_status
        },
        'coverage_by_age_group': coverage_by_age_group
    }
