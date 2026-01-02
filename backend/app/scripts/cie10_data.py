"""
CIE-10 Catalog Data - Colombian Health System
Clasificación Internacional de Enfermedades, 10ª Revisión

Fuentes:
- Organización Mundial de la Salud (OMS)
- Ministerio de Salud y Protección Social de Colombia
- RIPS (Registro Individual de Prestación de Servicios)

Este catálogo contiene códigos CIE-10 prioritarios para atención primaria
y seguimiento de enfermedades crónicas en el contexto colombiano.

Estructura: ~200 códigos comunes organizados por capítulos
"""

CIE10_CATALOG_DATA = [
    # ========================================================================
    # CAPÍTULO I: ENFERMEDADES INFECCIOSAS Y PARASITARIAS (A00-B99)
    # ========================================================================
    {
        "code": "A09",
        "short_description": "Diarrea y gastroenteritis de presunto origen infeccioso",
        "full_description": "Diarrea y gastroenteritis de presunto origen infeccioso (diarrea infecciosa, disentería NE, enteritis infecciosa)",
        "chapter": "I - Enfermedades infecciosas y parasitarias",
        "chapter_code": "I",
        "category": "Enfermedades infecciosas intestinales",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código muy común en atención primaria"
    },
    {
        "code": "B24",
        "short_description": "Enfermedad por VIH, sin otra especificación",
        "full_description": "Enfermedad por virus de la inmunodeficiencia humana [VIH], sin otra especificación",
        "chapter": "I - Enfermedades infecciosas y parasitarias",
        "chapter_code": "I",
        "category": "VIH/SIDA",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere seguimiento especial"
    },

    # ========================================================================
    # CAPÍTULO II: NEOPLASIAS (C00-D48)
    # ========================================================================
    {
        "code": "C50",
        "short_description": "Tumor maligno de la mama",
        "full_description": "Tumor maligno de la mama (neoplasia maligna de mama)",
        "chapter": "II - Neoplasias",
        "chapter_code": "II",
        "category": "Tumores malignos",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere tamización y seguimiento"
    },
    {
        "code": "C53",
        "short_description": "Tumor maligno del cuello del útero",
        "full_description": "Tumor maligno del cuello del útero (cáncer de cérvix)",
        "chapter": "II - Neoplasias",
        "chapter_code": "II",
        "category": "Tumores malignos",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Tamización con citología/VPH"
    },
    {
        "code": "C61",
        "short_description": "Tumor maligno de la próstata",
        "full_description": "Tumor maligno de la próstata (cáncer de próstata)",
        "chapter": "II - Neoplasias",
        "chapter_code": "II",
        "category": "Tumores malignos",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Tamización en hombres >50 años"
    },

    # ========================================================================
    # CAPÍTULO IV: ENFERMEDADES ENDOCRINAS, NUTRICIONALES Y METABÓLICAS (E00-E90)
    # ========================================================================
    # DIABETES MELLITUS TIPO 1 (E10)
    {
        "code": "E10",
        "short_description": "Diabetes mellitus tipo 1",
        "full_description": "Diabetes mellitus tipo 1 (diabetes insulinodependiente)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere insulina desde el diagnóstico"
    },
    {
        "code": "E10.9",
        "short_description": "Diabetes mellitus tipo 1 sin complicaciones",
        "full_description": "Diabetes mellitus tipo 1 sin mención de complicación",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E10",
        "is_common": True,
        "notes": None
    },

    # DIABETES MELLITUS TIPO 2 (E11) - MUY IMPORTANTE PARA SAGE3280
    {
        "code": "E11",
        "short_description": "Diabetes mellitus tipo 2",
        "full_description": "Diabetes mellitus tipo 2 (diabetes no insulinodependiente)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código prioritario para SAGE3280 - Grupo B"
    },
    {
        "code": "E11.0",
        "short_description": "Diabetes mellitus tipo 2 con coma",
        "full_description": "Diabetes mellitus tipo 2 con coma (hiperosmolar, hipoglucémico)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": False,
        "notes": "Urgencia médica"
    },
    {
        "code": "E11.2",
        "short_description": "Diabetes mellitus tipo 2 con complicaciones renales",
        "full_description": "Diabetes mellitus tipo 2 con complicaciones renales (nefropatía diabética)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": "Requiere monitoreo de función renal"
    },
    {
        "code": "E11.3",
        "short_description": "Diabetes mellitus tipo 2 con complicaciones oftálmicas",
        "full_description": "Diabetes mellitus tipo 2 con complicaciones oftálmicas (retinopatía diabética)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": "Requiere valoración oftalmológica anual"
    },
    {
        "code": "E11.4",
        "short_description": "Diabetes mellitus tipo 2 con complicaciones neurológicas",
        "full_description": "Diabetes mellitus tipo 2 con complicaciones neurológicas (neuropatía diabética)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": "Neuropatía periférica, pie diabético"
    },
    {
        "code": "E11.5",
        "short_description": "Diabetes mellitus tipo 2 con complicaciones circulatorias periféricas",
        "full_description": "Diabetes mellitus tipo 2 con complicaciones circulatorias periféricas (vasculopatía diabética)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": "Riesgo de amputación"
    },
    {
        "code": "E11.6",
        "short_description": "Diabetes mellitus tipo 2 con otras complicaciones especificadas",
        "full_description": "Diabetes mellitus tipo 2 con otras complicaciones especificadas",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": None
    },
    {
        "code": "E11.7",
        "short_description": "Diabetes mellitus tipo 2 con complicaciones múltiples",
        "full_description": "Diabetes mellitus tipo 2 con complicaciones múltiples",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": "Requiere manejo multidisciplinario"
    },
    {
        "code": "E11.9",
        "short_description": "Diabetes mellitus tipo 2 sin complicaciones",
        "full_description": "Diabetes mellitus tipo 2 sin mención de complicación",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Diabetes mellitus",
        "is_subcategory": True,
        "parent_code": "E11",
        "is_common": True,
        "notes": "Código más usado para DM2"
    },

    # TRASTORNOS DE LA TIROIDES (E00-E07)
    {
        "code": "E03",
        "short_description": "Otros hipotiroidismos",
        "full_description": "Otros hipotiroidismos (deficiencia de hormona tiroidea)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Trastornos de la glándula tiroides",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere reemplazo hormonal"
    },
    {
        "code": "E03.9",
        "short_description": "Hipotiroidismo no especificado",
        "full_description": "Hipotiroidismo no especificado",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Trastornos de la glándula tiroides",
        "is_subcategory": True,
        "parent_code": "E03",
        "is_common": True,
        "notes": None
    },
    {
        "code": "E05",
        "short_description": "Tirotoxicosis (hipertiroidismo)",
        "full_description": "Tirotoxicosis [hipertiroidismo] (exceso de hormona tiroidea)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Trastornos de la glándula tiroides",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere tratamiento especializado"
    },

    # OBESIDAD Y DISLIPIDEMIA (E65-E68, E78)
    {
        "code": "E66",
        "short_description": "Obesidad",
        "full_description": "Obesidad (exceso de peso corporal)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Obesidad y sobrepeso",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Factor de riesgo cardiovascular"
    },
    {
        "code": "E66.0",
        "short_description": "Obesidad debida a exceso de calorías",
        "full_description": "Obesidad debida a exceso de calorías",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Obesidad y sobrepeso",
        "is_subcategory": True,
        "parent_code": "E66",
        "is_common": True,
        "notes": None
    },
    {
        "code": "E66.9",
        "short_description": "Obesidad no especificada",
        "full_description": "Obesidad no especificada",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Obesidad y sobrepeso",
        "is_subcategory": True,
        "parent_code": "E66",
        "is_common": True,
        "notes": None
    },
    {
        "code": "E78",
        "short_description": "Trastornos del metabolismo de las lipoproteínas",
        "full_description": "Trastornos del metabolismo de las lipoproteínas y otras lipidemias",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Dislipidemia",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Dislipidemia, colesterol alto"
    },
    {
        "code": "E78.0",
        "short_description": "Hipercolesterolemia pura",
        "full_description": "Hipercolesterolemia pura (colesterol elevado)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Dislipidemia",
        "is_subcategory": True,
        "parent_code": "E78",
        "is_common": True,
        "notes": "Requiere manejo dietético y/o farmacológico"
    },
    {
        "code": "E78.5",
        "short_description": "Hiperlipidemia no especificada",
        "full_description": "Hiperlipidemia no especificada (dislipidemia mixta)",
        "chapter": "IV - Enfermedades endocrinas, nutricionales y metabólicas",
        "chapter_code": "IV",
        "category": "Dislipidemia",
        "is_subcategory": True,
        "parent_code": "E78",
        "is_common": True,
        "notes": None
    },

    # ========================================================================
    # CAPÍTULO IX: ENFERMEDADES DEL SISTEMA CIRCULATORIO (I00-I99)
    # MUY IMPORTANTE PARA SAGE3280
    # ========================================================================
    # HIPERTENSIÓN ARTERIAL (I10-I15) - CÓDIGO PRIORITARIO
    {
        "code": "I10",
        "short_description": "Hipertensión esencial (primaria)",
        "full_description": "Hipertensión esencial (primaria) - HTA sin causa identificable",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedades hipertensivas",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código prioritario para SAGE3280 - Grupo B. Código más usado para HTA"
    },
    {
        "code": "I11",
        "short_description": "Enfermedad cardíaca hipertensiva",
        "full_description": "Enfermedad cardíaca hipertensiva (hipertensión con afectación cardíaca)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedades hipertensivas",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "HTA con compromiso del corazón"
    },
    {
        "code": "I11.9",
        "short_description": "Enfermedad cardíaca hipertensiva sin insuficiencia cardíaca",
        "full_description": "Enfermedad cardíaca hipertensiva sin insuficiencia cardíaca (congestiva)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedades hipertensivas",
        "is_subcategory": True,
        "parent_code": "I11",
        "is_common": True,
        "notes": None
    },
    {
        "code": "I12",
        "short_description": "Enfermedad renal hipertensiva",
        "full_description": "Enfermedad renal hipertensiva (hipertensión con compromiso renal)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedades hipertensivas",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "HTA con daño renal"
    },
    {
        "code": "I13",
        "short_description": "Enfermedad cardíaca y renal hipertensiva",
        "full_description": "Enfermedad cardíaca y renal hipertensiva (hipertensión con compromiso cardio-renal)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedades hipertensivas",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "HTA con daño cardíaco y renal"
    },
    {
        "code": "I15",
        "short_description": "Hipertensión secundaria",
        "full_description": "Hipertensión secundaria (HTA con causa identificable)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedades hipertensivas",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": False,
        "notes": "HTA de causa renal, endocrina, etc."
    },

    # ENFERMEDAD ISQUÉMICA DEL CORAZÓN (I20-I25)
    {
        "code": "I20",
        "short_description": "Angina de pecho",
        "full_description": "Angina de pecho (dolor precordial isquémico)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Cardiopatía isquémica",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere evaluación cardiológica"
    },
    {
        "code": "I21",
        "short_description": "Infarto agudo del miocardio",
        "full_description": "Infarto agudo del miocardio (ataque cardíaco)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Cardiopatía isquémica",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Urgencia cardiovascular"
    },
    {
        "code": "I25",
        "short_description": "Enfermedad isquémica crónica del corazón",
        "full_description": "Enfermedad isquémica crónica del corazón (cardiopatía isquémica)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Cardiopatía isquémica",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Incluye antecedente de IAM"
    },
    {
        "code": "I25.1",
        "short_description": "Enfermedad aterosclerótica del corazón",
        "full_description": "Enfermedad aterosclerótica del corazón (enfermedad coronaria)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Cardiopatía isquémica",
        "is_subcategory": True,
        "parent_code": "I25",
        "is_common": True,
        "notes": None
    },

    # INSUFICIENCIA CARDÍACA (I50)
    {
        "code": "I50",
        "short_description": "Insuficiencia cardíaca",
        "full_description": "Insuficiencia cardíaca (falla del corazón)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Insuficiencia cardíaca",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere seguimiento estrecho"
    },
    {
        "code": "I50.0",
        "short_description": "Insuficiencia cardíaca congestiva",
        "full_description": "Insuficiencia cardíaca congestiva (ICC)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Insuficiencia cardíaca",
        "is_subcategory": True,
        "parent_code": "I50",
        "is_common": True,
        "notes": "Requiere control de líquidos y peso"
    },
    {
        "code": "I50.9",
        "short_description": "Insuficiencia cardíaca no especificada",
        "full_description": "Insuficiencia cardíaca no especificada",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Insuficiencia cardíaca",
        "is_subcategory": True,
        "parent_code": "I50",
        "is_common": True,
        "notes": None
    },

    # ENFERMEDAD CEREBROVASCULAR (I60-I69)
    {
        "code": "I63",
        "short_description": "Infarto cerebral",
        "full_description": "Infarto cerebral (ACV isquémico, derrame cerebral)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedad cerebrovascular",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Emergencia neurológica"
    },
    {
        "code": "I64",
        "short_description": "Accidente vascular encefálico",
        "full_description": "Accidente vascular encefálico agudo, no especificado como hemorrágico o isquémico",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedad cerebrovascular",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "ACV sin especificar tipo"
    },
    {
        "code": "I69",
        "short_description": "Secuelas de enfermedad cerebrovascular",
        "full_description": "Secuelas de enfermedad cerebrovascular (secuelas de ACV)",
        "chapter": "IX - Enfermedades del sistema circulatorio",
        "chapter_code": "IX",
        "category": "Enfermedad cerebrovascular",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Antecedente de ACV"
    },

    # ========================================================================
    # CAPÍTULO X: ENFERMEDADES DEL SISTEMA RESPIRATORIO (J00-J99)
    # ========================================================================
    {
        "code": "J18",
        "short_description": "Neumonía",
        "full_description": "Neumonía, organismo no especificado",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Infecciones respiratorias bajas",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere antibioticoterapia"
    },
    {
        "code": "J44",
        "short_description": "EPOC",
        "full_description": "Enfermedad pulmonar obstructiva crónica (EPOC)",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código prioritario para SAGE3280 - Grupo B"
    },
    {
        "code": "J44.0",
        "short_description": "EPOC con infección respiratoria aguda",
        "full_description": "Enfermedad pulmonar obstructiva crónica con infección aguda de las vías respiratorias inferiores",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": True,
        "parent_code": "J44",
        "is_common": True,
        "notes": "Exacerbación infecciosa"
    },
    {
        "code": "J44.1",
        "short_description": "EPOC con exacerbación aguda",
        "full_description": "Enfermedad pulmonar obstructiva crónica con exacerbación aguda, no especificada",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": True,
        "parent_code": "J44",
        "is_common": True,
        "notes": "Crisis de EPOC"
    },
    {
        "code": "J44.9",
        "short_description": "EPOC no especificada",
        "full_description": "Enfermedad pulmonar obstructiva crónica, no especificada",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": True,
        "parent_code": "J44",
        "is_common": True,
        "notes": None
    },
    {
        "code": "J45",
        "short_description": "Asma",
        "full_description": "Asma bronquial",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código prioritario para SAGE3280 - Grupo B"
    },
    {
        "code": "J45.0",
        "short_description": "Asma predominantemente alérgica",
        "full_description": "Asma predominantemente alérgica (asma extrínseca)",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": True,
        "parent_code": "J45",
        "is_common": True,
        "notes": None
    },
    {
        "code": "J45.9",
        "short_description": "Asma no especificada",
        "full_description": "Asma, no especificada",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": True,
        "parent_code": "J45",
        "is_common": True,
        "notes": None
    },
    {
        "code": "J46",
        "short_description": "Estado asmático",
        "full_description": "Estado asmático (crisis asmática severa)",
        "chapter": "X - Enfermedades del sistema respiratorio",
        "chapter_code": "X",
        "category": "Enfermedades crónicas respiratorias",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Urgencia respiratoria"
    },

    # ========================================================================
    # CAPÍTULO XIV: ENFERMEDADES DEL SISTEMA GENITOURINARIO (N00-N99)
    # ========================================================================
    {
        "code": "N18",
        "short_description": "Enfermedad renal crónica (ERC)",
        "full_description": "Enfermedad renal crónica (insuficiencia renal crónica)",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código prioritario para SAGE3280 - Grupo B"
    },
    {
        "code": "N18.1",
        "short_description": "ERC estadio 1",
        "full_description": "Enfermedad renal crónica, estadio 1 (daño renal con TFG normal ≥90)",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": True,
        "parent_code": "N18",
        "is_common": True,
        "notes": "TFG ≥90 ml/min/1.73m²"
    },
    {
        "code": "N18.2",
        "short_description": "ERC estadio 2",
        "full_description": "Enfermedad renal crónica, estadio 2 (TFG levemente disminuida 60-89)",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": True,
        "parent_code": "N18",
        "is_common": True,
        "notes": "TFG 60-89 ml/min/1.73m²"
    },
    {
        "code": "N18.3",
        "short_description": "ERC estadio 3",
        "full_description": "Enfermedad renal crónica, estadio 3 (TFG moderadamente disminuida 30-59)",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": True,
        "parent_code": "N18",
        "is_common": True,
        "notes": "TFG 30-59 ml/min/1.73m²"
    },
    {
        "code": "N18.4",
        "short_description": "ERC estadio 4",
        "full_description": "Enfermedad renal crónica, estadio 4 (TFG severamente disminuida 15-29)",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": True,
        "parent_code": "N18",
        "is_common": True,
        "notes": "TFG 15-29 ml/min/1.73m²"
    },
    {
        "code": "N18.5",
        "short_description": "ERC estadio 5",
        "full_description": "Enfermedad renal crónica, estadio 5 (falla renal <15)",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": True,
        "parent_code": "N18",
        "is_common": True,
        "notes": "TFG <15 ml/min/1.73m² - Requiere diálisis o trasplante"
    },
    {
        "code": "N18.9",
        "short_description": "ERC no especificada",
        "full_description": "Enfermedad renal crónica, no especificada",
        "chapter": "XIV - Enfermedades del sistema genitourinario",
        "chapter_code": "XIV",
        "category": "Insuficiencia renal",
        "is_subcategory": True,
        "parent_code": "N18",
        "is_common": True,
        "notes": None
    },

    # ========================================================================
    # CAPÍTULO XV: EMBARAZO, PARTO Y PUERPERIO (O00-O99)
    # ========================================================================
    {
        "code": "O10",
        "short_description": "Hipertensión preexistente que complica el embarazo",
        "full_description": "Hipertensión preexistente que complica el embarazo, el parto y el puerperio",
        "chapter": "XV - Embarazo, parto y puerperio",
        "chapter_code": "XV",
        "category": "Trastornos hipertensivos del embarazo",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "HTA crónica en embarazo"
    },
    {
        "code": "O13",
        "short_description": "Hipertensión gestacional",
        "full_description": "Hipertensión gestacional [inducida por el embarazo] sin proteinuria significativa",
        "chapter": "XV - Embarazo, parto y puerperio",
        "chapter_code": "XV",
        "category": "Trastornos hipertensivos del embarazo",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "HTA que aparece en el embarazo"
    },
    {
        "code": "O14",
        "short_description": "Preeclampsia",
        "full_description": "Hipertensión gestacional con proteinuria significativa (preeclampsia)",
        "chapter": "XV - Embarazo, parto y puerperio",
        "chapter_code": "XV",
        "category": "Trastornos hipertensivos del embarazo",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere vigilancia estrecha"
    },
    {
        "code": "O15",
        "short_description": "Eclampsia",
        "full_description": "Eclampsia (preeclampsia con convulsiones)",
        "chapter": "XV - Embarazo, parto y puerperio",
        "chapter_code": "XV",
        "category": "Trastornos hipertensivos del embarazo",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": False,
        "notes": "Urgencia obstétrica"
    },
    {
        "code": "O24",
        "short_description": "Diabetes mellitus en el embarazo",
        "full_description": "Diabetes mellitus en el embarazo (diabetes gestacional)",
        "chapter": "XV - Embarazo, parto y puerperio",
        "chapter_code": "XV",
        "category": "Diabetes en el embarazo",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Requiere control glicémico estricto"
    },
    {
        "code": "O24.4",
        "short_description": "Diabetes mellitus gestacional",
        "full_description": "Diabetes mellitus gestacional (diabetes que aparece en el embarazo)",
        "chapter": "XV - Embarazo, parto y puerperio",
        "chapter_code": "XV",
        "category": "Diabetes en el embarazo",
        "is_subcategory": True,
        "parent_code": "O24",
        "is_common": True,
        "notes": "Tamización con PTOG"
    },

    # ========================================================================
    # CAPÍTULO XXI: FACTORES QUE INFLUYEN EN EL ESTADO DE SALUD (Z00-Z99)
    # ========================================================================
    {
        "code": "Z00",
        "short_description": "Examen general",
        "full_description": "Examen general e investigación de personas sin quejas o sin diagnóstico informado",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Exámenes y controles de salud",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Control de salud preventivo"
    },
    {
        "code": "Z00.0",
        "short_description": "Examen médico general",
        "full_description": "Examen médico general",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Exámenes y controles de salud",
        "is_subcategory": True,
        "parent_code": "Z00",
        "is_common": True,
        "notes": "Chequeo médico"
    },
    {
        "code": "Z13",
        "short_description": "Examen especial de pesquisa",
        "full_description": "Examen especial de pesquisa para enfermedades y trastornos (tamización)",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Exámenes y controles de salud",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Tamización de enfermedades"
    },
    {
        "code": "Z34",
        "short_description": "Supervisión de embarazo normal",
        "full_description": "Supervisión de embarazo normal (control prenatal)",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Atención materna",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Código para controles prenatales"
    },
    {
        "code": "Z34.0",
        "short_description": "Supervisión de primer embarazo normal",
        "full_description": "Supervisión de primer embarazo normal (control prenatal primigestante)",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Atención materna",
        "is_subcategory": True,
        "parent_code": "Z34",
        "is_common": True,
        "notes": None
    },
    {
        "code": "Z71",
        "short_description": "Asesoramiento",
        "full_description": "Personas en contacto con los servicios de salud por otras razones de asesoramiento",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Consejería y asesoramiento",
        "is_subcategory": False,
        "parent_code": None,
        "is_common": True,
        "notes": "Educación en salud"
    },
    {
        "code": "Z71.3",
        "short_description": "Asesoramiento y supervisión dietética",
        "full_description": "Asesoramiento y supervisión dietética (consejería nutricional)",
        "chapter": "XXI - Factores que influyen en el estado de salud",
        "chapter_code": "XXI",
        "category": "Consejería y asesoramiento",
        "is_subcategory": True,
        "parent_code": "Z71",
        "is_common": True,
        "notes": "Educación nutricional"
    },
]


