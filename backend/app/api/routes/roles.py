"""
Roles Management Routes - Gestión de Roles

Endpoints para administración de roles (solo Admin).

Endpoints:
- GET /roles - Listar roles
- GET /roles/{role_id} - Obtener rol
- GET /roles/{role_id}/users - Obtener usuarios con rol
- POST /roles - Crear rol personalizado
- PUT /roles/{role_id} - Actualizar rol
- DELETE /roles/{role_id} - Eliminar rol personalizado
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies.auth import require_admin
from app.models.user import User
from app.models.role import Role
from app.models.audit_log import AuditLog
from app.schemas.user import RoleResponse, RoleListResponse, RoleBase


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(
    prefix="/roles",
    tags=["Role Management"],
    dependencies=[Depends(require_admin)],  # Todos los endpoints requieren admin
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Prohibido - Solo Admin"},
    }
)


# ============================================================================
# LIST ROLES
# ============================================================================

@router.get(
    "",
    response_model=RoleListResponse,
    summary="Listar roles",
    description="Obtiene lista de roles del sistema. Solo Admin."
)
async def list_roles(
    include_inactive: bool = Query(False, description="Incluir roles inactivos"),
    db: Session = Depends(get_db)
):
    """Lista todos los roles."""
    query = db.query(Role)

    if not include_inactive:
        query = query.filter(Role.is_active == True)

    roles = query.all()

    items = []
    for role in roles:
        user_count = db.query(User).join(User.roles).filter(Role.id == role.id).count()
        items.append({
            "id": role.id,
            "name": role.name,
            "display_name": role.display_name,
            "description": role.description,
            "permissions": role.get_permissions(),
            "is_active": role.is_active,
            "is_system_role": role.is_system_role,
            "user_count": user_count,
            "created_at": role.created_at,
            "updated_at": role.updated_at
        })

    return {
        "total": len(items),
        "items": items
    }


# ============================================================================
# GET ROLE
# ============================================================================

@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Obtener rol",
    description="Obtiene información detallada de un rol. Solo Admin."
)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un rol por ID."""
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    user_count = db.query(User).join(User.roles).filter(Role.id == role.id).count()

    return {
        "id": role.id,
        "name": role.name,
        "display_name": role.display_name,
        "description": role.description,
        "permissions": role.get_permissions(),
        "is_active": role.is_active,
        "is_system_role": role.is_system_role,
        "user_count": user_count,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }


# ============================================================================
# GET ROLE USERS
# ============================================================================

@router.get(
    "/{role_id}/users",
    summary="Obtener usuarios con rol",
    description="Lista usuarios que tienen un rol específico. Solo Admin."
)
async def get_role_users(
    role_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene usuarios que tienen un rol."""
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    users = db.query(User).join(User.roles).filter(Role.id == role_id).all()

    return {
        "role_id": role.id,
        "role_name": role.name,
        "role_display_name": role.display_name,
        "user_count": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active
            }
            for user in users
        ]
    }


# ============================================================================
# CREATE ROLE
# ============================================================================

@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear rol personalizado",
    description="Crea un nuevo rol personalizado. Solo Admin."
)
async def create_role(
    role_data: RoleBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Crea un nuevo rol personalizado."""
    # Verificar si el nombre ya existe
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre"
        )

    # Crear rol
    new_role = Role(
        name=role_data.name,
        display_name=role_data.display_name,
        description=role_data.description,
        permissions=role_data.permissions,
        is_active=role_data.is_active,
        is_system_role=False  # Roles personalizados no son del sistema
    )

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="roles.created",
        category="role_management",
        resource_type="role",
        resource_id=new_role.id,
        resource_name=new_role.name,
        status="success",
        details={
            "name": new_role.name,
            "permissions": new_role.get_permissions()
        }
    )

    return {
        "id": new_role.id,
        "name": new_role.name,
        "display_name": new_role.display_name,
        "description": new_role.description,
        "permissions": new_role.get_permissions(),
        "is_active": new_role.is_active,
        "is_system_role": new_role.is_system_role,
        "user_count": 0,
        "created_at": new_role.created_at,
        "updated_at": new_role.updated_at
    }


