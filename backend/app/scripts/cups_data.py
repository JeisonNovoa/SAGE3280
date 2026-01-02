"""
Script de datos oficiales de CUPS (Clasificación Única de Procedimientos en Salud)

Fuente oficial: Ministerio de Salud y Protección Social - Colombia
Resolución 8430 de 2020
Última actualización: Enero 2026

Referencias:
- https://www.minsalud.gov.co/
- Manual de Tarifas ISS/SOAT

NOTA: Códigos priorizados para SAGE3280 según:
- Resolución 3280/2018 (RIAS)
- Atención primaria en salud (APS)
- Seguimiento de pacientes crónicos (Grupo B)
- Programas preventivos (Grupo A)
"""

CUPS_CATALOG_DATA = [
    # ====================================================================
    # SECCIÓN 89 - CONSULTAS MÉDICAS Y VALORACIONES
    # ====================================================================

    # Consultas de Medicina General
    {
        "code": "890201",
        "description": "Consulta de primera vez por medicina general",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Medicina general",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Medicina general",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Consulta inicial por médico general - Primera vez que se atiende al paciente"
    },
    {
        "code": "890203",
        "description": "Consulta de control por medicina general",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Medicina general",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Medicina general",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Consulta de seguimiento por médico general - Paciente ya conocido"
    },

    # Consultas de Medicina Especializada
    {
        "code": "890202",
        "description": "Consulta de primera vez por medicina especializada",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Medicina especializada",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Medicina especializada",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Primera consulta con médico especialista (cardiología, nefrología, etc.)"
    },
    {
        "code": "890204",
        "description": "Consulta de control por medicina especializada",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Medicina especializada",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Medicina especializada",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Consulta de seguimiento con médico especialista"
    },

    # Consultas de Enfermería
    {
        "code": "890205",
        "description": "Consulta de enfermería",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Enfermería",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Valoración por profesional de enfermería - Educación, tamizaje, seguimiento"
    },

    # Control Prenatal
    {
        "code": "890301",
        "description": "Control prenatal",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Materno-infantil",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Ginecología y obstetricia",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Control prenatal según RIAS - Gestantes - Resolución 3280"
    },

    # Valoración de Crecimiento y Desarrollo
    {
        "code": "890701",
        "description": "Consulta de control del crecimiento y desarrollo (menores de 10 años)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Materno-infantil",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Pediatría",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Control de crecimiento y desarrollo - Primera infancia e infancia - RIAS"
    },

    # Valoración Nutricional
    {
        "code": "890271",
        "description": "Consulta de primera vez por nutrición y dietética",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Nutrición",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Nutrición y dietética",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Valoración nutricional inicial - Importante para Grupo B (diabetes, HTA, obesidad)"
    },
    {
        "code": "890273",
        "description": "Consulta de control por nutrición y dietética",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Nutrición",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Nutrición y dietética",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Control nutricional - Seguimiento de pacientes crónicos"
    },

    # Consulta de Psicología
    {
        "code": "890251",
        "description": "Consulta de primera vez por psicología",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Salud mental",
        "procedure_type": "Preventivo",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Psicología",
        "estimated_duration_minutes": 40,
        "is_active": True,
        "notes": "Valoración inicial en salud mental - RIAS salud mental"
    },
    {
        "code": "890253",
        "description": "Consulta de control por psicología",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Salud mental",
        "procedure_type": "Preventivo",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Psicología",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Seguimiento psicológico"
    },

    # Consulta de Odontología
    {
        "code": "890208",
        "description": "Consulta de primera vez por odontología general",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Odontología",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Odontología",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Consulta inicial odontológica - RIAS salud bucal"
    },
    {
        "code": "890210",
        "description": "Consulta de control por odontología general",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Consultas médicas",
        "subcategory": "Odontología",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Odontología",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Control odontológico"
    },

    # ====================================================================
    # SECCIÓN 87 - PROCEDIMIENTOS DE ENFERMERÍA Y SIGNOS VITALES
    # ====================================================================

    {
        "code": "870101",
        "description": "Toma de presión arterial",
        "chapter": "87 - Procedimientos de enfermería",
        "category": "Signos vitales",
        "subcategory": "Monitoreo cardiovascular",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 5,
        "is_active": True,
        "notes": "Medición de presión arterial - Fundamental en HTA y riesgo cardiovascular"
    },
    {
        "code": "870102",
        "description": "Toma de temperatura corporal",
        "chapter": "87 - Procedimientos de enfermería",
        "category": "Signos vitales",
        "subcategory": "Monitoreo general",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 3,
        "is_active": True,
        "notes": "Medición de temperatura corporal"
    },
    {
        "code": "871101",
        "description": "Curva de tolerancia a la glucosa (3 muestras)",
        "chapter": "87 - Procedimientos de enfermería",
        "category": "Procedimientos diagnósticos",
        "subcategory": "Endocrinología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 150,
        "is_active": True,
        "notes": "Prueba de tolerancia oral a la glucosa - Diagnóstico de diabetes gestacional"
    },

    # ====================================================================
    # SECCIÓN 89.04 - PROCEDIMIENTOS PREVENTIVOS Y TAMIZAJES
    # ====================================================================

    # Citología Cervicovaginal
    {
        "code": "890401",
        "description": "Citología cervicovaginal (Papanicolaou)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Prevención y tamizaje",
        "subcategory": "Cáncer cervicouterino",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Ginecología",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Tamizaje de cáncer de cuello uterino - RIAS mujer - Prioritario"
    },

    # Mamografía
    {
        "code": "890601",
        "description": "Mamografía bilateral",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Prevención y tamizaje",
        "subcategory": "Cáncer de mama",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Radiología",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Tamizaje de cáncer de mama - Mujeres 50-69 años - RIAS"
    },

    # Prueba de VIH
    {
        "code": "906239",
        "description": "Prueba de detección de anticuerpos VIH (tamizaje)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Prevención y tamizaje",
        "subcategory": "Enfermedades infecciosas",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Tamizaje de VIH - Gestantes y población en riesgo"
    },

    # Tamizaje de Cáncer de Próstata
    {
        "code": "902263",
        "description": "Antígeno prostático específico (PSA)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Prevención y tamizaje",
        "subcategory": "Cáncer de próstata",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Tamizaje de cáncer de próstata - Hombres >50 años"
    },

    # ====================================================================
    # SECCIÓN 90 - LABORATORIO CLÍNICO - QUÍMICA SANGUÍNEA
    # ====================================================================

    # Glucosa
    {
        "code": "902215",
        "description": "Glicemia en ayunas",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Química sanguínea",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Glucemia basal - Fundamental en diabetes y riesgo cardiovascular"
    },
    {
        "code": "902210",
        "description": "Hemoglobina glicosilada (HbA1c)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Química sanguínea",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Control glucémico a 3 meses - Pacientes diabéticos - Grupo B"
    },
    {
        "code": "902216",
        "description": "Glucemia posprandial (2 horas)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Química sanguínea",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Glucemia después de las comidas - Control diabetes"
    },

    # Lípidos (Perfil Lipídico)
    {
        "code": "902216",
        "description": "Colesterol total",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Perfil lipídico",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Colesterol total - Riesgo cardiovascular"
    },
    {
        "code": "902217",
        "description": "Colesterol HDL (lipoproteína de alta densidad)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Perfil lipídico",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Colesterol HDL (bueno) - Riesgo cardiovascular"
    },
    {
        "code": "902218",
        "description": "Colesterol LDL (lipoproteína de baja densidad)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Perfil lipídico",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Colesterol LDL (malo) - Riesgo cardiovascular - Meta <100 mg/dL"
    },
    {
        "code": "902219",
        "description": "Triglicéridos",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Perfil lipídico",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Triglicéridos - Parte del perfil lipídico - Riesgo cardiovascular"
    },

    # Función Renal
    {
        "code": "902252",
        "description": "Creatinina en suero",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función renal",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Creatinina sérica - Función renal - Pacientes con HTA, diabetes, ERC"
    },
    {
        "code": "902253",
        "description": "Nitrógeno ureico (BUN)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función renal",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "BUN - Valoración de función renal"
    },
    {
        "code": "902621",
        "description": "Depuración de creatinina en orina de 24 horas",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función renal",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Tasa de filtración glomerular - Diagnóstico y estadificación de ERC"
    },
    {
        "code": "902610",
        "description": "Microalbuminuria en orina",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función renal",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Detección temprana de nefropatía diabética - Pacientes con diabetes"
    },

    # Función Hepática
    {
        "code": "902231",
        "description": "Transaminasa glutámico oxalacética (TGO/AST)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función hepática",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "AST - Función hepática - Monitoreo de medicamentos hepatotóxicos"
    },
    {
        "code": "902232",
        "description": "Transaminasa glutámico pirúvica (TGP/ALT)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función hepática",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "ALT - Marcador específico de daño hepático"
    },

    # Función Tiroidea
    {
        "code": "902809",
        "description": "TSH (Hormona estimulante de tiroides)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función tiroidea",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "TSH - Tamizaje y seguimiento de hipotiroidismo/hipertiroidismo"
    },
    {
        "code": "902810",
        "description": "T4 libre (Tiroxina libre)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Función tiroidea",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "T4 libre - Confirmación de alteraciones tiroideas"
    },

    # ====================================================================
    # SECCIÓN 90 - LABORATORIO CLÍNICO - HEMATOLOGÍA
    # ====================================================================

    {
        "code": "902210",
        "description": "Hemograma completo (hemoleucograma)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Hematología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Cuadro hemático completo - Anemia, infecciones, leucemias"
    },
    {
        "code": "902008",
        "description": "Recuento de plaquetas",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Hematología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Conteo de plaquetas - Trastornos de coagulación"
    },
    {
        "code": "902037",
        "description": "Velocidad de sedimentación globular (VSG)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Hematología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 60,
        "is_active": True,
        "notes": "VSG - Marcador inespecífico de inflamación"
    },

    # ====================================================================
    # SECCIÓN 90 - LABORATORIO CLÍNICO - OTROS
    # ====================================================================

    # Parcial de Orina
    {
        "code": "902601",
        "description": "Parcial de orina (uroanálisis)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Uroanálisis",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Examen general de orina - Infecciones urinarias, diabetes, función renal"
    },
    {
        "code": "902602",
        "description": "Urocultivo con antibiograma",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Microbiología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Cultivo de orina - Identificación de bacteria y sensibilidad antibiótica"
    },

    # Serología
    {
        "code": "906031",
        "description": "Grupo sanguíneo ABO y factor Rh",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Serología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Tipificación sanguínea - Obligatorio en gestantes"
    },
    {
        "code": "906221",
        "description": "Prueba de embarazo en sangre (Beta-HCG cuantitativa)",
        "chapter": "90 - Laboratorio clínico",
        "category": "Laboratorio",
        "subcategory": "Serología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Laboratorio clínico",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Beta-HCG - Confirmación de embarazo"
    },

    # ====================================================================
    # SECCIÓN 88 - IMÁGENES DIAGNÓSTICAS
    # ====================================================================

    # Radiología
    {
        "code": "881201",
        "description": "Radiografía de tórax PA (posteroanterior)",
        "chapter": "88 - Imágenes diagnósticas",
        "category": "Radiología",
        "subcategory": "Tórax",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Radiología",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Rx de tórax - Neumonía, tuberculosis, EPOC, insuficiencia cardíaca"
    },
    {
        "code": "881401",
        "description": "Radiografía de abdomen simple",
        "chapter": "88 - Imágenes diagnósticas",
        "category": "Radiología",
        "subcategory": "Abdomen",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Radiología",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Rx de abdomen - Obstrucción intestinal, cálculos renales"
    },

    # Ecografía
    {
        "code": "881801",
        "description": "Ecografía obstétrica",
        "chapter": "88 - Imágenes diagnósticas",
        "category": "Ecografía",
        "subcategory": "Obstetricia",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Radiología",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Ecografía de embarazo - Control prenatal según RIAS"
    },
    {
        "code": "881802",
        "description": "Ecografía de abdomen total",
        "chapter": "88 - Imágenes diagnósticas",
        "category": "Ecografía",
        "subcategory": "Abdomen",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Radiología",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Ecografía abdominal completa - Hígado, vesícula, riñones, bazo"
    },
    {
        "code": "881805",
        "description": "Ecografía renal y de vías urinarias",
        "chapter": "88 - Imágenes diagnósticas",
        "category": "Ecografía",
        "subcategory": "Urología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Radiología",
        "estimated_duration_minutes": 25,
        "is_active": True,
        "notes": "Ecografía renal - Enfermedad renal crónica, litiasis"
    },

    # Electrocardiograma
    {
        "code": "893101",
        "description": "Electrocardiograma de reposo (ECG)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Electrodiagnóstico",
        "subcategory": "Cardiología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Cardiología",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "ECG de 12 derivaciones - HTA, cardiopatías, arritmias - Grupo B"
    },
    {
        "code": "893102",
        "description": "Prueba de esfuerzo (ergometría)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Electrodiagnóstico",
        "subcategory": "Cardiología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Cardiología",
        "estimated_duration_minutes": 45,
        "is_active": True,
        "notes": "Prueba de esfuerzo - Cardiopatía isquémica, capacidad funcional"
    },

    # Ecocardiograma
    {
        "code": "881818",
        "description": "Ecocardiograma transtorácico",
        "chapter": "88 - Imágenes diagnósticas",
        "category": "Ecografía",
        "subcategory": "Cardiología",
        "procedure_type": "Diagnóstico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Cardiología",
        "estimated_duration_minutes": 40,
        "is_active": True,
        "notes": "Ecocardiograma - Insuficiencia cardíaca, valvulopatías, hipertrofia ventricular"
    },

    # ====================================================================
    # SECCIÓN 99 - VACUNACIÓN
    # ====================================================================

    {
        "code": "993101",
        "description": "Aplicación de biológico - Vacuna triple viral (sarampión, rubéola, parotiditis)",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Infantil",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna triple viral - Esquema PAI - Primera infancia"
    },
    {
        "code": "993102",
        "description": "Aplicación de biológico - Vacuna antipoliomielítica oral (VOP)",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Infantil",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 5,
        "is_active": True,
        "notes": "Vacuna antipolio oral - Esquema PAI"
    },
    {
        "code": "993103",
        "description": "Aplicación de biológico - Vacuna DPT (difteria, tosferina, tétanos)",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Infantil",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna DPT - Esquema PAI - Primera infancia"
    },
    {
        "code": "993104",
        "description": "Aplicación de biológico - Vacuna BCG (tuberculosis)",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Infantil",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna BCG - Recién nacidos - Prevención de tuberculosis"
    },
    {
        "code": "993105",
        "description": "Aplicación de biológico - Vacuna hepatitis B",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Infantil y adultos",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna hepatitis B - Recién nacidos y grupos de riesgo"
    },
    {
        "code": "993106",
        "description": "Aplicación de biológico - Vacuna antiinfluenza",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Adultos y grupos de riesgo",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna influenza - Adultos mayores, gestantes, crónicos - RIAS"
    },
    {
        "code": "993107",
        "description": "Aplicación de biológico - Vacuna neumococo",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Infantil y adultos mayores",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna antineumocócica - Menores de 5 años y adultos mayores"
    },
    {
        "code": "993108",
        "description": "Aplicación de biológico - Vacuna VPH (virus papiloma humano)",
        "chapter": "99 - Vacunación",
        "category": "Vacunación",
        "subcategory": "Adolescentes",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Vacuna VPH - Niñas 9-17 años - Prevención cáncer cervicouterino - RIAS"
    },

    # ====================================================================
    # PROCEDIMIENTOS ODONTOLÓGICOS BÁSICOS
    # ====================================================================

    {
        "code": "997101",
        "description": "Aplicación de sellantes de fotocurado",
        "chapter": "99 - Procedimientos odontológicos",
        "category": "Odontología preventiva",
        "subcategory": "Prevención",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Odontología",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Sellantes dentales - Prevención de caries - Niños - RIAS salud bucal"
    },
    {
        "code": "997102",
        "description": "Aplicación tópica de flúor",
        "chapter": "99 - Procedimientos odontológicos",
        "category": "Odontología preventiva",
        "subcategory": "Prevención",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Odontología",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Fluorización dental - Prevención de caries - RIAS salud bucal"
    },
    {
        "code": "997301",
        "description": "Detartraje supragingival (limpieza dental)",
        "chapter": "99 - Procedimientos odontológicos",
        "category": "Odontología preventiva",
        "subcategory": "Higiene oral",
        "procedure_type": "Preventivo",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Odontología",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Profilaxis dental - Remoción de placa y sarro"
    },

    # ====================================================================
    # PROCEDIMIENTOS TERAPÉUTICOS AMBULATORIOS
    # ====================================================================

    {
        "code": "893501",
        "description": "Nebulización con broncodilatador",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Terapia respiratoria",
        "subcategory": "Nebulización",
        "procedure_type": "Terapéutico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 20,
        "is_active": True,
        "notes": "Nebulización - Asma, EPOC, bronquitis - Grupo B respiratorio"
    },
    {
        "code": "893502",
        "description": "Oxigenoterapia ambulatoria",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Terapia respiratoria",
        "subcategory": "Oxigenoterapia",
        "procedure_type": "Terapéutico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 60,
        "is_active": True,
        "notes": "Oxígeno suplementario - EPOC severo, insuficiencia respiratoria"
    },

    # Inyectología
    {
        "code": "891101",
        "description": "Inyección intramuscular (IM)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Procedimientos de enfermería",
        "subcategory": "Inyectología",
        "procedure_type": "Terapéutico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 5,
        "is_active": True,
        "notes": "Aplicación de medicamento intramuscular"
    },
    {
        "code": "891102",
        "description": "Inyección intravenosa (IV)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Procedimientos de enfermería",
        "subcategory": "Inyectología",
        "procedure_type": "Terapéutico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 10,
        "is_active": True,
        "notes": "Aplicación de medicamento endovenoso"
    },
    {
        "code": "891103",
        "description": "Inyección subcutánea (SC)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Procedimientos de enfermería",
        "subcategory": "Inyectología",
        "procedure_type": "Terapéutico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 5,
        "is_active": True,
        "notes": "Aplicación subcutánea - Insulina, heparina, vacunas"
    },

    # Curaciones
    {
        "code": "891201",
        "description": "Curación de heridas (simple)",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Procedimientos de enfermería",
        "subcategory": "Curaciones",
        "procedure_type": "Terapéutico",
        "complexity_level": "Baja",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 15,
        "is_active": True,
        "notes": "Curación de heridas superficiales - Pie diabético, úlceras"
    },
    {
        "code": "891202",
        "description": "Curación de úlceras y escaras",
        "chapter": "89 - Otros procedimientos médicos",
        "category": "Procedimientos de enfermería",
        "subcategory": "Curaciones",
        "procedure_type": "Terapéutico",
        "complexity_level": "Media",
        "ambulatory": True,
        "requires_hospitalization": False,
        "specialty": "Enfermería",
        "estimated_duration_minutes": 30,
        "is_active": True,
        "notes": "Curación de úlceras - Pie diabético, úlceras por presión - Grupo B"
    },
]


