"""
Audit Logs Routes - Logs de Auditoría

Endpoints para consultar logs de auditoría del sistema.
Accesible por Admin y Médicos.

Endpoints:
- GET /audit/logs - Listar logs con filtros
- GET /audit/logs/{log_id} - Obtener log específico
- GET /audit/stats - Estadísticas de auditoría
- GET /audit/user/{user_id} - Logs de un usuario
- DELETE /audit/cleanup - Limpiar logs antiguos (solo Admin)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.dependencies.auth import require_admin, require_medical_staff, get_current_active_user
from app.models.user import User
from app.models.audit_log import AuditLog


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(
    prefix="/audit",
    tags=["Audit Logs"],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Prohibido"},
    }
)


# ============================================================================
# LIST AUDIT LOGS
# ============================================================================

@router.get(
    "/logs",
    summary="Listar logs de auditoría",
    description="Obtiene logs de auditoría con filtros. Admin y Médicos."
)
async def list_audit_logs(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    user_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    action: Optional[str] = Query(None, description="Filtrar por acción"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    resource_type: Optional[str] = Query(None, description="Filtrar por tipo de recurso"),
    date_from: Optional[datetime] = Query(None, description="Fecha desde"),
    date_to: Optional[datetime] = Query(None, description="Fecha hasta"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_medical_staff)
):
    """Lista logs de auditoría con filtros."""
    query = db.query(AuditLog)

    # Filtros
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))

    if category:
        query = query.filter(AuditLog.category == category)

    if status:
        query = query.filter(AuditLog.status == status)

    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)

    if date_from:
        query = query.filter(AuditLog.timestamp >= date_from)

    if date_to:
        query = query.filter(AuditLog.timestamp <= date_to)

    # Ordenar por timestamp descendente (más reciente primero)
    query = query.order_by(AuditLog.timestamp.desc())

    # Total count
    total = query.count()

    # Paginación
    logs = query.offset(offset).limit(limit).all()

    items = []
    for log in logs:
        items.append({
            "id": log.id,
            "user_id": log.user_id,
            "username": log.username,
            "action": log.action,
            "category": log.category,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "resource_name": log.resource_name,
            "timestamp": log.timestamp,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "details": log.details,
            "status": log.status,
            "error_message": log.error_message
        })

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": items
    }


# ============================================================================
# GET AUDIT LOG
# ============================================================================

@router.get(
    "/logs/{log_id}",
    summary="Obtener log específico",
    description="Obtiene información detallada de un log. Admin y Médicos."
)
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_medical_staff)
):
    """Obtiene un log por ID."""
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()

    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log no encontrado"
        )

    return {
        "id": log.id,
        "user_id": log.user_id,
        "username": log.username,
        "action": log.action,
        "category": log.category,
        "resource_type": log.resource_type,
        "resource_id": log.resource_id,
        "resource_name": log.resource_name,
        "timestamp": log.timestamp,
        "ip_address": log.ip_address,
        "user_agent": log.user_agent,
        "details": log.details,
        "status": log.status,
        "error_message": log.error_message
    }


# ============================================================================
# GET USER AUDIT LOGS
# ============================================================================

@router.get(
    "/user/{user_id}",
    summary="Logs de un usuario",
    description="Obtiene logs de auditoría de un usuario específico. Admin y Médicos."
)
async def get_user_audit_logs(
    user_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_medical_staff)
):
    """Obtiene logs de un usuario."""
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Obtener logs
    query = db.query(AuditLog).filter(AuditLog.user_id == user_id)
    query = query.order_by(AuditLog.timestamp.desc())

    total = query.count()
    logs = query.offset(offset).limit(limit).all()

    items = []
    for log in logs:
        items.append({
            "id": log.id,
            "action": log.action,
            "category": log.category,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "resource_name": log.resource_name,
            "timestamp": log.timestamp,
            "ip_address": log.ip_address,
            "status": log.status,
            "details": log.details
        })

    return {
        "user_id": user_id,
        "username": user.username,
        "total_logs": total,
        "offset": offset,
        "limit": limit,
        "logs": items
    }


# ============================================================================
# AUDIT STATS
# ============================================================================

@router.get(
    "/stats",
    summary="Estadísticas de auditoría",
    description="Obtiene estadísticas de logs de auditoría. Admin y Médicos."
)
async def get_audit_stats(
    days: int = Query(7, ge=1, le=365, description="Días a consultar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_medical_staff)
):
    """Obtiene estadísticas de auditoría."""
    since_date = datetime.now() - timedelta(days=days)

    query = db.query(AuditLog).filter(AuditLog.timestamp >= since_date)

    total_logs = query.count()

    # Por categoría
    from sqlalchemy import func
    category_stats = db.query(
        AuditLog.category,
        func.count(AuditLog.id).label('count')
    ).filter(AuditLog.timestamp >= since_date).group_by(AuditLog.category).all()

    # Por acción
    action_stats = db.query(
        AuditLog.action,
        func.count(AuditLog.id).label('count')
    ).filter(AuditLog.timestamp >= since_date).group_by(AuditLog.action).order_by(func.count(AuditLog.id).desc()).limit(10).all()

    # Por status
    status_stats = db.query(
        AuditLog.status,
        func.count(AuditLog.id).label('count')
    ).filter(AuditLog.timestamp >= since_date).group_by(AuditLog.status).all()

    # Por usuario (top 10)
    user_stats = db.query(
        AuditLog.username,
        func.count(AuditLog.id).label('count')
    ).filter(AuditLog.timestamp >= since_date).filter(AuditLog.username.isnot(None)).group_by(AuditLog.username).order_by(func.count(AuditLog.id).desc()).limit(10).all()

    # Logs recientes con errores
    error_logs = db.query(AuditLog).filter(
        AuditLog.timestamp >= since_date,
        AuditLog.status == 'error'
    ).order_by(AuditLog.timestamp.desc()).limit(10).all()

    return {
        "period_days": days,
        "since_date": since_date.isoformat(),
        "total_logs": total_logs,
        "by_category": [{"category": cat, "count": count} for cat, count in category_stats],
        "by_action": [{"action": action, "count": count} for action, count in action_stats],
        "by_status": [{"status": st, "count": count} for st, count in status_stats],
        "top_users": [{"username": user, "count": count} for user, count in user_stats],
        "recent_errors": [
            {
                "id": log.id,
                "action": log.action,
                "username": log.username,
                "timestamp": log.timestamp,
                "error_message": log.error_message
            }
            for log in error_logs
        ]
    }


# ============================================================================
# CLEANUP OLD LOGS
# ============================================================================

@router.delete(
    "/cleanup",
    summary="Limpiar logs antiguos",
    description="Elimina logs de auditoría antiguos. Solo Admin."
)
async def cleanup_old_logs(
    days: int = Query(90, ge=30, le=365, description="Eliminar logs más antiguos que X días"),
    dry_run: bool = Query(True, description="Si es True, solo muestra cuántos se eliminarían"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Limpia logs antiguos."""
    cutoff_date = datetime.now() - timedelta(days=days)

    # Contar logs a eliminar
    query = db.query(AuditLog).filter(AuditLog.timestamp < cutoff_date)
    count = query.count()

    if dry_run:
        return {
            "dry_run": True,
            "cutoff_date": cutoff_date.isoformat(),
            "logs_to_delete": count,
            "message": f"Se eliminarían {count} logs más antiguos que {days} días"
        }
    else:
        # Eliminar logs
        query.delete(synchronize_session=False)
        db.commit()

        # Registrar en audit log
        AuditLog.log_action(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            action="audit.cleanup",
            category="system",
            status="success",
            details={
                "cutoff_date": cutoff_date.isoformat(),
                "logs_deleted": count,
                "days": days
            }
        )

        return {
            "dry_run": False,
            "cutoff_date": cutoff_date.isoformat(),
            "logs_deleted": count,
            "message": f"Se eliminaron {count} logs exitosamente"
        }


# ============================================================================
# GET CATEGORIES AND ACTIONS
# ============================================================================

@router.get(
    "/metadata",
    summary="Obtener metadatos de auditoría",
    description="Obtiene categorías y acciones disponibles para filtros. Admin y Médicos."
)
async def get_audit_metadata(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_medical_staff)
):
    """Obtiene categorías y acciones disponibles."""
    from sqlalchemy import func

    # Categorías únicas
    categories = db.query(AuditLog.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]

    # Acciones únicas
    actions = db.query(AuditLog.action).distinct().all()
    actions = [action[0] for action in actions if action[0]]

    # Tipos de recursos únicos
    resource_types = db.query(AuditLog.resource_type).distinct().all()
    resource_types = [rt[0] for rt in resource_types if rt[0]]

    return {
        "categories": sorted(categories),
        "actions": sorted(actions),
        "resource_types": sorted(resource_types),
        "statuses": ["success", "error", "failed", "blocked"]
    }