# ============================================================================
# UPDATE ROLE
# ============================================================================

@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Actualizar rol",
    description="Actualiza un rol personalizado. Solo Admin. No se pueden editar roles del sistema."
)
async def update_role(
    role_id: int,
    role_data: RoleBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Actualiza un rol personalizado."""
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    # No permitir editar roles del sistema
    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pueden modificar roles del sistema"
        )

    # Verificar nombre único (si cambió)
    if role_data.name != role.name:
        existing = db.query(Role).filter(
            Role.name == role_data.name,
            Role.id != role_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un rol con ese nombre"
            )

    # Actualizar campos
    role.name = role_data.name
    role.display_name = role_data.display_name
    role.description = role_data.description
    role.permissions = role_data.permissions
    role.is_active = role_data.is_active

    from datetime import datetime
    role.updated_at = datetime.now()

    db.commit()
    db.refresh(role)

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="roles.updated",
        category="role_management",
        resource_type="role",
        resource_id=role.id,
        resource_name=role.name,
        status="success",
        details={
            "changes": role_data.dict()
        }
    )

    user_count = db.query(User).join(User.roles).filter(Role.id == role.id).count()

    return {
        "id": role.id,
        "name": role.name,
        "display_name": role.display_name,
        "description": role.description,
        "permissions": role.get_permissions(),
        "is_active": role.is_active,
        "is_system_role": role.is_system_role,
        "user_count": user_count,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }


# ============================================================================
# DELETE ROLE
# ============================================================================

@router.delete(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar rol personalizado",
    description="Elimina un rol personalizado. Solo Admin. No se pueden eliminar roles del sistema."
)
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Elimina un rol personalizado."""
    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )

    # No permitir eliminar roles del sistema
    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pueden eliminar roles del sistema"
        )

    # Verificar si hay usuarios con este rol
    user_count = db.query(User).join(User.roles).filter(Role.id == role_id).count()
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar el rol. {user_count} usuarios lo tienen asignado."
        )

    role_name = role.name

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="roles.deleted",
        category="role_management",
        resource_type="role",
        resource_id=role.id,
        resource_name=role_name,
        status="success"
    )

    db.delete(role)
    db.commit()

    return {
        "message": f"Rol {role_name} eliminado exitosamente",
        "deleted_role_id": role_id
    }


# ============================================================================
# GET AVAILABLE PERMISSIONS
# ============================================================================

@router.get(
    "/permissions/list",
    summary="Listar permisos disponibles",
    description="Obtiene lista de permisos disponibles en el sistema. Solo Admin."
)
async def list_available_permissions():
    """Lista todos los permisos disponibles."""
    permissions = {
        "patients": [
            "patients.create",
            "patients.read",
            "patients.update",
            "patients.delete",
            "patients.export",
            "patients.contact"
        ],
        "consultations": [
            "consultations.create",
            "consultations.read",
            "consultations.update"
        ],
        "controls": [
            "controls.create",
            "controls.read",
            "controls.update"
        ],
        "alerts": [
            "alerts.read",
            "alerts.update",
            "alerts.create"
        ],
        "reports": [
            "reports.read",
            "reports.create",
            "reports.export"
        ],
        "upload": [
            "upload.create",
            "upload.read"
        ],
        "catalogs": [
            "catalogs.read",
            "catalogs.manage"
        ],
        "stats": [
            "stats.read"
        ],
        "users": [
            "users.create",
            "users.read",
            "users.update",
            "users.delete"
        ],
        "roles": [
            "roles.create",
            "roles.read",
            "roles.update",
            "roles.delete"
        ],
        "audit": [
            "audit.read"
        ],
        "admin": [
            "*"
        ]
    }

    return {
        "permissions": permissions,
        "total_permissions": sum(len(v) for v in permissions.values()),
        "categories": list(permissions.keys())
    }
