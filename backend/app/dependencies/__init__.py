"""
Dependencies module - FastAPI dependencies for authentication
"""
from app.dependencies.auth import (
    get_current_user,
    get_current_active_user,
    require_role,
    require_permission,
    get_db
)

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "require_permission",
    "get_db",
]
