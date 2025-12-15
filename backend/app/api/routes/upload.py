from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Patient, Upload, Control, Alert, Exam
from app.models.upload import UploadStatusEnum
from app.models.control import ControlStatusEnum
from app.models.alert import AlertStatusEnum
from app.services import ExcelProcessor, PatientClassifier, AlertGenerator
from app.schemas import UploadResponse, UploadStats
from datetime import datetime, date
import os
import uuid
from typing import List, Dict

router = APIRouter(prefix="/upload", tags=["upload"])

# Directory for storing uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=UploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an Excel file with patient data.
    The file will be processed in the background.
    """
    # Validate file extension
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(
            status_code=400,
            detail="Formato de archivo no válido. Solo se permiten archivos .xlsx, .xls, .csv"
        )

    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar archivo: {str(e)}")

    # Create upload record
    upload = Upload(
        filename=unique_filename,
        original_filename=file.filename,
        file_size=len(content),
        file_path=file_path,
        status=UploadStatusEnum.PENDING
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)

    # Process file in background
    background_tasks.add_task(process_upload, upload.id, file_path, db)

    return upload


def process_upload(upload_id: int, file_path: str, db: Session):
    """
    Background task to process uploaded file.
    """
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        return

    try:
        # Update status to processing
        upload.status = UploadStatusEnum.PROCESSING
        db.commit()

        # Process Excel file
        processor = ExcelProcessor()
        success, message, row_count = processor.load_file(file_path)

        if not success:
            upload.status = UploadStatusEnum.FAILED
            upload.error_message = message
            db.commit()
            return

        upload.total_rows = row_count

        # Extract patient data
        patients_data = processor.extract_patients()
        upload.processed_rows = len(patients_data)

        success_count = 0
        error_count = 0
        updated_count = 0
        created_count = 0
        duplicate_docs = []

        # Process each patient
        for patient_data in patients_data:
            try:
                # Check if patient already exists by document number
                existing_patient = db.query(Patient).filter(
                    Patient.document_number == patient_data['document_number']
                ).first()

                if existing_patient:
                    # Log duplicate for statistics
                    duplicate_docs.append(patient_data['document_number'])

                    # Update existing patient with new data
                    for key, value in patient_data.items():
                        # Only update if new value is not None/empty
                        if value is not None and value != '':
                            setattr(existing_patient, key, value)

                    existing_patient.upload_id = upload_id
                    existing_patient.updated_at = datetime.now()
                    patient = existing_patient
                    updated_count += 1
                else:
                    # Create new patient
                    patient = Patient(**patient_data, upload_id=upload_id)
                    db.add(patient)
                    created_count += 1

                db.flush()  # Get patient ID

                # Classify patient
                age_group = PatientClassifier.classify_age_group(patient.age)
                patient.age_group = age_group

                # Calculate cardiovascular risk
                has_cv_risk, cv_risk_level = PatientClassifier.calculate_cardiovascular_risk(
                    age=patient.age,
                    sex=patient.sex,
                    is_hypertensive=patient.is_hypertensive,
                    is_diabetic=patient.is_diabetic
                )
                patient.has_cardiovascular_risk = has_cv_risk
                patient.cardiovascular_risk_level = cv_risk_level

                # Generate controls
                required_controls = PatientClassifier.determine_required_controls(
                    age=patient.age,
                    sex=patient.sex,
                    is_pregnant=patient.is_pregnant,
                    is_hypertensive=patient.is_hypertensive,
                    is_diabetic=patient.is_diabetic,
                    has_hypothyroidism=getattr(patient, 'has_hypothyroidism', False),
                    has_copd=getattr(patient, 'has_copd', False),
                    has_asthma=getattr(patient, 'has_asthma', False),
                    has_ckd=getattr(patient, 'has_ckd', False),
                    has_cardiovascular_disease=getattr(patient, 'has_cardiovascular_disease', False),
                    has_cardiovascular_risk=has_cv_risk,
                    last_control_date=patient.last_control_date
                )

                # Delete existing controls for this patient (to avoid duplicates)
                db.query(Control).filter(Control.patient_id == patient.id).delete()

                # Create control records
                for control_data in required_controls:
                    control = Control(
                        patient_id=patient.id,
                        status=ControlStatusEnum.PENDIENTE,
                        **control_data
                    )
                    db.add(control)

                # Get patient's exam history to calculate due dates
                last_exam_dates = {}
                patient_exams = db.query(Exam).filter(Exam.patient_id == patient.id).all()
                for exam in patient_exams:
                    exam_type_key = exam.exam_type.value  # e.g., "citologia", "mamografia"
                    # Keep only the most recent exam date for each type
                    if exam_type_key not in last_exam_dates or exam.exam_date > last_exam_dates[exam_type_key]:
                        last_exam_dates[exam_type_key] = exam.exam_date

                # Generate alerts with exam history context
                alerts_data = AlertGenerator.generate_alerts(
                    age=patient.age,
                    sex=patient.sex,
                    is_pregnant=patient.is_pregnant,
                    is_hypertensive=patient.is_hypertensive,
                    is_diabetic=patient.is_diabetic,
                    has_hypothyroidism=getattr(patient, 'has_hypothyroidism', False),
                    has_copd=getattr(patient, 'has_copd', False),
                    has_asthma=getattr(patient, 'has_asthma', False),
                    has_ckd=getattr(patient, 'has_ckd', False),
                    has_cardiovascular_disease=getattr(patient, 'has_cardiovascular_disease', False),
                    has_cardiovascular_risk=has_cv_risk,
                    cardiovascular_risk_level=cv_risk_level,
                    last_exam_dates=last_exam_dates
                )

                # Delete existing alerts for this patient
                db.query(Alert).filter(Alert.patient_id == patient.id).delete()

                # Create alert records
                for alert_data in alerts_data:
                    alert = Alert(
                        patient_id=patient.id,
                        created_date=date.today(),
                        status=AlertStatusEnum.ACTIVA,
                        **alert_data
                    )
                    db.add(alert)

                success_count += 1

            except Exception as e:
                error_count += 1
                print(f"Error processing patient {patient_data.get('document_number')}: {str(e)}")
                continue

        # Update upload record with detailed statistics
        upload.success_rows = success_count
        upload.error_rows = error_count
        upload.status = UploadStatusEnum.COMPLETED
        upload.completed_at = datetime.now()

        # Log duplicate statistics
        if duplicate_docs:
            duplicate_msg = f"Procesados: {created_count} nuevos, {updated_count} actualizados"
            print(f"📊 Duplicados encontrados: {len(duplicate_docs)}")
            print(f"📊 {duplicate_msg}")
            upload.error_message = duplicate_msg if not upload.error_message else upload.error_message

        db.commit()
        print(f"✅ Upload {upload_id} completado: {success_count} exitosos, {error_count} errores")

    except Exception as e:
        upload.status = UploadStatusEnum.FAILED
        upload.error_message = str(e)
        db.commit()


@router.get("/{upload_id}", response_model=UploadResponse)
def get_upload_status(upload_id: int, db: Session = Depends(get_db)):
    """
    Get status of an upload.
    """
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload no encontrado")
    return upload


@router.get("/{upload_id}/stats", response_model=UploadStats)
def get_upload_stats(upload_id: int, db: Session = Depends(get_db)):
    """
    Get statistics for a specific upload.
    """
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload no encontrado")

    # Get patients from this upload
    patients = db.query(Patient).filter(Patient.upload_id == upload_id).all()

    # Calculate stats
    patients_by_age_group = {}
    patients_by_sex = {}
    patients_with_risks = {
        'hypertensive': 0,
        'diabetic': 0,
        'pregnant': 0,
        'cardiovascular': 0
    }

    for patient in patients:
        # Age group
        if patient.age_group:
            patients_by_age_group[patient.age_group] = patients_by_age_group.get(patient.age_group, 0) + 1

        # Sex
        if patient.sex:
            patients_by_sex[patient.sex] = patients_by_sex.get(patient.sex, 0) + 1

        # Risks
        if patient.is_hypertensive:
            patients_with_risks['hypertensive'] += 1
        if patient.is_diabetic:
            patients_with_risks['diabetic'] += 1
        if patient.is_pregnant:
            patients_with_risks['pregnant'] += 1
        if patient.has_cardiovascular_risk:
            patients_with_risks['cardiovascular'] += 1

    # Count controls and alerts
    controls_count = db.query(Control).join(Patient).filter(Patient.upload_id == upload_id).count()
    alerts_count = db.query(Alert).join(Patient).filter(Patient.upload_id == upload_id).count()

    # Processing time
    processing_time = 0
    if upload.completed_at and upload.created_at:
        processing_time = (upload.completed_at - upload.created_at).total_seconds()

    return UploadStats(
        upload_id=upload_id,
        total_patients=len(patients),
        patients_by_age_group=patients_by_age_group,
        patients_by_sex=patients_by_sex,
        patients_with_risks=patients_with_risks,
        controls_generated=controls_count,
        alerts_generated=alerts_count,
        processing_time_seconds=processing_time
    )
