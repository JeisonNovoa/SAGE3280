from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class AlertTypeEnum(str, enum.Enum):
    # Exámenes de laboratorio - General
    PERFIL_LIPIDICO = "perfil_lipidico"
    GLICEMIA = "glicemia"
    HBA1C = "hba1c"
    CREATININA = "creatinina"
    POTASIO = "potasio"
    MICROALBUMINURIA = "microalbuminuria"
    HEMOGRAMA = "hemograma"
    PARCIAL_ORINA = "parcial_orina"

    # Exámenes de laboratorio - Condiciones específicas
    TSH = "tsh"  # Hormona estimulante de tiroides (hipotiroidismo)
    T4_LIBRE = "t4_libre"  # Tiroxina libre
    ESPIROMETRIA = "espirometria"  # EPOC, Asma
    GASES_ARTERIALES = "gases_arteriales"  # EPOC
    CLEARANCE_CREATININA = "clearance_creatinina"  # IRC
    BUN = "bun"  # Nitrógeno ureico en sangre - IRC

    # Exámenes de imágenes
    MAMOGRAFIA = "mamografia"
    ECOGRAFIA = "ecografia"
    ECOGRAFIA_OBSTETRICA = "ecografia_obstetrica"
    RAYOS_X = "rayos_x"
    RAYOS_X_TORAX = "rayos_x_torax"  # EPOC
    EKG = "ekg"
    ECOCARDIOGRAMA = "ecocardiograma"  # Enfermedad cardiovascular

    # Tamizajes preventivos
    PSA = "psa"
    CITOLOGIA = "citologia"
    VPH = "vph"
    COLONOSCOPIA = "colonoscopia"
    SANGRE_OCULTA_HECES = "sangre_oculta_heces"  # Tamizaje cáncer colorrectal

    # Evaluaciones específicas
    FONDO_OJO = "fondo_ojo"
    VALORACION_PIE_DIABETICO = "valoracion_pie_diabetico"
    EVALUACION_RIESGO_CV = "evaluacion_riesgo_cardiovascular"
    AGUDEZA_VISUAL = "agudeza_visual"
    AGUDEZA_AUDITIVA = "agudeza_auditiva"
    VALORACION_ODONTOLOGICA = "valoracion_odontologica"

    # Vacunación
    VACUNA_INFLUENZA = "vacuna_influenza"
    VACUNA_NEUMOCOCO = "vacuna_neumococo"
    VACUNA_COVID = "vacuna_covid"
    VACUNA_VPH = "vacuna_vph"
    VACUNA_HEPATITIS_B = "vacuna_hepatitis_b"
    VACUNA_TETANOS = "vacuna_tetanos"
    ESQUEMA_VACUNACION_COMPLETO = "esquema_vacunacion_completo"

    # Mediciones y controles rutinarios
    TOMA_PRESION = "toma_presion"
    MEDICION_IMC = "medicion_imc"
    MEDICION_PESO_TALLA = "medicion_peso_talla"

    # Evaluaciones desarrollo infantil
    TAMIZAJE_DESARROLLO = "tamizaje_desarrollo"
    VALORACION_CRECIMIENTO = "valoracion_crecimiento"

    # Otros
    REFILL_MEDICAMENTO = "refill_medicamento"  # Alerta de renovación de medicamento


class AlertPriorityEnum(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class AlertStatusEnum(str, enum.Enum):
    ACTIVA = "activa"
    NOTIFICADA = "notificada"
    PROGRAMADA = "programada"
    COMPLETADA = "completada"
    IGNORADA = "ignorada"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    # Patient reference
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    # Alert info
    alert_type = Column(Enum(AlertTypeEnum), nullable=False, index=True)
    alert_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(AlertPriorityEnum), default=AlertPriorityEnum.MEDIA, index=True)
    status = Column(Enum(AlertStatusEnum), default=AlertStatusEnum.ACTIVA, index=True)

    # Reasoning
    reason = Column(Text, nullable=True)  # Por qué se generó esta alerta
    criteria = Column(Text, nullable=True)  # Criterios que cumplió (edad, sexo, riesgo, etc.)

    # Dates
    created_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)  # Fecha límite recomendada
    notified_date = Column(DateTime, nullable=True)
    completed_date = Column(Date, nullable=True)

    # Action taken
    action_taken = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.alert_type} for Patient {self.patient_id} - {self.priority}>"
