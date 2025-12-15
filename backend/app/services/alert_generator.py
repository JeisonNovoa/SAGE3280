from typing import List, Dict, Optional
from app.models.alert import AlertTypeEnum, AlertPriorityEnum
from datetime import date, timedelta


class AlertGenerator:
    """
    Service to generate preventive alerts for patients.
    Determines what exams and procedures are needed based on patient characteristics.

    Complete implementation based on:
    - Resolución 3280 de 2018 (RIAS)
    - Resolución 412 de 2000 (Norma técnica para enfermedades crónicas)
    - Colombian clinical practice guidelines for screening

    Organized by:
    - Grupo A: Preventive screening by age/sex
    - Grupo B: Chronic condition follow-up
    """

    @staticmethod
    def generate_alerts(
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
        cardiovascular_risk_level: Optional[str],
        last_exam_dates: Optional[Dict[str, date]] = None
    ) -> List[Dict]:
        """
        Generate complete alerts for required exams and procedures.

        Args:
            last_exam_dates: Dict mapping exam type to last exam date

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
        # GRUPO A - ALERTAS PREVENTIVAS POR EDAD/SEXO
        # ============================================

        # ------ POBLACIÓN GENERAL (ADULTOS) ------

        if age >= 18:
            # Toma de presión arterial - Anual
            alerts.append({
                'alert_type': AlertTypeEnum.TOMA_PRESION.value,
                'alert_name': 'Toma de Presión Arterial',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control anual de presión arterial para adultos',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('toma_presion', 365)
            })

            # IMC - Anual
            alerts.append({
                'alert_type': AlertTypeEnum.MEDICION_IMC.value,
                'alert_name': 'Medición de IMC',
                'priority': AlertPriorityEnum.BAJA.value,
                'reason': 'Control de peso y estado nutricional',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('medicion_imc', 365)
            })

            # Glicemia - Anual (o cada 3 años si bajo riesgo)
            interval = 365 if (is_diabetic or is_hypertensive or has_cardiovascular_risk) else 1095
            alerts.append({
                'alert_type': AlertTypeEnum.GLICEMIA.value,
                'alert_name': 'Glicemia en Ayunas',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Tamizaje de diabetes',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('glicemia', interval)
            })

        # ------ NIÑOS Y ADOLESCENTES ------

        if age <= 17:
            # Peso y talla
            alerts.append({
                'alert_type': AlertTypeEnum.MEDICION_PESO_TALLA.value,
                'alert_name': 'Medición de Peso y Talla',
                'priority': AlertPriorityEnum.ALTA.value if age < 5 else AlertPriorityEnum.MEDIA.value,
                'reason': 'Control de crecimiento y desarrollo',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('medicion_peso_talla', 180 if age < 5 else 365)
            })

        if age < 5:
            # Tamizaje de desarrollo
            alerts.append({
                'alert_type': AlertTypeEnum.TAMIZAJE_DESARROLLO.value,
                'alert_name': 'Tamizaje de Desarrollo Psicomotor',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Evaluación de hitos del desarrollo',
                'criteria': f'Primera infancia: {age} años',
                'due_date': calculate_due_date('tamizaje_desarrollo', 60 if age < 2 else 180)
            })

            # Esquema de vacunación
            alerts.append({
                'alert_type': AlertTypeEnum.ESQUEMA_VACUNACION_COMPLETO.value,
                'alert_name': 'Esquema de Vacunación',
                'priority': AlertPriorityEnum.URGENTE.value if age < 1 else AlertPriorityEnum.ALTA.value,
                'reason': 'Completar esquema PAI según edad',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('esquema_vacunacion', 30 if age < 1 else 180)
            })

        if 6 <= age <= 17:
            # Salud oral
            alerts.append({
                'alert_type': AlertTypeEnum.VALORACION_ODONTOLOGICA.value,
                'alert_name': 'Valoración Odontológica',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control preventivo de salud oral',
                'criteria': f'Edad escolar: {age} años',
                'due_date': calculate_due_date('valoracion_odontologica', 365)
            })

        # ------ TAMIZAJES ESPECÍFICOS POR SEXO ------

        # Mujeres
        if sex == 'F':
            # Citología cervicouterina (25-65 años) - Anual
            if 25 <= age <= 65:
                alerts.append({
                    'alert_type': AlertTypeEnum.CITOLOGIA.value,
                    'alert_name': 'Citología Cervicouterina',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Tamizaje de cáncer cervicouterino - anual',
                    'criteria': f'Mujer, {age} años (rango 25-65)',
                    'due_date': calculate_due_date('citologia', 365, is_urgent=True)
                })

            # Test de VPH (30-65 años) - Alternativa o complemento a citología
            if 30 <= age <= 65:
                alerts.append({
                    'alert_type': AlertTypeEnum.VPH.value,
                    'alert_name': 'Test de VPH',
                    'priority': AlertPriorityEnum.MEDIA.value,
                    'reason': 'Detección de virus papiloma humano - cada 3-5 años',
                    'criteria': f'Mujer, {age} años (rango 30-65)',
                    'due_date': calculate_due_date('vph', 1095)  # 3 years
                })

            # Mamografía (50-69 años) - Cada 2 años
            if 50 <= age <= 69:
                alerts.append({
                    'alert_type': AlertTypeEnum.MAMOGRAFIA.value,
                    'alert_name': 'Mamografía',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Tamizaje de cáncer de mama - cada 2 años',
                    'criteria': f'Mujer, {age} años (rango 50-69)',
                    'due_date': calculate_due_date('mamografia', 730, is_urgent=True)  # 2 years
                })

        # Hombres
        if sex == 'M':
            # PSA (50+ años) - Anual
            if age >= 50:
                alerts.append({
                    'alert_type': AlertTypeEnum.PSA.value,
                    'alert_name': 'Antígeno Prostático Específico (PSA)',
                    'priority': AlertPriorityEnum.MEDIA.value,
                    'reason': 'Tamizaje de cáncer de próstata - anual',
                    'criteria': f'Hombre, {age} años (≥50)',
                    'due_date': calculate_due_date('psa', 365)
                })

        # ------ TAMIZAJE CÁNCER COLORRECTAL (AMBOS SEXOS) ------

        if age >= 50:
            # Sangre oculta en heces - Anual
            alerts.append({
                'alert_type': AlertTypeEnum.SANGRE_OCULTA_HECES.value,
                'alert_name': 'Sangre Oculta en Heces',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Tamizaje de cáncer colorrectal - anual',
                'criteria': f'Edad: {age} años (≥50)',
                'due_date': calculate_due_date('sangre_oculta_heces', 365)
            })

            # Colonoscopia - Cada 10 años (o según hallazgos)
            if age >= 50 and age % 10 == 0:  # Simplified trigger
                alerts.append({
                    'alert_type': AlertTypeEnum.COLONOSCOPIA.value,
                    'alert_name': 'Colonoscopia',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Tamizaje de cáncer colorrectal - cada 10 años',
                    'criteria': f'Edad: {age} años (≥50)',
                    'due_date': calculate_due_date('colonoscopia', 3650, is_urgent=True)  # 10 years
                })

        # ------ EVALUACIONES SENSORIALES ------

        if 6 <= age <= 11 or age >= 60:
            # Agudeza visual
            alerts.append({
                'alert_type': AlertTypeEnum.AGUDEZA_VISUAL.value,
                'alert_name': 'Evaluación de Agudeza Visual',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control preventivo de visión',
                'criteria': f'Edad: {age} años',
                'due_date': calculate_due_date('agudeza_visual', 730)  # Every 2 years
            })

        if age >= 60:
            # Agudeza auditiva
            alerts.append({
                'alert_type': AlertTypeEnum.AGUDEZA_AUDITIVA.value,
                'alert_name': 'Evaluación de Agudeza Auditiva',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Detección de hipoacusia en adulto mayor',
                'criteria': f'Edad: {age} años (≥60)',
                'due_date': calculate_due_date('agudeza_auditiva', 730)  # Every 2 years
            })

        # ------ VACUNACIÓN ADULTOS ------

        if age >= 60:
            # Influenza - Anual
            alerts.append({
                'alert_type': AlertTypeEnum.VACUNA_INFLUENZA.value,
                'alert_name': 'Vacuna Influenza',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Vacunación anual contra influenza - adulto mayor',
                'criteria': f'Edad: {age} años (≥60)',
                'due_date': calculate_due_date('vacuna_influenza', 365, is_urgent=True)
            })

            # Neumococo - Única dosis o refuerzo
            alerts.append({
                'alert_type': AlertTypeEnum.VACUNA_NEUMOCOCO.value,
                'alert_name': 'Vacuna Neumococo',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Vacuna antineumocócica - adulto mayor',
                'criteria': f'Edad: {age} años (≥60)',
                'due_date': calculate_due_date('vacuna_neumococo', 1825, is_urgent=True)  # 5 years
            })

        if age >= 18:
            # Tétanos - Refuerzo cada 10 años
            alerts.append({
                'alert_type': AlertTypeEnum.VACUNA_TETANOS.value,
                'alert_name': 'Refuerzo Tétanos',
                'priority': AlertPriorityEnum.BAJA.value,
                'reason': 'Refuerzo de vacuna antitetánica - cada 10 años',
                'criteria': f'Adulto',
                'due_date': calculate_due_date('vacuna_tetanos', 3650)  # 10 years
            })

        # ============================================
        # RIESGO CARDIOVASCULAR
        # ============================================

        if has_cardiovascular_risk or has_cardiovascular_disease or age >= 40:
            # Perfil lipídico - Frecuencia según riesgo
            if cardiovascular_risk_level in ['alto', 'muy_alto'] or has_cardiovascular_disease:
                interval = 365  # Annual for high risk or established disease
                priority = AlertPriorityEnum.ALTA.value
            elif has_cardiovascular_risk:
                interval = 730  # Every 2 years for medium risk
                priority = AlertPriorityEnum.MEDIA.value
            else:
                interval = 1095  # Every 3 years for low risk (age-based screening)
                priority = AlertPriorityEnum.MEDIA.value

            alerts.append({
                'alert_type': AlertTypeEnum.PERFIL_LIPIDICO.value,
                'alert_name': 'Perfil Lipídico',
                'priority': priority,
                'reason': f'Evaluación de riesgo cardiovascular - cada {interval//365} año(s)',
                'criteria': f'Edad: {age} años, Riesgo CV: {cardiovascular_risk_level or "a evaluar"}',
                'due_date': calculate_due_date('perfil_lipidico', interval, is_urgent=has_cardiovascular_risk)
            })

            # EKG
            if (has_cardiovascular_risk and cardiovascular_risk_level in ['alto', 'muy_alto']) or has_cardiovascular_disease or age >= 50:
                alerts.append({
                    'alert_type': AlertTypeEnum.EKG.value,
                    'alert_name': 'Electrocardiograma',
                    'priority': AlertPriorityEnum.ALTA.value if has_cardiovascular_disease else AlertPriorityEnum.MEDIA.value,
                    'reason': 'Evaluación de función cardíaca - anual',
                    'criteria': f'Edad: {age} años, Riesgo/Enfermedad CV',
                    'due_date': calculate_due_date('ekg', 365, is_urgent=has_cardiovascular_disease)
                })

        # ============================================
        # GRUPO B - ALERTAS POR CONDICIONES CRÓNICAS
        # ============================================

        # ------ EMBARAZO ------

        if is_pregnant and sex == 'F':
            # Ecografía obstétrica - Cada 6 semanas (o trimestral)
            alerts.append({
                'alert_type': AlertTypeEnum.ECOGRAFIA_OBSTETRICA.value,
                'alert_name': 'Ecografía Obstétrica',
                'priority': AlertPriorityEnum.URGENTE.value,
                'reason': 'Control prenatal - ecografías trimestrales',
                'criteria': 'Gestante',
                'due_date': calculate_due_date('ecografia_obstetrica', 90, is_urgent=True)  # ~3 months
            })

            # Hemograma
            alerts.append({
                'alert_type': AlertTypeEnum.HEMOGRAMA.value,
                'alert_name': 'Hemograma Completo',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Control prenatal - detección de anemia',
                'criteria': 'Gestante',
                'due_date': calculate_due_date('hemograma', 90, is_urgent=True)
            })

        # ------ HIPERTENSIÓN ARTERIAL ------

        if is_hypertensive:
            # Creatinina - Cada 6 meses
            alerts.append({
                'alert_type': AlertTypeEnum.CREATININA.value,
                'alert_name': 'Creatinina Sérica',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Evaluación de función renal en hipertenso - cada 6 meses',
                'criteria': 'Paciente hipertenso',
                'due_date': calculate_due_date('creatinina', 180, is_urgent=True)  # 6 months
            })

            # Potasio - Cada 6 meses
            alerts.append({
                'alert_type': AlertTypeEnum.POTASIO.value,
                'alert_name': 'Potasio Sérico',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control de electrolitos en hipertenso - cada 6 meses',
                'criteria': 'Paciente hipertenso (uso de diuréticos/IECA)',
                'due_date': calculate_due_date('potasio', 180)
            })

            # Microalbuminuria - Cada 6 meses
            alerts.append({
                'alert_type': AlertTypeEnum.MICROALBUMINURIA.value,
                'alert_name': 'Microalbuminuria',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Detección temprana de daño renal - cada 6 meses',
                'criteria': 'Paciente hipertenso',
                'due_date': calculate_due_date('microalbuminuria', 180, is_urgent=True)
            })

            # Parcial de orina - Anual
            alerts.append({
                'alert_type': AlertTypeEnum.PARCIAL_ORINA.value,
                'alert_name': 'Parcial de Orina',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Evaluación de función renal',
                'criteria': 'Paciente hipertenso',
                'due_date': calculate_due_date('parcial_orina', 365)
            })

        # ------ DIABETES MELLITUS ------

        if is_diabetic:
            # HbA1c - Cada 3 meses
            alerts.append({
                'alert_type': AlertTypeEnum.HBA1C.value,
                'alert_name': 'Hemoglobina Glicosilada (HbA1c)',
                'priority': AlertPriorityEnum.URGENTE.value,
                'reason': 'Control de diabetes - cada 3 meses',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('hba1c', 90, is_urgent=True)  # 3 months
            })

            # Fondo de ojo - Anual
            alerts.append({
                'alert_type': AlertTypeEnum.FONDO_OJO.value,
                'alert_name': 'Fondo de Ojo',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Tamizaje de retinopatía diabética - anual',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('fondo_ojo', 365, is_urgent=True)
            })

            # Valoración de pie diabético - Cada 3 meses
            alerts.append({
                'alert_type': AlertTypeEnum.VALORACION_PIE_DIABETICO.value,
                'alert_name': 'Valoración de Pie Diabético',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Prevención de úlceras y amputaciones - cada 3 meses',
                'criteria': 'Paciente diabético',
                'due_date': calculate_due_date('valoracion_pie_diabetico', 90, is_urgent=True)
            })

            # Creatinina y Microalbuminuria (si no ya en lista por HTA)
            if not is_hypertensive:
                alerts.append({
                    'alert_type': AlertTypeEnum.CREATININA.value,
                    'alert_name': 'Creatinina Sérica',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Evaluación de función renal en diabético - cada 6 meses',
                    'criteria': 'Paciente diabético',
                    'due_date': calculate_due_date('creatinina', 180, is_urgent=True)
                })

                alerts.append({
                    'alert_type': AlertTypeEnum.MICROALBUMINURIA.value,
                    'alert_name': 'Microalbuminuria',
                    'priority': AlertPriorityEnum.ALTA.value,
                    'reason': 'Detección temprana de nefropatía diabética - cada 6 meses',
                    'criteria': 'Paciente diabético',
                    'due_date': calculate_due_date('microalbuminuria', 180, is_urgent=True)
                })

        # ------ HIPOTIROIDISMO ------

        if has_hypothyroidism:
            # TSH - Cada 3-6 meses
            alerts.append({
                'alert_type': AlertTypeEnum.TSH.value,
                'alert_name': 'TSH (Hormona Estimulante de Tiroides)',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control de hipotiroidismo - cada 3-6 meses',
                'criteria': 'Paciente con hipotiroidismo',
                'due_date': calculate_due_date('tsh', 120)  # 4 months
            })

            # T4 libre - Cada 6 meses
            alerts.append({
                'alert_type': AlertTypeEnum.T4_LIBRE.value,
                'alert_name': 'T4 Libre',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Evaluación de función tiroidea - cada 6 meses',
                'criteria': 'Paciente con hipotiroidismo',
                'due_date': calculate_due_date('t4_libre', 180)
            })

        # ------ EPOC (Enfermedad Pulmonar Obstructiva Crónica) ------

        if has_copd:
            # Espirometría - Cada 6-12 meses
            alerts.append({
                'alert_type': AlertTypeEnum.ESPIROMETRIA.value,
                'alert_name': 'Espirometría',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Evaluación de función pulmonar en EPOC - cada 6-12 meses',
                'criteria': 'Paciente con EPOC',
                'due_date': calculate_due_date('espirometria', 270, is_urgent=True)  # 9 months
            })

            # Rayos X de tórax - Anual o según síntomas
            alerts.append({
                'alert_type': AlertTypeEnum.RAYOS_X_TORAX.value,
                'alert_name': 'Rayos X de Tórax',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Control de EPOC - anual',
                'criteria': 'Paciente con EPOC',
                'due_date': calculate_due_date('rayos_x_torax', 365)
            })

            # Gases arteriales - Según severidad
            alerts.append({
                'alert_type': AlertTypeEnum.GASES_ARTERIALES.value,
                'alert_name': 'Gases Arteriales',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Evaluación de oxigenación en EPOC severo',
                'criteria': 'Paciente con EPOC',
                'due_date': calculate_due_date('gases_arteriales', 180, is_urgent=True)
            })

        # ------ ASMA ------

        if has_asthma:
            # Espirometría - Cada 6-12 meses
            alerts.append({
                'alert_type': AlertTypeEnum.ESPIROMETRIA.value,
                'alert_name': 'Espirometría',
                'priority': AlertPriorityEnum.MEDIA.value,
                'reason': 'Evaluación de control de asma - cada 6-12 meses',
                'criteria': 'Paciente con asma',
                'due_date': calculate_due_date('espirometria', 270)  # 9 months
            })

        # ------ IRC (Insuficiencia Renal Crónica) ------

        if has_ckd:
            # Creatinina y clearance - Cada 3-6 meses según estadio
            alerts.append({
                'alert_type': AlertTypeEnum.CLEARANCE_CREATININA.value,
                'alert_name': 'Clearance de Creatinina (TFG)',
                'priority': AlertPriorityEnum.URGENTE.value,
                'reason': 'Control de función renal - cada 3-6 meses',
                'criteria': 'Paciente con IRC',
                'due_date': calculate_due_date('clearance_creatinina', 120, is_urgent=True)  # 4 months
            })

            # BUN (Nitrógeno ureico)
            alerts.append({
                'alert_type': AlertTypeEnum.BUN.value,
                'alert_name': 'BUN (Nitrógeno Ureico en Sangre)',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Control de función renal - cada 3-6 meses',
                'criteria': 'Paciente con IRC',
                'due_date': calculate_due_date('bun', 120, is_urgent=True)
            })

            # Hemograma - Control de anemia
            alerts.append({
                'alert_type': AlertTypeEnum.HEMOGRAMA.value,
                'alert_name': 'Hemograma Completo',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Control de anemia en IRC - cada 3-6 meses',
                'criteria': 'Paciente con IRC',
                'due_date': calculate_due_date('hemograma', 120, is_urgent=True)
            })

        # ------ ENFERMEDAD CARDIOVASCULAR ESTABLECIDA ------

        if has_cardiovascular_disease:
            # Ecocardiograma - Anual o según indicación
            alerts.append({
                'alert_type': AlertTypeEnum.ECOCARDIOGRAMA.value,
                'alert_name': 'Ecocardiograma',
                'priority': AlertPriorityEnum.ALTA.value,
                'reason': 'Evaluación de función cardíaca - anual',
                'criteria': 'Paciente con enfermedad cardiovascular',
                'due_date': calculate_due_date('ecocardiograma', 365, is_urgent=True)
            })

        return alerts

    @staticmethod
    def prioritize_alerts(alerts: List[Dict]) -> List[Dict]:
        """
        Sort alerts by priority (urgent > high > medium > low) and due date.
        """
        priority_order = {
            AlertPriorityEnum.URGENTE.value: 0,
            AlertPriorityEnum.ALTA.value: 1,
            AlertPriorityEnum.MEDIA.value: 2,
            AlertPriorityEnum.BAJA.value: 3
        }

        return sorted(
            alerts,
            key=lambda x: (
                priority_order.get(x['priority'], 4),
                x.get('due_date', date.today())
            )
        )
