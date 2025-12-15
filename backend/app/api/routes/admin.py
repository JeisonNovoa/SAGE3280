"""
Admin routes for database management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Patient, Control, Alert, Upload, Exam

router = APIRouter(prefix="/admin", tags=["admin"])


@router.delete("/clear-database")
def clear_database(
    confirm: str,
    db: Session = Depends(get_db)
):
    """
    ⚠️ DANGER: Clear all data from database

    This endpoint deletes ALL patients, controls, alerts, uploads, and exams.
    Use with caution! Only for development/testing.

    Parameters:
    - confirm: Must be "YES_DELETE_ALL_DATA" to execute
    """
    if confirm != "YES_DELETE_ALL_DATA":
        raise HTTPException(
            status_code=400,
            detail="Confirmación incorrecta. Usa confirm=YES_DELETE_ALL_DATA para confirmar."
        )

    try:
        # Delete in correct order (respecting foreign keys)
        deleted_alerts = db.query(Alert).delete()
        deleted_controls = db.query(Control).delete()
        deleted_exams = db.query(Exam).delete()
        deleted_patients = db.query(Patient).delete()
        deleted_uploads = db.query(Upload).delete()

        db.commit()

        return {
            "message": "Base de datos limpiada exitosamente",
            "deleted": {
                "alerts": deleted_alerts,
                "controls": deleted_controls,
                "exams": deleted_exams,
                "patients": deleted_patients,
                "uploads": deleted_uploads
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al limpiar base de datos: {str(e)}")


@router.delete("/patients/all")
def delete_all_patients(
    confirm: str,
    db: Session = Depends(get_db)
):
    """
    ⚠️ Delete ALL patients and their related data

    This endpoint deletes all patients, controls, alerts, and exams.
    Uploads records are preserved.

    Parameters:
    - confirm: Must be "YES_DELETE_ALL_PATIENTS" to execute
    """
    if confirm != "YES_DELETE_ALL_PATIENTS":
        raise HTTPException(
            status_code=400,
            detail="Confirmación incorrecta. Usa confirm=YES_DELETE_ALL_PATIENTS para confirmar."
        )

    try:
        # Delete in correct order (respecting foreign keys)
        deleted_alerts = db.query(Alert).delete()
        deleted_controls = db.query(Control).delete()
        deleted_exams = db.query(Exam).delete()
        deleted_patients = db.query(Patient).delete()

        db.commit()

        return {
            "message": "Todos los pacientes fueron eliminados exitosamente",
            "deleted": {
                "patients": deleted_patients,
                "controls": deleted_controls,
                "alerts": deleted_alerts,
                "exams": deleted_exams
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar pacientes: {str(e)}")


@router.delete("/patients/upload/{upload_id}")
def delete_patients_by_upload(
    upload_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete all patients from a specific upload

    This endpoint deletes all patients that were created from a specific upload,
    along with their controls, alerts, and exams.

    Parameters:
    - upload_id: The ID of the upload whose patients should be deleted
    """
    # Verify upload exists
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail=f"Upload {upload_id} no encontrado")

    try:
        # Get patients from this upload
        patients = db.query(Patient).filter(Patient.upload_id == upload_id).all()
        patient_ids = [p.id for p in patients]

        if not patient_ids:
            return {
                "message": f"No hay pacientes asociados al upload {upload_id}",
                "deleted": {
                    "patients": 0,
                    "controls": 0,
                    "alerts": 0,
                    "exams": 0
                }
            }

        # Delete related data
        deleted_alerts = db.query(Alert).filter(Alert.patient_id.in_(patient_ids)).delete(synchronize_session=False)
        deleted_controls = db.query(Control).filter(Control.patient_id.in_(patient_ids)).delete(synchronize_session=False)
        deleted_exams = db.query(Exam).filter(Exam.patient_id.in_(patient_ids)).delete(synchronize_session=False)
        deleted_patients = db.query(Patient).filter(Patient.upload_id == upload_id).delete(synchronize_session=False)

        db.commit()

        return {
            "message": f"Pacientes del upload {upload_id} ({upload.original_filename}) eliminados exitosamente",
            "upload_info": {
                "id": upload.id,
                "filename": upload.original_filename,
                "created_at": upload.created_at
            },
            "deleted": {
                "patients": deleted_patients,
                "controls": deleted_controls,
                "alerts": deleted_alerts,
                "exams": deleted_exams
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar pacientes: {str(e)}")


@router.get("/uploads")
def list_uploads(db: Session = Depends(get_db)):
    """
    List all uploads with patient counts
    """
    try:
        uploads = db.query(Upload).order_by(Upload.created_at.desc()).all()

        uploads_data = []
        for upload in uploads:
            patient_count = db.query(Patient).filter(Patient.upload_id == upload.id).count()
            uploads_data.append({
                "id": upload.id,
                "filename": upload.original_filename,
                "created_at": upload.created_at,
                "status": upload.status,
                "total_rows": upload.total_rows,
                "success_rows": upload.success_rows,
                "error_rows": upload.error_rows,
                "current_patient_count": patient_count
            })

        return {
            "total": len(uploads_data),
            "uploads": uploads_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar uploads: {str(e)}")


@router.get("/database-stats")
def get_database_stats(db: Session = Depends(get_db)):
    """
    Get current database statistics
    """
    try:
        stats = {
            "patients": db.query(Patient).count(),
            "controls": db.query(Control).count(),
            "alerts": db.query(Alert).count(),
            "uploads": db.query(Upload).count(),
            "exams": db.query(Exam).count()
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")