def get_cups_data():
    """
    Retorna la lista completa de códigos CUPS para poblar el catálogo.

    Returns:
        list: Lista de diccionarios con datos de códigos CUPS
    """
    return CUPS_CATALOG_DATA


def get_cups_count():
    """
    Retorna el número total de códigos CUPS en el catálogo.

    Returns:
        int: Total de códigos CUPS
    """
    return len(CUPS_CATALOG_DATA)


def get_cups_by_category():
    """
    Agrupa códigos CUPS por categoría.

    Returns:
        dict: Diccionario con categorías como claves y listas de códigos como valores
    """
    categories = {}
    for cups in CUPS_CATALOG_DATA:
        category = cups['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(cups)
    return categories


def get_cups_stats():
    """
    Retorna estadísticas del catálogo CUPS.

    Returns:
        dict: Estadísticas del catálogo
    """
    by_category = get_cups_by_category()

    procedure_types = {}
    complexity_levels = {}

    for cups in CUPS_CATALOG_DATA:
        proc_type = cups['procedure_type']
        complexity = cups['complexity_level']

        procedure_types[proc_type] = procedure_types.get(proc_type, 0) + 1
        complexity_levels[complexity] = complexity_levels.get(complexity, 0) + 1

    return {
        'total_codes': len(CUPS_CATALOG_DATA),
        'total_categories': len(by_category),
        'by_category': {cat: len(codes) for cat, codes in by_category.items()},
        'by_procedure_type': procedure_types,
        'by_complexity': complexity_levels,
        'ambulatory_procedures': sum(1 for c in CUPS_CATALOG_DATA if c['ambulatory']),
        'hospitalization_required': sum(1 for c in CUPS_CATALOG_DATA if c['requires_hospitalization'])
    }


if __name__ == "__main__":
    """Muestra estadísticas del catálogo al ejecutar el script"""
    import json

    stats = get_cups_stats()
    print("=" * 80)
    print("CATÁLOGO CUPS PARA SAGE3280")
    print("=" * 80)
    print(f"\nTotal de códigos: {stats['total_codes']}")
    print(f"Total de categorías: {stats['total_categories']}")

    print("\n📋 Códigos por Categoría:")
    for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {category}: {count}")

    print("\n🏥 Por Tipo de Procedimiento:")
    for proc_type, count in stats['by_procedure_type'].items():
        print(f"  - {proc_type}: {count}")

    print("\n⚡ Por Nivel de Complejidad:")
    for complexity, count in stats['by_complexity'].items():
        print(f"  - {complexity}: {count}")

    print(f"\n✅ Ambulatorios: {stats['ambulatory_procedures']}")
    print(f"🏥 Requieren hospitalización: {stats['hospitalization_required']}")
    print("\n" + "=" * 80)
