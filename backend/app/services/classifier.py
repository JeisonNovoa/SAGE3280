from typing import List, Dict, Optional
from app.models.patient import AgeGroupEnum
from app.models.control import ControlTypeEnum
from datetime import date, timedelta


class PatientClassifier:
    """
    Service to classify patients and determine required controls.
    Based on Resolución 3280 guidelines with complete RIAS implementation.
    """

    @staticmethod
    def classify_age_group(age: Optional[int]) -> Optional[str]:
        """
        Classify patient by age group according to Colombian health guidelines.
        """
        if age is None:
            return None

        if 0 <= age <= 5:
            return AgeGroupEnum.PRIMERA_INFANCIA.value
        elif 6 <= age <= 11:
            return AgeGroupEnum.INFANCIA.value
        elif 12 <= age <= 17:
            return AgeGroupEnum.ADOLESCENCIA.value
        elif 18 <= age <= 28:
            return AgeGroupEnum.JUVENTUD.value
        elif 29 <= age <= 59:
            return AgeGroupEnum.ADULTEZ.value
        elif age >= 60:
            return AgeGroupEnum.VEJEZ.value
        else:
            return None

    @staticmethod
    def determine_required_controls(
        age: Optional[int],
        sex: Optional[str],
        is_pregnant: bool,
        is_hypertensive: bool,
        is_diabetic: bool,
        has_hypothyroidism: bool,
        has_copd: bool,
        has_asthma: bool,
        has_ckd: bool,
        has_cardiovascular_disease: bool,
        has_cardiovascular_risk: bool,
        last_control_date: Optional[date]
    ) -> List[Dict]:
        """
        Determine what controls a patient needs based on their characteristics.
        Returns list of control dictionaries.

        Based on Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud (RIAS)
        for Health Promotion and Maintenance, organized by life course stages.

        Complete implementation for:
        - Grupo A: Preventive care (RIAS) by age group
        - Grupo B: Chronic conditions follow-up
        """
        controls = []
        age_group = PatientClassifier.classify_age_group(age)

        if not age or not age_group:
            return controls

        # Calculate days since last control for urgency determination
        days_since_control = 0
        if last_control_date:
            days_since_control = (date.today() - last_control_date).days

        # =================================================================
        # GRUPO A - CONTROLES PREVENTIVOS (RIAS)
        # =================================================================

        # PRIMERA INFANCIA (0-5 años)
        if age_group == AgeGroupEnum.PRIMERA_INFANCIA.value:
            if age < 2:
                frequency_days = 60  # Every 2 months for infants
            else:
                frequency_days = 180  # Every 6 months for 2-5 years

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_PRIMERA_INFANCIA.value,
                'control_name': 'Control de Primera Infancia',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración integral: crecimiento físico, desarrollo psicomotor, nutrición, vínculo afectivo'
            })

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_CRECIMIENTO_DESARROLLO.value,
                'control_name': 'Valoración de Crecimiento y Desarrollo',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Medición de peso, talla, perímetro cefálico. Evaluación de hitos del desarrollo'
            })

            controls.append({
                'control_type': ControlTypeEnum.VACUNACION.value,
                'control_name': 'Esquema de Vacunación',
                'is_urgent': is_overdue,
                'recommended_frequency_days': 30 if age < 1 else 180,
                'description': 'Esquema PAI: BCG, Hepatitis B, Pentavalente, Neumococo, Rotavirus, Influenza, Triple Viral, Varicela'
            })

            controls.append({
                'control_type': ControlTypeEnum.VALORACION_NUTRICIONAL.value,
                'control_name': 'Valoración Nutricional',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Evaluación del estado nutricional, detección de desnutrición o sobrepeso, lactancia materna'
            })

        # INFANCIA (6-11 años)
        elif age_group == AgeGroupEnum.INFANCIA.value:
            frequency_days = 365  # Annual

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_INFANCIA.value,
                'control_name': 'Control de Infancia',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración integral de salud escolar, crecimiento, desarrollo, nutrición'
            })

            controls.append({
                'control_type': ControlTypeEnum.SALUD_ORAL.value,
                'control_name': 'Control de Salud Oral',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración odontológica preventiva, higiene oral, detección de caries'
            })

            controls.append({
                'control_type': ControlTypeEnum.VALORACION_NUTRICIONAL.value,
                'control_name': 'Valoración Nutricional',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Evaluación de IMC, detección de malnutrición, hábitos alimentarios'
            })

            controls.append({
                'control_type': ControlTypeEnum.SALUD_MENTAL.value,
                'control_name': 'Tamizaje de Salud Mental',
                'is_urgent': False,
                'recommended_frequency_days': frequency_days,
                'description': 'Detección temprana de problemas de salud mental, adaptación escolar'
            })

        # ADOLESCENCIA (12-17 años)
        elif age_group == AgeGroupEnum.ADOLESCENCIA.value:
            frequency_days = 365  # Annual

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_ADOLESCENCIA.value,
                'control_name': 'Control de Adolescencia',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración integral del adolescente: desarrollo puberal, salud mental, conductas de riesgo'
            })

            controls.append({
                'control_type': ControlTypeEnum.SALUD_SEXUAL_REPRODUCTIVA.value,
                'control_name': 'Salud Sexual y Reproductiva',
                'is_urgent': False,
                'recommended_frequency_days': frequency_days,
                'description': 'Educación sexual, anticoncepción, prevención de ITS, detección de VIH'
            })

            controls.append({
                'control_type': ControlTypeEnum.DETECCION_ITS.value,
                'control_name': 'Detección de ITS',
                'is_urgent': False,
                'recommended_frequency_days': 365,
                'description': 'Tamizaje de infecciones de transmisión sexual en población sexualmente activa'
            })

            controls.append({
                'control_type': ControlTypeEnum.SALUD_MENTAL.value,
                'control_name': 'Salud Mental Adolescente',
                'is_urgent': False,
                'recommended_frequency_days': frequency_days,
                'description': 'Detección de depresión, ansiedad, trastornos alimentarios, consumo de sustancias'
            })

        # JUVENTUD (18-28 años)
        elif age_group == AgeGroupEnum.JUVENTUD.value:
            frequency_days = 730  # Every 2 years

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_JUVENTUD.value,
                'control_name': 'Control de Juventud',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración de salud general, factores de riesgo, estilos de vida saludables'
            })

            if sex == 'F':
                controls.append({
                    'control_type': ControlTypeEnum.PLANIFICACION_FAMILIAR.value,
                    'control_name': 'Planificación Familiar',
                    'is_urgent': False,
                    'recommended_frequency_days': 365,
                    'description': 'Asesoría en métodos anticonceptivos, preconcepcional'
                })

        # ADULTEZ (29-59 años)
        elif age_group == AgeGroupEnum.ADULTEZ.value:
            # Annual if risk factors, otherwise every 2 years
            if is_hypertensive or is_diabetic or has_cardiovascular_risk:
                frequency_days = 365  # Annual with risk factors
            else:
                frequency_days = 730  # Every 2 years without risk

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_ADULTEZ.value,
                'control_name': 'Control de Adultez',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración integral: tamizaje de enfermedades crónicas (HTA, DM), riesgo CV, cáncer'
            })

        # VEJEZ (60+ años)
        elif age_group == AgeGroupEnum.VEJEZ.value:
            frequency_days = 365  # Annual mandatory

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_VEJEZ.value,
                'control_name': 'Control de Vejez',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control anual obligatorio para adulto mayor'
            })

            controls.append({
                'control_type': ControlTypeEnum.VALORACION_GERIATRICA.value,
                'control_name': 'Valoración Geriátrica Integral',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Evaluación multidimensional: funcional, cognitiva, afectiva, social, nutricional'
            })

            controls.append({
                'control_type': ControlTypeEnum.EVALUACION_FUNCIONALIDAD.value,
                'control_name': 'Evaluación de Funcionalidad',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Escala de Barthel, Lawton-Brody. Evaluación de riesgo de caídas'
            })

            controls.append({
                'control_type': ControlTypeEnum.SALUD_MENTAL.value,
                'control_name': 'Evaluación Cognitiva',
                'is_urgent': False,
                'recommended_frequency_days': frequency_days,
                'description': 'Detección de deterioro cognitivo, demencia, depresión en adulto mayor'
            })

        # =================================================================
        # GRUPO B - CONDICIONES CRÓNICAS (Seguimiento Activo)
        # =================================================================

        # CONTROL PRENATAL
        if is_pregnant and sex == 'F':
            frequency_days = 30  # Monthly minimum

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_PRENATAL.value,
                'control_name': 'Control Prenatal',
                'is_urgent': True,  # Always urgent for pregnant women
                'recommended_frequency_days': frequency_days,
                'description': 'Mínimo 4 controles prenatales. Mensual hasta semana 32, quincenal hasta 36, semanal después'
            })

        # HIPERTENSIÓN ARTERIAL
        if is_hypertensive:
            frequency_days = 30  # Monthly control per Resolución 412

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_HIPERTENSO.value,
                'control_name': 'Control de Hipertensión Arterial',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control mensual: toma de PA, adherencia tratamiento, función renal, perfil lipídico semestral'
            })

        # DIABETES MELLITUS
        if is_diabetic:
            frequency_days = 30  # Monthly control per Resolución 412

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_DIABETICO.value,
                'control_name': 'Control de Diabetes Mellitus',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control mensual: glicemia, HbA1c trimestral, pie diabético trimestral, fondo de ojo anual'
            })

        # HIPOTIROIDISMO
        if has_hypothyroidism:
            frequency_days = 90  # Every 3 months

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_HIPOTIROIDISMO.value,
                'control_name': 'Control de Hipotiroidismo',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control trimestral: TSH, T4 libre, adherencia a levotiroxina, síntomas clínicos'
            })

        # EPOC (Enfermedad Pulmonar Obstructiva Crónica)
        if has_copd:
            frequency_days = 90  # Every 3 months

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_EPOC.value,
                'control_name': 'Control de EPOC',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control trimestral: espirometría, saturación O2, exacerbaciones, adherencia a inhaladores'
            })

        # ASMA
        if has_asthma:
            frequency_days = 90  # Every 3 months

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_ASMA.value,
                'control_name': 'Control de Asma',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control trimestral: control de síntomas (ACT), espirometría, técnica inhalatoria, plan de acción'
            })

        # IRC (Insuficiencia Renal Crónica)
        if has_ckd:
            frequency_days = 90  # Every 3 months (puede ser mensual según estadio)

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_IRC.value,
                'control_name': 'Control de Insuficiencia Renal Crónica',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control según estadio: creatinina, TFG, BUN, K+, Ca, P, anemia, PA'
            })

        # ENFERMEDAD CARDIOVASCULAR ESTABLECIDA
        if has_cardiovascular_disease:
            frequency_days = 90  # Every 3 months

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_CARDIOVASCULAR.value,
                'control_name': 'Control de Enfermedad Cardiovascular',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Seguimiento post-IAM, ICC, ECV: síntomas, adherencia antiagregación, perfil lipídico, ecocardiograma'
            })

        # RIESGO CARDIOVASCULAR (sin enfermedad establecida)
        if has_cardiovascular_risk and age and age >= 40 and not has_cardiovascular_disease:
            frequency_days = 365  # Annual cardiovascular risk assessment

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_RIESGO_CV.value,
                'control_name': 'Evaluación de Riesgo Cardiovascular',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración anual: Framingham/ASCVD, perfil lipídico, PA, glicemia, IMC, tabaquismo'
            })

        # CONTROL DE MEDICAMENTOS (para pacientes con polifarmacia)
        # Aplica si tiene 2 o más condiciones crónicas
        chronic_conditions_count = sum([
            is_hypertensive, is_diabetic, has_hypothyroidism,
            has_copd, has_asthma, has_ckd, has_cardiovascular_disease
        ])

        if chronic_conditions_count >= 2:
            controls.append({
                'control_type': ControlTypeEnum.CONTROL_MEDICAMENTOS.value,
                'control_name': 'Revisión de Medicamentos',
                'is_urgent': False,
                'recommended_frequency_days': 180,  # Every 6 months
                'description': 'Revisión de adherencia, interacciones medicamentosas, RAM, ajuste de dosis'
            })

        return controls

    @staticmethod
    def calculate_cardiovascular_risk(
        age: Optional[int],
        sex: Optional[str],
        is_hypertensive: bool,
        is_diabetic: bool,
        is_smoker: bool = False,
        systolic_bp: Optional[int] = None,
        cholesterol_total: Optional[float] = None,
        hdl: Optional[float] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Calculate cardiovascular risk level.

        Uses simplified risk scoring if lab values not available.
        Could be enhanced with Framingham/ASCVD calculation when labs available.

        Returns: (has_risk, risk_level)
        """
        if not age:
            return False, None

        risk_factors = 0

        # Age
        if (sex == 'M' and age >= 45) or (sex == 'F' and age >= 55):
            risk_factors += 1

        # Major risk factors
        if is_hypertensive:
            risk_factors += 2
        if is_diabetic:
            risk_factors += 2
        if is_smoker:
            risk_factors += 1

        # Additional factors from lab values (if available)
        if systolic_bp and systolic_bp >= 140:
            risk_factors += 1

        if cholesterol_total and cholesterol_total >= 240:
            risk_factors += 1

        if hdl and hdl < 40:  # Low HDL is a risk factor
            risk_factors += 1

        # Determine risk level
        if risk_factors == 0:
            return False, None
        elif risk_factors <= 1:
            return True, "bajo"
        elif risk_factors <= 3:
            return True, "medio"
        elif risk_factors <= 5:
            return True, "alto"
        else:
            return True, "muy_alto"

    @staticmethod
    def calculate_priority_score(
        age: Optional[int],
        is_pregnant: bool,
        is_hypertensive: bool,
        is_diabetic: bool,
        has_hypothyroidism: bool,
        has_copd: bool,
        has_asthma: bool,
        has_ckd: bool,
        has_cardiovascular_disease: bool,
        has_cardiovascular_risk: bool,
        cardiovascular_risk_level: Optional[str],
        last_control_date: Optional[date]
    ) -> int:
        """
        Calculate priority score (0-100) for patient contact.
        Higher score = higher priority.

        Takes into account all chronic conditions.
        """
        score = 50  # Base score

        # Age factors
        if age:
            if age < 1:
                score += 20  # Infants
            elif age >= 65:
                score += 15  # Elderly
            elif 1 <= age <= 5:
                score += 10  # Young children

        # Pregnancy - highest priority
        if is_pregnant:
            score += 25

        # Chronic conditions - weight by severity
        if is_diabetic:
            score += 15
        if is_hypertensive:
            score += 15
        if has_ckd:
            score += 20  # Renal disease is very serious
        if has_cardiovascular_disease:
            score += 18  # Established CVD
        if has_copd:
            score += 12
        if has_asthma:
            score += 8
        if has_hypothyroidism:
            score += 5

        # Cardiovascular risk
        if has_cardiovascular_risk:
            if cardiovascular_risk_level == "muy_alto":
                score += 20
            elif cardiovascular_risk_level == "alto":
                score += 15
            elif cardiovascular_risk_level == "medio":
                score += 10
            else:
                score += 5

        # Time since last control
        if last_control_date:
            days_since = (date.today() - last_control_date).days
            if days_since > 730:  # 2 years
                score += 15
            elif days_since > 365:  # 1 year
                score += 10
            elif days_since > 180:  # 6 months
                score += 5
        else:
            # Never had a control
            score += 20

        # Cap at 100
        return min(score, 100)
