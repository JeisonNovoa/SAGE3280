from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Patient, Control, Alert
from app.models.control import ControlTypeEnum, ControlStatusEnum
from app.models.alert import AlertTypeEnum, AlertStatusEnum
from typing import Optional
import pandas as pd
import io

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/patients")
def export_patients(
    age_group: Optional[str] = None,
    sex: Optional[str] = None,
    is_pregnant: Optional[bool] = None,
    is_hypertensive: Optional[bool] = None,
    is_diabetic: Optional[bool] = None,
    has_cardiovascular_risk: Optional[bool] = None,
    control_type: Optional[str] = None,
    alert_type: Optional[str] = None,
    is_contacted: Optional[bool] = None,
    format: str = Query("xlsx", regex="^(xlsx|csv)$"),
    db: Session = Depends(get_db)
):
    """
    Export filtered patient list to Excel or CSV.
    """
    query = db.query(Patient).filter(Patient.is_active == True)

    # Apply filters (same as in patients endpoint)
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

    patients = query.all()

    if not patients:
        raise HTTPException(status_code=404, detail="No se encontraron pacientes con los filtros aplicados")

    # Convert to DataFrame
    data = []
    for patient in patients:
        data.append({
            'Documento': patient.document_number,
            'Tipo de Documento': patient.document_type,
            'Nombre Completo': patient.full_name,
            'Edad': patient.age,
            'Sexo': patient.sex,
            'Grupo Etario': patient.age_group,
            'Teléfono': patient.phone,
            'Email': patient.email,
            'Dirección': patient.address,
            'Barrio / Vereda': patient.neighborhood,
            'Ciudad': patient.city,
            'EPS': patient.eps,
            'Tipo de Convenio': patient.tipo_convenio,
            'Diagnósticos': patient.diagnoses,
            'Hipertenso': 'Sí' if patient.is_hypertensive else 'No',
            'Diabético': 'Sí' if patient.is_diabetic else 'No',
            'Gestante': 'Sí' if patient.is_pregnant else 'No',
            'Riesgo CV': 'Sí' if patient.has_cardiovascular_risk else 'No',
            'Nivel Riesgo CV': patient.cardiovascular_risk_level,
            'Último Control General': patient.last_general_control_date,
            'Último Control 3280': patient.last_3280_control_date,
            'Último Control HTA': patient.last_hta_control_date,
            'Último Control DM': patient.last_dm_control_date,
            'Contactado': 'Sí' if patient.is_contacted else 'No',
            'Estado Contacto': patient.contact_status,
            'Intentos Contacto': patient.contact_attempts,
        })

    df = pd.DataFrame(data)

    # Create output file
    output = io.BytesIO()

    if format == 'xlsx':
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Pacientes')
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        filename = 'pacientes_sage3280.xlsx'
    else:  # csv
        df.to_csv(output, index=False, encoding='utf-8-sig')
        media_type = 'text/csv'
        filename = 'pacientes_sage3280.csv'

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=media_type,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@router.get("/controls")
def export_controls_by_type(
    control_type: str,
    status: Optional[str] = Query(None, regex="^(pendiente|completado|vencido)$"),
    format: str = Query("xlsx", regex="^(xlsx|csv)$"),
    db: Session = Depends(get_db)
):
    """
    Export list of patients needing specific control type.
    """
    query = db.query(Control).join(Patient).filter(
        Patient.is_active == True,
        Control.control_type == control_type
    )

    if status:
        query = query.filter(Control.status == status)

    controls = query.all()

    if not controls:
        raise HTTPException(status_code=404, detail="No se encontraron controles con los filtros aplicados")

    # Convert to DataFrame
    data = []
    for control in controls:
        patient = control.patient
        data.append({
            'Documento': patient.document_number,
            'Nombre Completo': patient.full_name,
            'Edad': patient.age,
            'Sexo': patient.sex,
            'Teléfono': patient.phone,
            'Email': patient.email,
            'Dirección': patient.address,
            'Control': control.control_name,
            'Estado': control.status,
            'Fecha Última': control.last_date,
            'Fecha Vencimiento': control.due_date,
            'Es Urgente': 'Sí' if control.is_urgent else 'No',
        })

    df = pd.DataFrame(data)

    # Create output file
    output = io.BytesIO()

    if format == 'xlsx':
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Controles')
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        filename = f'controles_{control_type}_sage3280.xlsx'
    else:  # csv
        df.to_csv(output, index=False, encoding='utf-8-sig')
        media_type = 'text/csv'
        filename = f'controles_{control_type}_sage3280.csv'

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=media_type,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )


@router.get("/alerts")
def export_alerts_by_type(
    alert_type: str,
    priority: Optional[str] = None,
    format: str = Query("xlsx", regex="^(xlsx|csv)$"),
    db: Session = Depends(get_db)
):
    """
    Export list of patients with specific alert type.
    """
    query = db.query(Alert).join(Patient).filter(
        Patient.is_active == True,
        Alert.alert_type == alert_type,
        Alert.status == AlertStatusEnum.ACTIVA
    )

    if priority:
        query = query.filter(Alert.priority == priority)

    alerts = query.all()

    if not alerts:
        raise HTTPException(status_code=404, detail="No se encontraron alertas con los filtros aplicados")

    # Convert to DataFrame
    data = []
    for alert in alerts:
        patient = alert.patient
        data.append({
            'Documento': patient.document_number,
            'Nombre Completo': patient.full_name,
            'Edad': patient.age,
            'Sexo': patient.sex,
            'Teléfono': patient.phone,
            'Email': patient.email,
            'Dirección': patient.address,
            'Alerta': alert.alert_name,
            'Prioridad': alert.priority,
            'Razón': alert.reason,
            'Criterios': alert.criteria,
            'Fecha Límite': alert.due_date,
        })

    df = pd.DataFrame(data)

    # Create output file
    output = io.BytesIO()

    if format == 'xlsx':
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Alertas')
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        filename = f'alertas_{alert_type}_sage3280.xlsx'
    else:  # csv
        df.to_csv(output, index=False, encoding='utf-8-sig')
        media_type = 'text/csv'
        filename = f'alertas_{alert_type}_sage3280.csv'

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=media_type,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
