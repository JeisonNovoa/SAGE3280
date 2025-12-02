from typing import List, Dict, Optional
from app.models.alert import AlertTypeEnum, AlertPriorityEnum
from datetime import date, timedelta


class AlertGenerator:
    """
    Service to generate preventive alerts for patients.
    Determines what exams and procedures are needed based on patient characteristics.

    Based on Resolución 3280 de 2018 and Colombian clinical practice guidelines for screening.

    Screening Frequencies (Colombian Guidelines):
    - Cytology (Cervical Cancer): Annual for women 25-65 years
    - Mammography (Breast Cancer): Every 2 years for women 50-69 years
    - PSA (Prostate Cancer): Annual for men 50+ years
    - Colonoscopy (Colon Cancer): Every 10 years for adults 50+ (or shorter with risk)
    - Lipid Profile (CV Risk): Every 1-3 years depending on risk
    - Glycemia (Diabetes): Annual for adults 18+ or every 3 years without risk
    - Blood Pressure: Annual for all adults 18+
    - HbA1c (Diabetes Control): Every 3 months for diabetics
    - Diabetic Retinopathy Screening: Annual
    - Diabetic Foot Evaluation: Every 3 months for diabetics
    - Renal Function (Creatinine/Microalbuminuria): Every 6 months for diabetics/hypertensives
    """

    @staticmethod
    def generate_alerts(
        age: Optional[int],
        sex: Optional[str],
        is_pregnant: bool,
        is_hypertensive: bool,
        is_diabetic: bool,
        has_cardiovascular_risk: bool,
        cardiovascular_risk_level: Optional[str],
        last_exam_dates: Optional[Dict[str, date]] = None
    ) -> List[Dict]:
        """
        Generate alerts for required exams and procedures with calculated due dates.

        Args:
            last_exam_dates: Dict mapping exam type to last exam date (e.g., {'citologia': date(2023, 1, 15)})

        Returns list of alert dictionaries including due_date field.
        """
        alerts = []

        if not age:
            return alerts

        # Initialize last_exam_dates if not provided
        if last_exam_dates is None:
            last_exam_dates = {}

        # Helper function to calculate due date
        def calculate_due_date(exam_type: str, interval_days: int, is_urgent: bool = False) -> date:
            """Calculate due date based on last exam or today if no previous exam"""
            last_date = last_exam_dates.get(exam_type)

            if last_date:
                # Calculate from last exam date
                due = last_date + timedelta(days=interval_days)
            else:
                # No previous exam - set due date based on urgency
                if is_urgent:
                    due = date.today() + timedelta(days=30)  # 1 month for urgent
                else:
                    due = date.today() + timedelta(days=90)  # 3 months for non-urgent

            return due

        # ============================================
        # GENERAL POPULATION ALERTS
        # ============================================

        # Blood pressure for all adults - Annual
        if age >= 18:
            alerts.append({
                'alert_type': AlertTypeEnum.TOMA_PRESION.value,
                'alert_name': 'Toma de Presión Arterial',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control anual de presión arterial para adultos',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('toma_presion', 365)
            })

        # BMI measurement for adults - Annual
        if age >= 18:
            alerts.append({
                'alert_type': AlertTypeEnum.MEDICION_IMC.value,
                'alert_name': 'Medición de IMC',
                'priority': AlertPriorityEnum.BAJA.value,
                'reason': 'Control de peso y estado nutricional',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('medicion_imc', 365)
            })

        # Glycemia for adults - Annual if no risk, every 3 years if low risk
        if age >= 18:
            interval = 365 if (is_diabetic or is_hypertensive or has_cardiovascular_risk) else 1095  # 3 years
            alerts.append({
                'alert_type': AlertTypeEnum.GLICEMIA.value,
                'alert_name': 'Glicemia en Ayunas',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Tamizaje de diabetes',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('glicemia', interval)
            })

        # ============================================
        # GENDER-SPECIFIC ALERTS
        # ============================================

        # Women's health
        if sex == 'F':
            # Cytology (25-65 years) - Annual per Colombian guidelines
            if 25 <= age <= 65:
                alerts.append({
                    'alert_type': AlertTypeEnum.CITOLOGIA.value,
                    'alert_name': 'Citología Cervicouterina',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Tamizaje de cáncer cervicouterino - anual',
                    'criteria': f'Mujer, {age} años (rango 25-65)',
                    'due_date': calculate_due_date('citologia', 365, is_urgent=True)
                })

            # Mammography (50-69 years) - Every 2 years per Colombian guidelines
            if 50 <= age <= 69:
                alerts.append({
                    'alert_type': AlertTypeEnum.MAMOGRAFIA.value,
                    'alert_name': 'Mamografía',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Tamizaje de cáncer de mama - cada 2 años',
                    'criteria': f'Mujer, {age} años (rango 50-69)',
                    'due_date': calculate_due_date('mamografia', 730, is_urgent=True)  # 2 years
                })

        # Men's health
        if sex == 'M':
            # PSA (50+ years) - Annual
            if age >= 50:
                alerts.append({
                    'alert_type': AlertTypeEnum.PSA.value,
                    'alert_name': 'Antígeno Prostático Específico (PSA)',
                    'priority': AlertPriorityEnum.MEDIA.value,
                    'reason': 'Tamizaje de cáncer de próstata - anual',
                    'criteria': f'Hombre, {age} años (≥50)',
                    'due_date': calculate_due_date('psa', 365)
                })

        # ============================================
        # CARDIOVASCULAR RISK ALERTS
        # ============================================

        if has_cardiovascular_risk or age >= 40:
            # Lipid profile - Frequency depends on risk level
            if cardiovascular_risk_level in ['alto', 'muy_alto']:
                interval = 365  # Annual for high risk
            elif has_cardiovascular_risk:
                interval = 730  # Every 2 years for medium risk
            else:
                interval = 1095  # Every 3 years for low risk (age-based screening)

            alerts.append({
                'alert_type': AlertTypeEnum.PERFIL_LIPIDICO.value,
                'alert_name': 'Perfil Lipídico',
                'priority': AlertPriorityEnum.ALTA.value if has_cardiovascular_risk else AlertPriorityEnum.MEDIA.value,
                'reason': f'Evaluación de riesgo cardiovascular - cada {interval//365} año(s)',
                'criteria': f'Edad: {age} años, Riesgo CV: {cardiovascular_risk_level or "a evaluar"}',
                'due_date': calculate_due_date('perfil_lipidico', interval, is_urgent=has_cardiovascular_risk)
            })

        # EKG for high-risk or older adults - Annual
        if (has_cardiovascular_risk and cardiovascular_risk_level in ['alto', 'muy_alto']) or age >= 50:
            alerts.append({
                'alert_type': AlertTypeEnum.EKG.value,
                'alert_name': 'Electrocardiograma',
                'priority': AlertPriorityEnum.ALTA.value if has_cardiovascular_risk else AlertPriorityEnum.MEDIA.value,
                'reason': 'Evaluación de función cardíaca - anual',
                'criteria': f'Edad: {age} años, Riesgo CV: {has_cardiovascular_risk}',
                'due_date': calculate_due_date('ekg', 365, is_urgent=has_cardiovascular_risk)
            })

        # ============================================
        # HYPERTENSION ALERTS
        # ============================================

        if is_hypertensive:
            # Creatinine - Every 6 months per Resolución 412
            alerts.append({
                'alert_type': AlertTypeEnum.CREATININA.value,
                'alert_name': 'Creatinina Sérica',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Evaluación de función renal en hipertenso - cada 6 meses',
                'criteria': 'Paciente hipertenso',
                'due_date': calculate_due_date('creatinina', 180, is_urgent=True)  # 6 months
            })

            # Potassium - Every 6 months
            alerts.append({
                'alert_type': AlertTypeEnum.POTASIO.value,
                'alert_name': 'Potasio Sérico',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control de electrolitos en hipertenso - cada 6 meses',
                'criteria': 'Paciente hipertenso',
                'due_date': calculate_due_date('potasio', 180, is_urgent=True)  # 6 months
            })

            # Microalbuminuria - Every 6 months
            alerts.append({
                'alert_type': AlertTypeEnum.MICROALBUMINURIA.value,
                'alert_name': 'Microalbuminuria',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Detección de daño renal en hipertenso - cada 6 meses',
                'criteria': 'Paciente hipertenso',
                'due_date': calculate_due_date('microalbuminuria', 180, is_urgent=True)  # 6 months
            })

        # ============================================
        # DIABETES ALERTS
        # ============================================

        if is_diabetic:
            # HbA1c - Every 3 months per Resolución 412
            alerts.append({
                'alert_type': AlertTypeEnum.HBA1C.value,
                'alert_name': 'Hemoglobina Glicosilada (HbA1c)',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Control de diabetes - cada 3 meses',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('hba1c', 90, is_urgent=True)  # 3 months
            })

            # Microalbuminuria - Every 6 months
            alerts.append({
                'alert_type': AlertTypeEnum.MICROALBUMINURIA.value,
                'alert_name': 'Microalbuminuria',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Detección de nefropatía diabética - cada 6 meses',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('microalbuminuria', 180, is_urgent=True)  # 6 months
            })

            # Eye exam (Diabetic retinopathy screening) - Annual
            alerts.append({
                'alert_type': AlertTypeEnum.FONDO_OJO.value,
                'alert_name': 'Fondo de Ojo',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Detección de retinopatía diabética - anual',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('fondo_ojo', 365, is_urgent=True)  # Annual
            })

            # Diabetic foot evaluation - Every 3 months
            alerts.append({
                'alert_type': AlertTypeEnum.VALORACION_PIE_DIABETICO.value,
                'alert_name': 'Valoración de Pie Diabético',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Prevención de complicaciones en pie diabético - cada 3 meses',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('valoracion_pie_diabetico', 90, is_urgent=True)  # 3 months
            })

            # Creatinine - Every 6 months (if not already added by hypertension)
            if not is_hypertensive:  # Avoid duplicate if already added
                alerts.append({
                    'alert_type': AlertTypeEnum.CREATININA.value,
                    'alert_name': 'Creatinina Sérica',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Evaluación de función renal en diabético - cada 6 meses',
                    'criteria': 'Paciente diabético',
                    'due_date': calculate_due_date('creatinina', 180, is_urgent=True)  # 6 months
                })

        # ============================================
        # PREGNANCY ALERTS
        # ============================================

        if is_pregnant and sex == 'F':
            # Obstetric ultrasound - Multiple during pregnancy (recommend next one in 4-6 weeks)
            alerts.append({
                'alert_type': AlertTypeEnum.ECOGRAFIA.value,
                'alert_name': 'Ecografía Obstétrica',
                'priority': AlertPriorityEnum.URGENTE.value,
                'reason': 'Control prenatal - mínimo 3 ecografías durante embarazo',
                'criteria': 'Paciente gestante',
                'due_date': calculate_due_date('ecografia', 42, is_urgent=True)  # 6 weeks
            })

        return alerts

    @staticmethod
    def prioritize_alerts(alerts: List[Dict]) -> List[Dict]:
        """
        Sort alerts by priority.
        """
        priority_order = {
            AlertPriorityEnum.URGENTE.value: 4,
            AlertPriorityEnum.ALTA.value: 3,
            AlertPriorityEnum.MEDIA.value: 2,
            AlertPriorityEnum.BAJA.value: 1,
        }

        return sorted(
            alerts,
            key=lambda x: priority_order.get(x['priority'], 0),
            reverse=True
        )
