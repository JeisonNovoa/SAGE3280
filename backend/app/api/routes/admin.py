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
