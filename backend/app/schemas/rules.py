from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# =========================================================
# Control Rule Schemas
# =========================================================

class ControlRuleBase(BaseModel):
    rule_code: str = Field(..., description="Código único de la regla")
    rule_name: str = Field(..., description="Nombre de la regla")
    description: Optional[str] = None
    control_type: str = Field(..., description="Tipo de control")
    criteria: Dict[str, Any] = Field(..., description="Criterios de aplicación en formato JSON")
    frequency_days: Optional[int] = Field(None, description="Frecuencia en días")
    is_urgent_if_overdue: bool = True
    overdue_threshold_days: Optional[int] = None
    priority: int = Field(50, ge=0, le=100)
    rias_stage: Optional[str] = None
    rias_description: Optional[str] = None
    normative_reference: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None


class ControlRuleCreate(ControlRuleBase):
    created_by: Optional[str] = None


class ControlRuleUpdate(BaseModel):
    rule_name: Optional[str] = None
    description: Optional[str] = None
    control_type: Optional[str] = None
    criteria: Optional[Dict[str, Any]] = None
    frequency_days: Optional[int] = None
    is_urgent_if_overdue: Optional[bool] = None
    overdue_threshold_days: Optional[int] = None
    priority: Optional[int] = Field(None, ge=0, le=100)
    rias_stage: Optional[str] = None
    rias_description: Optional[str] = None
    normative_reference: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    updated_by: Optional[str] = None


class ControlRuleResponse(ControlRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


# =========================================================
# Alert Rule Schemas
# =========================================================

class AlertRuleBase(BaseModel):
    rule_code: str = Field(..., description="Código único de la regla")
    rule_name: str = Field(..., description="Nombre de la regla")
    description: Optional[str] = None
    alert_type: str = Field(..., description="Tipo de alerta")
    criteria: Dict[str, Any] = Field(..., description="Criterios de aplicación en formato JSON")
    frequency_days: Optional[int] = Field(None, description="Frecuencia en días")
    due_date_calculation: str = Field("frequency", description="Método de cálculo de fecha de vencimiento")
    priority: str = Field(..., description="Prioridad de la alerta")
    priority_score: int = Field(50, ge=0, le=100)
    threshold_config: Optional[Dict[str, Any]] = None
    reason_template: Optional[str] = None
    normative_reference: Optional[str] = None
    clinical_guidelines: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None


class AlertRuleCreate(AlertRuleBase):
    created_by: Optional[str] = None


class AlertRuleUpdate(BaseModel):
    rule_name: Optional[str] = None
    description: Optional[str] = None
    alert_type: Optional[str] = None
    criteria: Optional[Dict[str, Any]] = None
    frequency_days: Optional[int] = None
    due_date_calculation: Optional[str] = None
    priority: Optional[str] = None
    priority_score: Optional[int] = Field(None, ge=0, le=100)
    threshold_config: Optional[Dict[str, Any]] = None
    reason_template: Optional[str] = None
    normative_reference: Optional[str] = None
    clinical_guidelines: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    updated_by: Optional[str] = None


class AlertRuleResponse(AlertRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


# =========================================================
# RIAS Guideline Schemas
# =========================================================

class RiasGuidelineBase(BaseModel):
    guideline_code: str = Field(..., description="Código único de la guía")
    guideline_name: str = Field(..., description="Nombre de la guía")
    life_stage: str = Field(..., description="Etapa del curso de vida")
    official_description: str = Field(..., description="Descripción oficial según normativa")
    objectives: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    recommended_controls: Optional[Dict[str, Any]] = None
    screening_activities: Optional[Dict[str, Any]] = None
    normative_reference: str = Field(..., description="Referencia normativa")
    additional_references: Optional[str] = None
    clinical_notes: Optional[str] = None
    special_considerations: Optional[str] = None
    is_active: bool = True
    version: str = "1.0"


class RiasGuidelineCreate(RiasGuidelineBase):
    created_by: Optional[str] = None


class RiasGuidelineUpdate(BaseModel):
    guideline_name: Optional[str] = None
    life_stage: Optional[str] = None
    official_description: Optional[str] = None
    objectives: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    recommended_controls: Optional[Dict[str, Any]] = None
    screening_activities: Optional[Dict[str, Any]] = None
    normative_reference: Optional[str] = None
    additional_references: Optional[str] = None
    clinical_notes: Optional[str] = None
    special_considerations: Optional[str] = None
    is_active: Optional[bool] = None
    version: Optional[str] = None
    updated_by: Optional[str] = None


class RiasGuidelineResponse(RiasGuidelineBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        from_attributes = True


# =========================================================
# List Responses
# =========================================================

class ControlRuleList(BaseModel):
    total: int
    rules: List[ControlRuleResponse]


class AlertRuleList(BaseModel):
    total: int
    rules: List[AlertRuleResponse]


class RiasGuidelineList(BaseModel):
    total: int
    guidelines: List[RiasGuidelineResponse]
