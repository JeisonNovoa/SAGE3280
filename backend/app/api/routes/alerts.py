from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date, datetime

from app.database import get_db
from app.models.alert import Alert, AlertTypeEnum, AlertPriorityEnum, AlertStatusEnum
from app.models.patient import Patient
from pydantic import BaseModel, Field


router = APIRouter(tags=["alerts"])


# ============================================================================
# SCHEMAS
# ============================================================================

class AlertUpdate(BaseModel):
    """Schema for updating an alert"""
    status: Optional[AlertStatusEnum] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=500)


class AlertResponse(BaseModel):
    """Schema for alert response"""
    id: int
    patient_id: int
    alert_type: str
    alert_name: str
    description: str
    priority: str
    status: str
    reason: Optional[str]
    criteria: Optional[str]
    created_date: date
    due_date: Optional[date]
    completed_date: Optional[date]
    notes: Optional[str]

    # Patient info
    patient_name: Optional[str] = None
    patient_document: Optional[str] = None

    class Config:
        from_attributes = True


class AlertStats(BaseModel):
    """Statistics about alerts"""
    total: int
    by_status: dict
    by_priority: dict
    by_type: dict


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/alerts/", response_model=List[AlertResponse])
async def get_alerts(
    alert_type: Optional[AlertTypeEnum] = None,
    priority: Optional[AlertPriorityEnum] = None,
    status: Optional[AlertStatusEnum] = None,
    patient_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get list of alerts with optional filters.

    - **alert_type**: Filter by alert type
    - **priority**: Filter by priority (baja, media, alta, urgente)
    - **status**: Filter by status
    - **patient_id**: Filter by patient ID
    - **limit**: Maximum number of results
    - **offset**: Number of results to skip
    """
    query = db.query(Alert).join(Patient)

    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)

    if priority:
        query = query.filter(Alert.priority == priority)

    if status:
        query = query.filter(Alert.status == status)

    if patient_id:
        query = query.filter(Alert.patient_id == patient_id)

    # Order by priority (urgente first, then alta, media, baja)
    priority_order = {
        AlertPriorityEnum.URGENTE: 1,
        AlertPriorityEnum.ALTA: 2,
        AlertPriorityEnum.MEDIA: 3,
        AlertPriorityEnum.BAJA: 4
    }

    alerts = query.offset(offset).limit(limit).all()

    # Sort by priority
    alerts_sorted = sorted(
        alerts,
        key=lambda a: (priority_order.get(a.priority, 5), a.created_date)
    )

    # Add patient info to response
    result = []
    for alert in alerts_sorted[offset:offset+limit]:
        alert_dict = {
            "id": alert.id,
            "patient_id": alert.patient_id,
            "alert_type": alert.alert_type.value,
            "alert_name": alert.alert_name,
            "description": alert.description,
            "priority": alert.priority.value,
            "status": alert.status.value,
            "reason": alert.reason,
            "criteria": alert.criteria,
            "created_date": alert.created_date,
            "due_date": alert.due_date,
            "completed_date": alert.completed_date,
            "notes": alert.notes,
            "patient_name": f"{alert.patient.first_name} {alert.patient.last_name}" if alert.patient else None,
            "patient_document": alert.patient.document_number if alert.patient else None
        }
        result.append(AlertResponse(**alert_dict))

    return result


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Get a specific alert by ID.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )

    alert_dict = {
        "id": alert.id,
        "patient_id": alert.patient_id,
        "alert_type": alert.alert_type.value,
        "alert_name": alert.alert_name,
        "description": alert.description,
        "priority": alert.priority.value,
        "status": alert.status.value,
        "reason": alert.reason,
        "criteria": alert.criteria,
        "created_date": alert.created_date,
        "due_date": alert.due_date,
        "completed_date": alert.completed_date,
        "notes": alert.notes,
        "patient_name": f"{alert.patient.first_name} {alert.patient.last_name}" if alert.patient else None,
        "patient_document": alert.patient.document_number if alert.patient else None
    }

    return AlertResponse(**alert_dict)


@router.put("/alerts/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an alert's status, dates, or notes.

    - **status**: New status (activa, notificada, programada, completada, ignorada)
    - **due_date**: Due date for the alert
    - **completed_date**: Date when the alert was resolved
    - **notes**: Additional notes about the alert
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )

    # Update fields if provided
    if alert_update.status is not None:
        alert.status = alert_update.status

        # Auto-set completed_date if marking as completed
        if alert_update.status == AlertStatusEnum.COMPLETADA and not alert_update.completed_date:
            alert.completed_date = date.today()

    if alert_update.due_date is not None:
        alert.due_date = alert_update.due_date

    if alert_update.completed_date is not None:
        alert.completed_date = alert_update.completed_date
        # Auto-change status to COMPLETADA if setting completion date
        if alert.status != AlertStatusEnum.COMPLETADA:
            alert.status = AlertStatusEnum.COMPLETADA

    if alert_update.notes is not None:
        alert.notes = alert_update.notes

    db.commit()
    db.refresh(alert)

    alert_dict = {
        "id": alert.id,
        "patient_id": alert.patient_id,
        "alert_type": alert.alert_type.value,
        "alert_name": alert.alert_name,
        "description": alert.description,
        "priority": alert.priority.value,
        "status": alert.status.value,
        "reason": alert.reason,
        "criteria": alert.criteria,
        "created_date": alert.created_date,
        "due_date": alert.due_date,
        "completed_date": alert.completed_date,
        "notes": alert.notes,
        "patient_name": f"{alert.patient.first_name} {alert.patient.last_name}" if alert.patient else None,
        "patient_document": alert.patient.document_number if alert.patient else None
    }

    return AlertResponse(**alert_dict)


@router.delete("/alerts/{alert_id}")
async def dismiss_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Dismiss/ignore an alert (sets status to IGNORADA).
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )

    alert.status = AlertStatusEnum.IGNORADA
    db.commit()

    return {"message": "Alert dismissed successfully", "alert_id": alert_id}


@router.get("/alerts/stats/summary", response_model=AlertStats)
async def get_alerts_stats(db: Session = Depends(get_db)):
    """
    Get statistics about alerts.
    """
    # Total alerts
    total = db.query(Alert).count()

    # By status
    by_status = {}
    status_counts = db.query(
        Alert.status,
        func.count(Alert.id)
    ).group_by(Alert.status).all()

    for status_enum, count in status_counts:
        by_status[status_enum.value] = count

    # By priority
    by_priority = {}
    priority_counts = db.query(
        Alert.priority,
        func.count(Alert.id)
    ).group_by(Alert.priority).all()

    for priority_enum, count in priority_counts:
        by_priority[priority_enum.value] = count

    # By type
    by_type = {}
    type_counts = db.query(
        Alert.alert_type,
        func.count(Alert.id)
    ).group_by(Alert.alert_type).all()

    for type_enum, count in type_counts:
        by_type[type_enum.value] = count

    return AlertStats(
        total=total,
        by_status=by_status,
        by_priority=by_priority,
        by_type=by_type
    )
