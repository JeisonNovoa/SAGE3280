from typing import List, Dict, Optional
from app.models.patient import AgeGroupEnum
from app.models.control import ControlTypeEnum
from datetime import date, timedelta


class PatientClassifier:
    """
    Service to classify patients and determine required controls.
    Based on Resolución 3280 guidelines.
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
        has_cardiovascular_risk: bool,
        last_control_date: Optional[date]
    ) -> List[Dict]:
        """
        Determine what controls a patient needs based on their characteristics.
        Returns list of control dictionaries.

        Based on Resolución 3280 de 2018 - Rutas Integrales de Atención en Salud (RIAS)
        for Health Promotion and Maintenance, organized by life course stages.
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
        # AGE-BASED CONTROLS (RIAS - Promoción y Mantenimiento)
        # =================================================================

        # PRIMERA INFANCIA (0-5 años) - Control más frecuente
        if age_group == AgeGroupEnum.PRIMERA_INFANCIA.value:
            # Children under 2: monthly or every 2 months depending on age
            # Children 2-5: every 6 months
            if age < 2:
                frequency_days = 60  # Every 2 months for infants
            else:
                frequency_days = 180  # Every 6 months for 2-5 years

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_CRECIMIENTO_DESARROLLO.value,
                'control_name': 'Control de Crecimiento y Desarrollo',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración integral de crecimiento, desarrollo psicomotor, vacunación'
            })

        # INFANCIA (6-11 años) - Control anual
        elif age_group == AgeGroupEnum.INFANCIA.value:
            frequency_days = 365  # Annual
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_CRECIMIENTO_DESARROLLO.value,
                'control_name': 'Control de Crecimiento y Desarrollo',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración de salud escolar, estado nutricional, desarrollo'
            })

        # ADOLESCENCIA (12-17 años) - Control anual
        elif age_group == AgeGroupEnum.ADOLESCENCIA.value:
            frequency_days = 365  # Annual
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_JUVENTUD.value,
                'control_name': 'Control de Adolescencia',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración de salud sexual, reproductiva, salud mental, factores de riesgo'
            })

        # JUVENTUD (18-28 años) - Control cada 2 años
        elif age_group == AgeGroupEnum.JUVENTUD.value:
            frequency_days = 730  # Every 2 years
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_JUVENTUD.value,
                'control_name': 'Control de Juventud',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración de salud general, factores de riesgo, salud sexual'
            })

        # ADULTEZ (29-59 años) - Control cada 2 años o anual si factores de riesgo
        elif age_group == AgeGroupEnum.ADULTEZ.value:
            # Annual if risk factors, otherwise every 2 years
            if is_hypertensive or is_diabetic or has_cardiovascular_risk:
                frequency_days = 365  # Annual with risk factors
            else:
                frequency_days = 730  # Every 2 years without risk

            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_ADULTO.value,
                'control_name': 'Control de Adulto',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración de salud general, tamizaje de enfermedades crónicas'
            })

        # VEJEZ (60+ años) - Control anual obligatorio
        elif age_group == AgeGroupEnum.VEJEZ.value:
            frequency_days = 365  # Annual mandatory
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_VEJEZ.value,
                'control_name': 'Control de Vejez',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración geriátrica integral, funcionalidad, polifarmacia'
            })

        # =================================================================
        # CONDITION-SPECIFIC CONTROLS (Resolución 412/3280)
        # =================================================================

        # PREGNANCY CONTROL - Very frequent (monthly initially, then more frequent)
        if is_pregnant and sex == 'F':
            # Prenatal controls should be monthly minimum
            frequency_days = 30  # Monthly
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_PRENATAL.value,
                'control_name': 'Control Prenatal',
                'is_urgent': True,  # Always urgent for pregnant women
                'recommended_frequency_days': frequency_days,
                'description': 'Mínimo 4 controles: trimestral. Ideal: mensual en primer trimestre, quincenal después'
            })

        # HYPERTENSION CONTROL - Monthly per Resolución 412
        if is_hypertensive:
            frequency_days = 30  # Monthly control for hypertensives
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_HIPERTENSO.value,
                'control_name': 'Control de Hipertensión Arterial',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control mensual con toma de presión, adherencia a tratamiento, función renal'
            })

        # DIABETES CONTROL - Monthly per Resolución 412
        if is_diabetic:
            frequency_days = 30  # Monthly control for diabetics
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_DIABETICO.value,
                'control_name': 'Control de Diabetes Mellitus',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Control mensual con glicemia, HbA1c trimestral, pie diabético, fondo de ojo anual'
            })

        # CARDIOVASCULAR RISK EVALUATION - Annual for adults 40+
        if has_cardiovascular_risk or (age and age >= 40):
            frequency_days = 365  # Annual cardiovascular risk assessment
            is_overdue = days_since_control > frequency_days if last_control_date else True

            controls.append({
                'control_type': ControlTypeEnum.CONTROL_RIESGO_CV.value,
                'control_name': 'Evaluación de Riesgo Cardiovascular',
                'is_urgent': is_overdue,
                'recommended_frequency_days': frequency_days,
                'description': 'Valoración anual con perfil lipídico, presión arterial, glicemia, IMC, tabaquismo'
            })

        return controls

    @staticmethod
    def calculate_cardiovascular_risk(
        age: Optional[int],
        sex: Optional[str],
        is_hypertensive: bool,
        is_diabetic: bool,
        is_smoker: bool = False  # This could come from diagnoses or additional field
    ) -> tuple[bool, Optional[str]]:
        """
        Calculate cardiovascular risk level (simplified).
        Returns: (has_risk, risk_level)

        NOTE: This is a simplified version. Real cardiovascular risk calculation
        requires more parameters (cholesterol, HDL, systolic BP, etc.)
        """
        if not age:
            return False, None

        risk_factors = 0

        # Age
        if (sex == 'M' and age >= 45) or (sex == 'F' and age >= 55):
            risk_factors += 1

        # Conditions
        if is_hypertensive:
            risk_factors += 2
        if is_diabetic:
            risk_factors += 2
        if is_smoker:
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
        has_cardiovascular_risk: bool,
        cardiovascular_risk_level: Optional[str],
        last_control_date: Optional[date]
    ) -> int:
        """
        Calculate priority score (0-100) for patient contact.
        Higher score = higher priority.
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

        # Pregnancy
        if is_pregnant:
            score += 25

        # Chronic conditions
        if is_diabetic:
            score += 15
        if is_hypertensive:
            score += 15

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
