from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.database import get_db
from app.models import Patient, Control, Alert
from app.models.control import ControlTypeEnum
from app.models.alert import AlertTypeEnum
from app.schemas.patient import PatientResponse, PatientList, PatientFilter
from typing import Optional, List

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_model=PatientList)
def get_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    age_group: Optional[str] = None,
    sex: Optional[str] = None,
    is_pregnant: Optional[bool] = None,
    is_hypertensive: Optional[bool] = None,
    is_diabetic: Optional[bool] = None,
    has_cardiovascular_risk: Optional[bool] = None,
    control_type: Optional[str] = None,
    alert_type: Optional[str] = None,
    is_contacted: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of patients with optional filters.
    """
    query = db.query(Patient).filter(Patient.is_active == True)

    # Apply filters
    if age_group:
        query = query.filter(Patient.age_group == age_group)

    if sex:
        query = query.filter(Patient.sex == sex)

    if is_pregnant is not None:
        query = query.filter(Patient.is_pregnant == is_pregnant)

    if is_hypertensive is not None:
        query = query.filter(Patient.is_hypertensive == is_hypertensive)

    if is_diabetic is not None:
        query = query.filter(Patient.is_diabetic == is_diabetic)

    if has_cardiovascular_risk is not None:
        query = query.filter(Patient.has_cardiovascular_risk == has_cardiovascular_risk)

    if is_contacted is not None:
        query = query.filter(Patient.is_contacted == is_contacted)

    if control_type:
        query = query.join(Control).filter(Control.control_type == control_type)

    if alert_type:
        query = query.join(Alert).filter(Alert.alert_type == alert_type)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Patient.full_name.ilike(search_term),
                Patient.document_number.ilike(search_term)
            )
        )

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    patients = query.offset(offset).limit(page_size).all()

    return PatientList(
        total=total,
        page=page,
        page_size=page_size,
        patients=patients
    )


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Get a single patient by ID.
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.is_active == True
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    return patient


@router.get("/document/{document_number}", response_model=PatientResponse)
def get_patient_by_document(document_number: str, db: Session = Depends(get_db)):
    """
    Get a patient by document number.
    """
    patient = db.query(Patient).filter(
        Patient.document_number == document_number,
        Patient.is_active == True
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    return patient


@router.put("/{patient_id}/contact")
def update_contact_status(
    patient_id: int,
    contact_status: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Update patient contact status.
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.is_active == True
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    patient.is_contacted = True
    patient.contact_attempts += 1
    patient.contact_status = contact_status
    from datetime import datetime
    patient.last_contact_date = datetime.now()

    db.commit()
    db.refresh(patient)

    return {"message": "Estado de contacto actualizado", "patient": patient}


@router.get("/list/priority")
def get_priority_list(
    limit: int = Query(100, ge=1, le=1000),
    min_priority: int = Query(50, ge=0, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of patients sorted by priority for contact.
    """
    from app.services.classifier import PatientClassifier

    patients = db.query(Patient).filter(
        Patient.is_active == True,
        Patient.is_contacted == False
    ).all()

    # Calculate priority for each patient
    patient_priorities = []
    for patient in patients:
        priority = PatientClassifier.calculate_priority_score(
            age=patient.age,
            is_pregnant=patient.is_pregnant,
            is_hypertensive=patient.is_hypertensive,
            is_diabetic=patient.is_diabetic,
            has_hypothyroidism=getattr(patient, 'has_hypothyroidism', False),
            has_copd=getattr(patient, 'has_copd', False),
            has_asthma=getattr(patient, 'has_asthma', False),
            has_ckd=getattr(patient, 'has_ckd', False),
            has_cardiovascular_disease=getattr(patient, 'has_cardiovascular_disease', False),
            has_cardiovascular_risk=patient.has_cardiovascular_risk,
            cardiovascular_risk_level=patient.cardiovascular_risk_level,
            last_control_date=patient.last_control_date
        )

        if priority >= min_priority:
            patient_priorities.append({
                'patient': patient,
                'priority_score': priority
            })

    # Sort by priority
    patient_priorities.sort(key=lambda x: x['priority_score'], reverse=True)

    # Limit results
    patient_priorities = patient_priorities[:limit]

    return {
        'total': len(patient_priorities),
        'patients': [
            {
                'id': item['patient'].id,
                'document_number': item['patient'].document_number,
                'full_name': item['patient'].full_name,
                'age': item['patient'].age,
                'phone': item['patient'].phone,
                'priority_score': item['priority_score'],
                'is_pregnant': item['patient'].is_pregnant,
                'is_hypertensive': item['patient'].is_hypertensive,
                'is_diabetic': item['patient'].is_diabetic,
                'has_cardiovascular_risk': item['patient'].has_cardiovascular_risk
            }
            for item in patient_priorities
        ]
    }
