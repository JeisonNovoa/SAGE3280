"""
Auth Schemas - Validación y Serialización de Autenticación

Schemas Pydantic para operaciones de autenticación:
- Login
- Tokens JWT
- Refresh tokens
- Logout
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


# ============================================================================
# LOGIN SCHEMAS
# ============================================================================

class UserLogin(BaseModel):
    """Schema para login de usuario"""
    username: str = Field(
        ...,
        description="Username o email del usuario",
        min_length=3,
        max_length=255
    )
    password: str = Field(
        ...,
        description="Contraseña del usuario",
        min_length=1,
        max_length=100
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "Admin123!"
            }
        }


# ============================================================================
# TOKEN SCHEMAS
# ============================================================================

class Token(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str = Field(..., description="Token de acceso JWT")
    refresh_token: str = Field(..., description="Token de refresco JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Segundos hasta la expiración del access token")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class TokenPayload(BaseModel):
    """Schema para payload de token JWT (claims)"""
    sub: int = Field(..., description="Subject - User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email del usuario")
    roles: List[str] = Field(default_factory=list, description="Roles del usuario")
    permissions: List[str] = Field(default_factory=list, description="Permisos del usuario")
    exp: int = Field(..., description="Expiration time (timestamp Unix)")
    iat: int = Field(..., description="Issued at (timestamp Unix)")
    jti: str = Field(..., description="JWT ID (identificador único)")
    type: str = Field(..., description="Tipo de token: access o refresh")


class TokenRefresh(BaseModel):
    """Schema para refresh de token"""
    refresh_token: str = Field(..., description="Refresh token válido")

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class TokenRefreshResponse(BaseModel):
    """Schema para respuesta de refresh token"""
    access_token: str = Field(..., description="Nuevo token de acceso JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Segundos hasta la expiración")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class TokenBlacklistRequest(BaseModel):
    """Schema para invalidar un token (logout)"""
    access_token: Optional[str] = Field(None, description="Access token a invalidar")
    refresh_token: Optional[str] = Field(None, description="Refresh token a invalidar")
    logout_all_devices: bool = Field(
        False,
        description="Si es True, invalida todos los tokens del usuario"
    )


# ============================================================================
# LOGIN RESPONSE SCHEMAS
# ============================================================================

class LoginResponse(BaseModel):
    """Schema completo de respuesta para login exitoso"""
    access_token: str = Field(..., description="Token de acceso JWT")
    refresh_token: str = Field(..., description="Token de refresco JWT")
    token_type: str = Field(default="bearer")
    expires_in: int = Field(..., description="Segundos hasta expiración")
    user: dict = Field(..., description="Información del usuario")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@sage3280.com",
                    "full_name": "Administrador SAGE",
                    "roles": ["admin"],
                    "permissions": ["*"],
                    "is_superuser": True
                }
            }
        }


class LogoutResponse(BaseModel):
    """Schema de respuesta para logout"""
    message: str = Field(..., description="Mensaje de confirmación")
    tokens_invalidated: int = Field(..., description="Número de tokens invalidados")

    class Config:
        schema_extra = {
            "example": {
                "message": "Logout exitoso",
                "tokens_invalidated": 2
            }
        }


# ============================================================================
# VALIDATION SCHEMAS
# ============================================================================

class TokenValidationRequest(BaseModel):
    """Schema para validar un token"""
    token: str = Field(..., description="Token a validar")


class TokenValidationResponse(BaseModel):
    """Schema de respuesta para validación de token"""
    valid: bool = Field(..., description="Si el token es válido")
    expired: bool = Field(False, description="Si el token expiró")
    blacklisted: bool = Field(False, description="Si el token está invalidado")
    user_id: Optional[int] = Field(None, description="ID del usuario si el token es válido")
    expires_at: Optional[datetime] = Field(None, description="Fecha de expiración")
    message: Optional[str] = Field(None, description="Mensaje de error si aplica")

    class Config:
        schema_extra = {
            "example": {
                "valid": True,
                "expired": False,
                "blacklisted": False,
                "user_id": 1,
                "expires_at": "2026-01-01T18:00:00Z",
                "message": None
            }
        }


# ============================================================================
# CURRENT USER SCHEMA
# ============================================================================

class CurrentUser(BaseModel):
    """Schema para el usuario actual (del token)"""
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    roles: List[str]
    permissions: List[str]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================================
# ERROR SCHEMAS
# ============================================================================

class AuthError(BaseModel):
    """Schema para errores de autenticación"""
    error: str = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje de error")
    details: Optional[dict] = Field(None, description="Detalles adicionales")

    class Config:
        schema_extra = {
            "example": {
                "error": "invalid_credentials",
                "message": "Usuario o contraseña incorrectos",
                "details": {
                    "attempts_remaining": 3,
                    "locked_until": None
                }
            }
        }