def get_cie10_by_chapter():
    """
    Agrupa los códigos CIE-10 por capítulo para facilitar análisis
    """
    chapters = {}
    for item in CIE10_CATALOG_DATA:
        chapter_code = item['chapter_code']
        if chapter_code not in chapters:
            chapters[chapter_code] = {
                'name': item['chapter'],
                'codes': []
            }
        chapters[chapter_code]['codes'].append(item)
    return chapters


def get_common_codes():
    """
    Retorna solo los códigos marcados como comunes (is_common=True)
    """
    return [item for item in CIE10_CATALOG_DATA if item['is_common']]


def get_codes_count():
    """
    Estadísticas del catálogo
    """
    total = len(CIE10_CATALOG_DATA)
    common = len(get_common_codes())
    by_chapter = get_cie10_by_chapter()

    return {
        'total_codes': total,
        'common_codes': common,
        'chapters_count': len(by_chapter),
        'chapters': {k: len(v['codes']) for k, v in by_chapter.items()}
    }


if __name__ == '__main__':
    # Test básico
    stats = get_codes_count()
    print(f"Catalogo CIE-10 para SAGE3280")
    print(f"   Total de codigos: {stats['total_codes']}")
    print(f"   Codigos comunes: {stats['common_codes']}")
    print(f"   Capitulos: {stats['chapters_count']}")
    print(f"\nCodigos por capitulo:")
    for chapter, count in stats['chapters'].items():
        print(f"   - Capitulo {chapter}: {count} codigos")
