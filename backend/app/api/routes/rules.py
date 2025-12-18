from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ControlRule, AlertRule, RiasGuideline
from app.schemas.rules import (
    ControlRuleCreate, ControlRuleUpdate, ControlRuleResponse, ControlRuleList,
    AlertRuleCreate, AlertRuleUpdate, AlertRuleResponse, AlertRuleList,
    RiasGuidelineCreate, RiasGuidelineUpdate, RiasGuidelineResponse, RiasGuidelineList
)
from typing import Optional

router = APIRouter(prefix="/rules", tags=["rules"])


# =========================================================
# Control Rules Endpoints
# =========================================================

@router.post("/controls", response_model=ControlRuleResponse)
def create_control_rule(rule: ControlRuleCreate, db: Session = Depends(get_db)):
    """
    Create a new control rule.
    """
    # Check if rule_code already exists
    existing = db.query(ControlRule).filter(ControlRule.rule_code == rule.rule_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Regla con código '{rule.rule_code}' ya existe")

    db_rule = ControlRule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.get("/controls", response_model=ControlRuleList)
def list_control_rules(
    is_active: Optional[bool] = None,
    rias_stage: Optional[str] = None,
    control_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all control rules with optional filters.
    """
    query = db.query(ControlRule)

    if is_active is not None:
        query = query.filter(ControlRule.is_active == is_active)
    if rias_stage:
        query = query.filter(ControlRule.rias_stage == rias_stage)
    if control_type:
        query = query.filter(ControlRule.control_type == control_type)

    total = query.count()
    rules = query.offset(skip).limit(limit).all()

    return ControlRuleList(total=total, rules=rules)


@router.get("/controls/{rule_id}", response_model=ControlRuleResponse)
def get_control_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Get a specific control rule by ID.
    """
    rule = db.query(ControlRule).filter(ControlRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla de control no encontrada")
    return rule


@router.put("/controls/{rule_id}", response_model=ControlRuleResponse)
def update_control_rule(rule_id: int, rule_update: ControlRuleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing control rule.
    """
    rule = db.query(ControlRule).filter(ControlRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla de control no encontrada")

    update_data = rule_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/controls/{rule_id}")
def delete_control_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Delete a control rule.
    """
    rule = db.query(ControlRule).filter(ControlRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla de control no encontrada")

    db.delete(rule)
    db.commit()
    return {"message": f"Regla de control '{rule.rule_code}' eliminada exitosamente"}


# =========================================================
# Alert Rules Endpoints
# =========================================================

@router.post("/alerts", response_model=AlertRuleResponse)
def create_alert_rule(rule: AlertRuleCreate, db: Session = Depends(get_db)):
    """
    Create a new alert rule.
    """
    # Check if rule_code already exists
    existing = db.query(AlertRule).filter(AlertRule.rule_code == rule.rule_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Regla con código '{rule.rule_code}' ya existe")

    db_rule = AlertRule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.get("/alerts", response_model=AlertRuleList)
def list_alert_rules(
    is_active: Optional[bool] = None,
    alert_type: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all alert rules with optional filters.
    """
    query = db.query(AlertRule)

    if is_active is not None:
        query = query.filter(AlertRule.is_active == is_active)
    if alert_type:
        query = query.filter(AlertRule.alert_type == alert_type)
    if priority:
        query = query.filter(AlertRule.priority == priority)

    total = query.count()
    rules = query.offset(skip).limit(limit).all()

    return AlertRuleList(total=total, rules=rules)


@router.get("/alerts/{rule_id}", response_model=AlertRuleResponse)
def get_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Get a specific alert rule by ID.
    """
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla de alerta no encontrada")
    return rule


@router.put("/alerts/{rule_id}", response_model=AlertRuleResponse)
def update_alert_rule(rule_id: int, rule_update: AlertRuleUpdate, db: Session = Depends(get_db)):
    """
    Update an existing alert rule.
    """
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla de alerta no encontrada")

    update_data = rule_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/alerts/{rule_id}")
def delete_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    """
    Delete an alert rule.
    """
    rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla de alerta no encontrada")

    db.delete(rule)
    db.commit()
    return {"message": f"Regla de alerta '{rule.rule_code}' eliminada exitosamente"}


# =========================================================
# RIAS Guidelines Endpoints
# =========================================================

@router.post("/rias", response_model=RiasGuidelineResponse)
def create_rias_guideline(guideline: RiasGuidelineCreate, db: Session = Depends(get_db)):
    """
    Create a new RIAS guideline.
    """
    # Check if guideline_code already exists
    existing = db.query(RiasGuideline).filter(RiasGuideline.guideline_code == guideline.guideline_code).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Guía con código '{guideline.guideline_code}' ya existe")

    db_guideline = RiasGuideline(**guideline.model_dump())
    db.add(db_guideline)
    db.commit()
    db.refresh(db_guideline)
    return db_guideline


@router.get("/rias", response_model=RiasGuidelineList)
def list_rias_guidelines(
    is_active: Optional[bool] = None,
    life_stage: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all RIAS guidelines with optional filters.
    """
    query = db.query(RiasGuideline)

    if is_active is not None:
        query = query.filter(RiasGuideline.is_active == is_active)
    if life_stage:
        query = query.filter(RiasGuideline.life_stage == life_stage)

    total = query.count()
    guidelines = query.offset(skip).limit(limit).all()

    return RiasGuidelineList(total=total, guidelines=guidelines)


@router.get("/rias/{guideline_id}", response_model=RiasGuidelineResponse)
def get_rias_guideline(guideline_id: int, db: Session = Depends(get_db)):
    """
    Get a specific RIAS guideline by ID.
    """
    guideline = db.query(RiasGuideline).filter(RiasGuideline.id == guideline_id).first()
    if not guideline:
        raise HTTPException(status_code=404, detail="Guía RIAS no encontrada")
    return guideline


@router.put("/rias/{guideline_id}", response_model=RiasGuidelineResponse)
def update_rias_guideline(guideline_id: int, guideline_update: RiasGuidelineUpdate, db: Session = Depends(get_db)):
    """
    Update an existing RIAS guideline.
    """
    guideline = db.query(RiasGuideline).filter(RiasGuideline.id == guideline_id).first()
    if not guideline:
        raise HTTPException(status_code=404, detail="Guía RIAS no encontrada")

    update_data = guideline_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guideline, field, value)

    db.commit()
    db.refresh(guideline)
    return guideline


@router.delete("/rias/{guideline_id}")
def delete_rias_guideline(guideline_id: int, db: Session = Depends(get_db)):
    """
    Delete a RIAS guideline.
    """
    guideline = db.query(RiasGuideline).filter(RiasGuideline.id == guideline_id).first()
    if not guideline:
        raise HTTPException(status_code=404, detail="Guía RIAS no encontrada")

    db.delete(guideline)
    db.commit()
    return {"message": f"Guía RIAS '{guideline.guideline_code}' eliminada exitosamente"}
