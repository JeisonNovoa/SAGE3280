from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date, datetime

from app.database import get_db
from app.models.control import Control, ControlStatusEnum, ControlTypeEnum
from app.models.patient import Patient
from pydantic import BaseModel, Field


router = APIRouter(tags=["controls"])


# ============================================================================
# SCHEMAS
# ============================================================================

class ControlUpdate(BaseModel):
    """Schema for updating a control"""
    status: Optional[ControlStatusEnum] = None
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=500)


class ControlResponse(BaseModel):
    """Schema for control response"""
    id: int
    patient_id: int
    control_type: str
    control_name: str
    status: str
    last_date: Optional[date]
    due_date: Optional[date]
    scheduled_date: Optional[date]
    completed_date: Optional[date]
    is_urgent: bool
    priority_score: int
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Patient info
    patient_name: Optional[str] = None
    patient_document: Optional[str] = None

    class Config:
        from_attributes = True


class ControlStats(BaseModel):
    """Statistics about controls"""
    total: int
    by_status: dict
    by_type: dict
    urgent_count: int


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/controls/", response_model=List[ControlResponse])
async def get_controls(
    control_type: Optional[ControlTypeEnum] = None,
    status: Optional[ControlStatusEnum] = None,
    urgent_only: bool = False,
    patient_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get list of controls with optional filters.

    - **control_type**: Filter by control type
    - **status**: Filter by status
    - **urgent_only**: Show only urgent controls
    - **patient_id**: Filter by patient ID
    - **limit**: Maximum number of results
    - **offset**: Number of results to skip
    """
    query = db.query(Control).join(Patient)

    if control_type:
        query = query.filter(Control.control_type == control_type)

    if status:
        query = query.filter(Control.status == status)

    if urgent_only:
        query = query.filter(Control.is_urgent == True)

    if patient_id:
        query = query.filter(Control.patient_id == patient_id)

    # Order by priority (urgent first, then by priority score)
    query = query.order_by(
        Control.is_urgent.desc(),
        Control.priority_score.desc(),
        Control.due_date.asc()
    )

    controls = query.offset(offset).limit(limit).all()

    # Add patient info to response
    result = []
    for control in controls:
        control_dict = {
            "id": control.id,
            "patient_id": control.patient_id,
            "control_type": control.control_type.value,
            "control_name": control.control_name,
            "status": control.status.value,
            "last_date": control.last_date,
            "due_date": control.due_date,
            "scheduled_date": control.scheduled_date,
            "completed_date": control.completed_date,
            "is_urgent": control.is_urgent,
            "priority_score": control.priority_score,
            "notes": control.notes,
            "created_at": control.created_at,
            "updated_at": control.updated_at,
            "patient_name": f"{control.patient.first_name} {control.patient.last_name}" if control.patient else None,
            "patient_document": control.patient.document_number if control.patient else None
        }
        result.append(ControlResponse(**control_dict))

    return result


@router.get("/controls/{control_id}", response_model=ControlResponse)
async def get_control(control_id: int, db: Session = Depends(get_db)):
    """
    Get a specific control by ID.
    """
    control = db.query(Control).filter(Control.id == control_id).first()

    if not control:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control with id {control_id} not found"
        )

    control_dict = {
        "id": control.id,
        "patient_id": control.patient_id,
        "control_type": control.control_type.value,
        "control_name": control.control_name,
        "status": control.status.value,
        "last_date": control.last_date,
        "due_date": control.due_date,
        "scheduled_date": control.scheduled_date,
        "completed_date": control.completed_date,
        "is_urgent": control.is_urgent,
        "priority_score": control.priority_score,
        "notes": control.notes,
        "created_at": control.created_at,
        "updated_at": control.updated_at,
        "patient_name": f"{control.patient.first_name} {control.patient.last_name}" if control.patient else None,
        "patient_document": control.patient.document_number if control.patient else None
    }

    return ControlResponse(**control_dict)


@router.put("/controls/{control_id}", response_model=ControlResponse)
async def update_control(
    control_id: int,
    control_update: ControlUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a control's status, dates, or notes.

    - **status**: New status (pendiente, programado, completado, vencido, cancelado)
    - **scheduled_date**: Date when the control is scheduled
    - **completed_date**: Date when the control was completed
    - **notes**: Additional notes about the control
    """
    control = db.query(Control).filter(Control.id == control_id).first()

    if not control:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control with id {control_id} not found"
        )

    # Update fields if provided
    if control_update.status is not None:
        control.status = control_update.status

        # Auto-set completed_date if marking as completed
        if control_update.status == ControlStatusEnum.COMPLETADO and not control_update.completed_date:
            control.completed_date = date.today()

    if control_update.scheduled_date is not None:
        control.scheduled_date = control_update.scheduled_date
        # Auto-change status to PROGRAMADO if setting a date
        if control.status == ControlStatusEnum.PENDIENTE:
            control.status = ControlStatusEnum.PROGRAMADO

    if control_update.completed_date is not None:
        control.completed_date = control_update.completed_date
        # Auto-change status to COMPLETADO if setting completion date
        if control.status != ControlStatusEnum.COMPLETADO:
            control.status = ControlStatusEnum.COMPLETADO

    if control_update.notes is not None:
        control.notes = control_update.notes

    db.commit()
    db.refresh(control)

    control_dict = {
        "id": control.id,
        "patient_id": control.patient_id,
        "control_type": control.control_type.value,
        "control_name": control.control_name,
        "status": control.status.value,
        "last_date": control.last_date,
        "due_date": control.due_date,
        "scheduled_date": control.scheduled_date,
        "completed_date": control.completed_date,
        "is_urgent": control.is_urgent,
        "priority_score": control.priority_score,
        "notes": control.notes,
        "created_at": control.created_at,
        "updated_at": control.updated_at,
        "patient_name": f"{control.patient.first_name} {control.patient.last_name}" if control.patient else None,
        "patient_document": control.patient.document_number if control.patient else None
    }

    return ControlResponse(**control_dict)


@router.get("/controls/stats/summary", response_model=ControlStats)
async def get_controls_stats(db: Session = Depends(get_db)):
    """
    Get statistics about controls.
    """
    # Total controls
    total = db.query(Control).count()

    # By status
    by_status = {}
    status_counts = db.query(
        Control.status,
        func.count(Control.id)
    ).group_by(Control.status).all()

    for status_enum, count in status_counts:
        by_status[status_enum.value] = count

    # By type
    by_type = {}
    type_counts = db.query(
        Control.control_type,
        func.count(Control.id)
    ).group_by(Control.control_type).all()

    for type_enum, count in type_counts:
        by_type[type_enum.value] = count

    # Urgent count
    urgent_count = db.query(Control).filter(Control.is_urgent == True).count()

    return ControlStats(
        total=total,
        by_status=by_status,
        by_type=by_type,
        urgent_count=urgent_count
    )
