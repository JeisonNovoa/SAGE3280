"""
Users Management Routes - Gestión de Usuarios

Endpoints para administración de usuarios (solo Admin).

Endpoints:
- GET /users - Listar usuarios
- POST /users - Crear usuario
- GET /users/{user_id} - Obtener usuario
- PUT /users/{user_id} - Actualizar usuario
- DELETE /users/{user_id} - Eliminar usuario
- PUT /users/{user_id}/roles - Asignar roles
- PUT /users/{user_id}/activate - Activar/desactivar
- POST /users/{user_id}/reset-password - Resetear contraseña
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies.auth import require_admin, get_current_active_user
from app.models.user import User
from app.models.role import Role
from app.models.audit_log import AuditLog
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserDetailResponse,
    UserListResponse
)
from app.core.security import get_password_hash


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(
    prefix="/users",
    tags=["User Management"],
    dependencies=[Depends(require_admin)],  # Todos los endpoints requieren admin
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Prohibido - Solo Admin"},
    }
)


# ============================================================================
# LIST USERS
# ============================================================================

@router.get(
    "",
    response_model=UserListResponse,
    summary="Listar usuarios",
    description="Obtiene lista paginada de usuarios del sistema. Solo Admin."
)
async def list_users(
    offset: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número de registros a retornar"),
    search: Optional[str] = Query(None, description="Buscar por username, email o nombre"),
    role: Optional[str] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista usuarios con paginación y filtros."""
    query = db.query(User)

    # Filtro de búsqueda
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.username.ilike(search_filter)) |
            (User.email.ilike(search_filter)) |
            (User.full_name.ilike(search_filter))
        )

    # Filtro por rol
    if role:
        query = query.join(User.roles).filter(Role.name == role)

    # Filtro por estado
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    # Total count
    total = query.count()

    # Paginación
    users = query.offset(offset).limit(limit).all()

    # Convertir a respuesta
    items = []
    for user in users:
        items.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "roles": [role.name for role in user.roles],
            "permissions": user.get_permissions(),
            "created_at": user.created_at,
            "last_login": user.last_login,
            "failed_login_attempts": user.failed_login_attempts,
            "is_locked": user.is_locked()
        })

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }


# ============================================================================
# CREATE USER
# ============================================================================

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario en el sistema. Solo Admin."
)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Crea un nuevo usuario."""
    # Verificar si username ya existe
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username ya existe"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya existe"
            )

    # Crear usuario
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        is_active=user_data.is_active
    )

    # Asignar roles
    if user_data.role_ids:
        roles = db.query(Role).filter(Role.id.in_(user_data.role_ids)).all()
        if len(roles) != len(user_data.role_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno o más roles no existen"
            )
        new_user.roles = roles

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="users.created",
        category="user_management",
        resource_type="user",
        resource_id=new_user.id,
        resource_name=new_user.username,
        status="success",
        details={
            "username": new_user.username,
            "email": new_user.email,
            "roles": [role.name for role in new_user.roles]
        }
    )

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "is_active": new_user.is_active,
        "is_superuser": new_user.is_superuser,
        "roles": [role.name for role in new_user.roles],
        "permissions": new_user.get_permissions(),
        "created_at": new_user.created_at,
        "last_login": new_user.last_login,
        "failed_login_attempts": new_user.failed_login_attempts,
        "is_locked": new_user.is_locked()
    }


# ============================================================================
# GET USER
# ============================================================================

@router.get(
    "/{user_id}",
    response_model=UserDetailResponse,
    summary="Obtener usuario",
    description="Obtiene información detallada de un usuario. Solo Admin."
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un usuario por ID."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "roles": [role.name for role in user.roles],
        "permissions": user.get_permissions(),
        "created_at": user.created_at,
        "last_login": user.last_login,
        "failed_login_attempts": user.failed_login_attempts,
        "is_locked": user.is_locked(),
        "updated_at": user.updated_at,
        "password_changed_at": user.password_changed_at,
        "locked_until": user.locked_until
    }


# ============================================================================
# UPDATE USER
# ============================================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza información de un usuario. Solo Admin."
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Actualiza un usuario."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Actualizar campos
    if user_data.email is not None:
        # Verificar que email no esté en uso
        existing = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya está en uso"
            )
        user.email = user_data.email

    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    # Actualizar roles
    if user_data.role_ids is not None:
        roles = db.query(Role).filter(Role.id.in_(user_data.role_ids)).all()
        if len(roles) != len(user_data.role_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno o más roles no existen"
            )
        user.roles = roles

    from datetime import datetime
    user.updated_at = datetime.now()
    user.updated_by_id = current_user.id

    db.commit()
    db.refresh(user)

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="users.updated",
        category="user_management",
        resource_type="user",
        resource_id=user.id,
        resource_name=user.username,
        status="success",
        details={
            "changes": user_data.dict(exclude_unset=True)
        }
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "roles": [role.name for role in user.roles],
        "permissions": user.get_permissions(),
        "created_at": user.created_at,
        "last_login": user.last_login,
        "failed_login_attempts": user.failed_login_attempts,
        "is_locked": user.is_locked()
    }


# ============================================================================
# DELETE USER
# ============================================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema. Solo Admin."
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Elimina un usuario."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # No permitir eliminar a sí mismo
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propia cuenta"
        )

    # No permitir eliminar superusers
    if user.is_superuser and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar superusuarios"
        )

    username = user.username

    # Audit log antes de eliminar
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="users.deleted",
        category="user_management",
        resource_type="user",
        resource_id=user.id,
        resource_name=username,
        status="success"
    )

    db.delete(user)
    db.commit()

    return {
        "message": f"Usuario {username} eliminado exitosamente",
        "deleted_user_id": user_id
    }


# ============================================================================
# RESET PASSWORD
# ============================================================================

@router.post(
    "/{user_id}/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Resetear contraseña",
    description="Resetea la contraseña de un usuario. Solo Admin."
)
async def reset_user_password(
    user_id: int,
    new_password: str = Query(..., min_length=8, description="Nueva contraseña"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Resetea la contraseña de un usuario."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Actualizar contraseña
    from datetime import datetime
    user.hashed_password = get_password_hash(new_password)
    user.password_changed_at = datetime.now()
    user.refresh_token = None  # Invalidar refresh token
    user.failed_login_attempts = 0  # Resetear intentos fallidos
    user.locked_until = None  # Desbloquear cuenta

    db.commit()

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action="users.password_reset",
        category="user_management",
        resource_type="user",
        resource_id=user.id,
        resource_name=user.username,
        status="success"
    )

    return {
        "message": f"Contraseña de {user.username} reseteada exitosamente",
        "password_changed_at": user.password_changed_at.isoformat()
    }


# ============================================================================
# ACTIVATE/DEACTIVATE USER
# ============================================================================

@router.put(
    "/{user_id}/activate",
    response_model=UserResponse,
    summary="Activar/Desactivar usuario",
    description="Activa o desactiva un usuario. Solo Admin."
)
async def toggle_user_activation(
    user_id: int,
    activate: bool = Query(..., description="True para activar, False para desactivar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Activa o desactiva un usuario."""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # No permitir desactivar a sí mismo
    if user.id == current_user.id and not activate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta"
        )

    user.is_active = activate

    from datetime import datetime
    user.updated_at = datetime.now()
    user.updated_by_id = current_user.id

    db.commit()
    db.refresh(user)

    # Audit log
    AuditLog.log_action(
        db=db,
        user_id=current_user.id,
        username=current_user.username,
        action=f"users.{'activated' if activate else 'deactivated'}",
        category="user_management",
        resource_type="user",
        resource_id=user.id,
        resource_name=user.username,
        status="success"
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "roles": [role.name for role in user.roles],
        "permissions": user.get_permissions(),
        "created_at": user.created_at,
        "last_login": user.last_login,
        "failed_login_attempts": user.failed_login_attempts,
        "is_locked": user.is_locked()
    }
