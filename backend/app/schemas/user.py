"""
User Schemas - Validación y Serialización de Usuarios

Schemas Pydantic para operaciones con usuarios:
- Creación de usuarios
- Actualización de perfiles
- Respuestas de API
- Listados con paginación
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


# ============================================================================
# SCHEMAS BASE
# ============================================================================

class RoleBase(BaseModel):
    """Schema base para Role"""
    name: str = Field(..., description="Nombre del rol", min_length=2, max_length=50)
    display_name: str = Field(..., description="Nombre para mostrar", max_length=100)
    description: Optional[str] = Field(None, description="Descripción del rol")
    permissions: List[str] = Field(default_factory=list, description="Lista de permisos")
    is_active: bool = Field(True, description="Si el rol está activo")


class RoleResponse(RoleBase):
    """Schema de respuesta para Role"""
    id: int
    is_system_role: bool
    user_count: int = Field(0, description="Cantidad de usuarios con este rol")
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """Schema para lista de roles"""
    total: int
    items: List[RoleResponse]


# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserBase(BaseModel):
    """Schema base para User"""
    username: str = Field(
        ...,
        description="Nombre de usuario único",
        min_length=3,
        max_length=50,
        pattern=r'^[a-zA-Z0-9._-]+$'  # Permite letras, números, puntos, guiones y guiones bajos
    )
    email: EmailStr = Field(..., description="Email del usuario")
    full_name: str = Field(..., description="Nombre completo", min_length=2, max_length=200)
    is_active: bool = Field(True, description="Si el usuario está activo")

    @validator('username')
    def username_alphanumeric(cls, v):
        """Validar que username solo contenga caracteres permitidos"""
        # Remover caracteres permitidos y verificar que el resto sea alfanumérico
        cleaned = v.replace('_', '').replace('-', '').replace('.', '')
        if not cleaned.isalnum():
            raise ValueError('Username solo puede contener letras, números, puntos, guiones y guiones bajos')
        return v.lower()  # Convertir a minúsculas


class UserCreate(UserBase):
    """Schema para crear un nuevo usuario"""
    password: str = Field(
        ...,
        description="Contraseña del usuario",
        min_length=8,
        max_length=100
    )
    role_ids: List[int] = Field(
        default_factory=list,
        description="IDs de los roles a asignar"
    )

    @validator('password')
    def password_strength(cls, v):
        """Validar fortaleza de contraseña"""
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=200)
    is_active: Optional[bool] = None
    role_ids: Optional[List[int]] = None


class UserResponse(UserBase):
    """Schema de respuesta para User"""
    id: int
    is_superuser: bool
    roles: List[str] = Field(default_factory=list, description="Nombres de los roles")
    permissions: List[str] = Field(default_factory=list, description="Lista de permisos")
    created_at: datetime
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    is_locked: bool = False

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Schema de respuesta detallada para User"""
    updated_at: Optional[datetime] = None
    password_changed_at: datetime
    locked_until: Optional[datetime] = None


class UserListResponse(BaseModel):
    """Schema para lista paginada de usuarios"""
    total: int = Field(..., description="Total de usuarios")
    limit: int
    offset: int
    items: List[UserResponse]


# ============================================================================
# PASSWORD SCHEMAS
# ============================================================================

class PasswordChange(BaseModel):
    """Schema para cambio de contraseña"""
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(
        ...,
        description="Nueva contraseña",
        min_length=8,
        max_length=100
    )
    confirm_password: str = Field(..., description="Confirmación de nueva contraseña")

    @validator('new_password')
    def password_strength(cls, v):
        """Validar fortaleza de contraseña"""
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validar que las contraseñas coincidan"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v


class PasswordReset(BaseModel):
    """Schema para reset de contraseña (futuro)"""
    email: EmailStr = Field(..., description="Email del usuario")


class PasswordResetConfirm(BaseModel):
    """Schema para confirmar reset de contraseña (futuro)"""
    token: str = Field(..., description="Token de reset")
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v
