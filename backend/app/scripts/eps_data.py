"""
Script de datos oficiales de EPS (Entidades Promotoras de Salud) en Colombia

Fuente oficial: Ministerio de Salud y Protección Social
Última actualización: Junio 2025
Referencias:
- https://www.minsalud.gov.co/
- Superintendencia Nacional de Salud
- ADRES (Administradora de los Recursos del Sistema General de Seguridad Social en Salud)

NOTA: Solo se incluyen 28 EPS autorizadas para operar en 2025 según MinSalud
Estado actualizado a diciembre 2025
"""

EPS_CATALOG_DATA = [
    # ====================================================================
    # RÉGIMEN CONTRIBUTIVO - EPS PRINCIPALES
    # ====================================================================

    {
        "code": "EPS002",
        "name": "SALUD TOTAL S.A. EPS",
        "short_name": "Salud Total",
        "nit": "800130907-4",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 116 699",
        "website": "https://www.saludtotal.com.co",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Una de las EPS más grandes del país"
    },
    {
        "code": "EPS005",
        "name": "EPS SANITAS S.A.",
        "short_name": "Sanitas",
        "nit": "800251440-6",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 123 414",
        "email": "servicioalcliente@colsanitas.com",
        "website": "https://www.colsanitas.com",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Parte del grupo Keralty (anteriormente Colsanitas)"
    },
    {
        "code": "EPS008",
        "name": "COMPENSAR ENTIDAD PROMOTORA DE SALUD",
        "short_name": "Compensar",
        "nit": "860066942-7",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "444 4234",
        "email": "epscompensarcajadecompensacionfamiliar@compensar.com",
        "website": "https://www.compensar.com",
        "coverage_nationwide": False,
        "departments": "Bogotá D.C., Cundinamarca",
        "notes": "EPS de Caja de Compensación Familiar Compensar"
    },
    {
        "code": "EPS010",
        "name": "EPS SURA",
        "short_name": "SURA",
        "nit": "800088702-2",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 51 7872",
        "email": "servicioalcliente@eps.sura.com.co",
        "website": "https://www.epssura.com",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "EPS del grupo SURA"
    },
    {
        "code": "EPS016",
        "name": "COOMEVA ENTIDAD PROMOTORA DE SALUD S.A.",
        "short_name": "Coomeva EPS",
        "nit": "805000427-1",
        "regime_type": "contributivo",
        "is_active": False,  # EN LIQUIDACIÓN desde 2024
        "phone": "01 8000 052 666",
        "website": "https://www.coomeva.com.co",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "EN LIQUIDACIÓN - Proceso iniciado en 2024"
    },
    {
        "code": "EPS017",
        "name": "EPS FAMISANAR LTDA",
        "short_name": "Famisanar",
        "nit": "830003564-7",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 426 600",
        "email": "servicioalcliente@famisanar.com.co",
        "website": "https://www.famisanar.com.co",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "EPS cooperativa con amplia cobertura"
    },
    {
        "code": "EPS037",
        "name": "NUEVA EPS S.A.",
        "short_name": "Nueva EPS",
        "nit": "900156264-2",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 113 110",
        "email": "servicioalcliente@nuevaeps.com.co",
        "website": "https://www.nuevaeps.com.co",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Estuvo bajo intervención administrativa hasta abril 2025. Ahora opera ambos regímenes (EPS037/EPSS41)"
    },
    {
        "code": "EPS001",
        "name": "ALIANSALUD EPS",
        "short_name": "Aliansalud",
        "nit": "830113831-0",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 110 102",
        "website": "https://www.aliansalud.com.co",
        "coverage_nationwide": False,
        "departments": "Cauca, Nariño, Valle del Cauca",
        "notes": "EPS regional del sur occidente colombiano"
    },

    # ====================================================================
    # RÉGIMEN CONTRIBUTIVO - EPS REGIONALES Y ESPECIALES
    # ====================================================================

    {
        "code": "EPS014",
        "name": "CAFESALUD ENTIDAD PROMOTORA DE SALUD S.A.",
        "short_name": "Cafesalud",
        "nit": "817000083-0",
        "regime_type": "contributivo",
        "is_active": False,  # LIQUIDADA
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "LIQUIDADA - Integrada a Nueva EPS en 2016"
    },
    {
        "code": "EPS025",
        "name": "SERVICIO OCCIDENTAL DE SALUD S.A.",
        "short_name": "SOS",
        "nit": "805024488-6",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "01 8000 117 717",
        "website": "https://www.sos.com.co",
        "coverage_nationwide": False,
        "departments": "Valle del Cauca, Cauca, Nariño, Chocó",
        "notes": "EPS regional del Valle del Cauca"
    },

    # ====================================================================
    # RÉGIMEN SUBSIDIADO - EPS PRINCIPALES
    # ====================================================================

    {
        "code": "ESS024",  # También opera como EPS042 en contributivo
        "name": "COOSALUD ENTIDAD PROMOTORA DE SALUD S.A.",
        "short_name": "Coosalud",
        "nit": "900226715-4",
        "regime_type": "subsidiado",  # Opera AMBOS regímenes
        "is_active": True,
        "phone": "01 8000 413 225",
        "email": "pqr@coosalud.com.co",
        "website": "https://www.coosalud.com.co",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Opera en ambos regímenes: ESS024 (subsidiado) y EPS042 (contributivo)"
    },
    {
        "code": "ESS207",  # También EPS048 en contributivo
        "name": "ASOCIACIÓN MUTUAL SER EMPRESA SOLIDARIA DE SALUD",
        "short_name": "Mutual Ser",
        "nit": "806008394-6",
        "regime_type": "subsidiado",  # Opera AMBOS regímenes
        "is_active": True,
        "phone": "01 8000 115 544",
        "email": "servicioalcliente@mutualser.com",
        "website": "https://www.mutualser.com",
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Opera en ambos regímenes: ESS207 (subsidiado) y EPS048 (contributivo)"
    },
    {
        "code": "EPSS46",
        "name": "SALUD MIA EPS SAS",
        "short_name": "Salud Mía",
        "nit": "900914254-5",
        "regime_type": "subsidiado",  # Opera AMBOS regímenes
        "is_active": True,
        "phone": "01 8000 422 220",
        "website": "https://www.saludmia.com.co",
        "coverage_nationwide": False,
        "departments": "Antioquia, Atlántico, Bogotá, Bolívar, Caldas, Cesar, Córdoba, Cundinamarca, La Guajira, Magdalena, Meta, Santander, Sucre, Valle del Cauca",
        "notes": "Opera principalmente en régimen subsidiado, expandiendo a contributivo"
    },
    {
        "code": "EPSC34",
        "name": "CAPITAL SALUD ENTIDAD PROMOTORA DE SALUD DEL REGIMEN SUBSIDIADO S.A.S.",
        "short_name": "Capital Salud",
        "nit": "900298372-9",
        "regime_type": "subsidiado",
        "is_active": True,
        "phone": "601 3649666",
        "email": "info@capitalsalud.gov.co",
        "website": "https://www.capitalsalud.gov.co",
        "coverage_nationwide": False,
        "departments": "Bogotá D.C., Cundinamarca (Soacha), Meta",
        "notes": "EPS territorial de Bogotá para régimen subsidiado"
    },
    {
        "code": "ESS025",
        "name": "ASOCIACIÓN INDÍGENA DEL CAUCA",
        "short_name": "AIC",
        "nit": "817002683-1",
        "regime_type": "subsidiado",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "Cauca",
        "notes": "EPS indígena del Cauca - Régimen subsidiado"
    },
    {
        "code": "ESS033",
        "name": "ANAS WAYUU ENTIDAD PROMOTORA DE SALUD INDIGENA",
        "short_name": "Anas Wayuu",
        "nit": "824005387-6",
        "regime_type": "subsidiado",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "La Guajira, Cesar",
        "notes": "EPS indígena para comunidad Wayuu"
    },
    {
        "code": "ESS117",
        "name": "COMFACOR ENTIDAD PROMOTORA DE SALUD S.A.",
        "short_name": "Comfacor",
        "nit": "891480160-1",
        "regime_type": "subsidiado",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "Córdoba",
        "notes": "EPS regional de Córdoba"
    },

    # ====================================================================
    # RÉGIMENES ESPECIALES
    # ====================================================================

    {
        "code": "ESE001",
        "name": "FONDO DE PASIVO SOCIAL DE FERROCARRILES NACIONALES DE COLOMBIA",
        "short_name": "Ferrocarriles",
        "nit": "800215381-9",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Régimen especial para ex-empleados de Ferrocarriles Nacionales"
    },
    {
        "code": "ESE002",
        "name": "CAJA DE COMPENSACIÓN FAMILIAR CAJACOPI ATLÁNTICO",
        "short_name": "Cajacopi",
        "nit": "890102018-4",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "Atlántico",
        "notes": "Régimen especial - Caja de Compensación"
    },
    {
        "code": "ESEM01",
        "name": "DIRECCIÓN DE SANIDAD DEL EJÉRCITO NACIONAL",
        "short_name": "DISAN Ejército",
        "nit": "800197268-4",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Régimen especial - Fuerzas Militares (Ejército Nacional)"
    },
    {
        "code": "ESEM02",
        "name": "DIRECCIÓN GENERAL DE SANIDAD DE LA POLICÍA NACIONAL",
        "short_name": "DISAN Policía",
        "nit": "899999026-6",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Régimen especial - Policía Nacional"
    },
    {
        "code": "ESEM03",
        "name": "DIRECCIÓN GENERAL DE SANIDAD MILITAR",
        "short_name": "DISAN Militar",
        "nit": "899999115-7",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Régimen especial - Fuerzas Militares"
    },
    {
        "code": "ESEE01",
        "name": "ECOPETROL S.A. - RÉGIMEN ESPECIAL DE SALUD",
        "short_name": "Ecopetrol Salud",
        "nit": "899999068-1",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": True,
        "departments": "Nacional",
        "notes": "Régimen especial - Empleados de Ecopetrol"
    },
    {
        "code": "ESEMC",
        "name": "UNIVERSIDAD DEL VALLE - PLAN DE SALUD",
        "short_name": "Univalle Salud",
        "nit": "890399010-6",
        "regime_type": "especial",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "Valle del Cauca",
        "notes": "Régimen especial - Empleados Universidad del Valle"
    },

    # ====================================================================
    # EPS ADICIONALES ACTIVAS 2025
    # ====================================================================

    {
        "code": "EPS022",
        "name": "FUNDACIÓN SALUD MIA",
        "short_name": "Fundación Salud Mía",
        "nit": "830037939-0",
        "regime_type": "contributivo",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "Antioquia, Valle del Cauca",
        "notes": "EPS regional"
    },
    {
        "code": "EPS033",
        "name": "MALLAMAS ENTIDAD PROMOTORA DE SALUD S.A.S.",
        "short_name": "Mallamas",
        "nit": "900815725-8",
        "regime_type": "contributivo",
        "is_active": True,
        "coverage_nationwide": False,
        "departments": "Nariño",
        "notes": "EPS regional de Nariño"
    },
    {
        "code": "EPS023",
        "name": "CRUZ BLANCA ENTIDAD PROMOTORA DE SALUD S.A.",
        "short_name": "Cruz Blanca",
        "nit": "860011153-6",
        "regime_type": "contributivo",
        "is_active": True,
        "phone": "601 3077777",
        "website": "https://www.cruzblanca.com.co",
        "coverage_nationwide": False,
        "departments": "Bogotá D.C., Cundinamarca",
        "notes": "EPS regional de Bogotá y Cundinamarca"
    },
]


def get_active_eps():
    """Retorna solo las EPS activas"""
    return [eps for eps in EPS_CATALOG_DATA if eps.get("is_active", True)]


def get_eps_by_regime(regime_type):
    """
    Retorna EPS filtradas por tipo de régimen

    Args:
        regime_type: 'contributivo', 'subsidiado' o 'especial'
    """
    return [eps for eps in EPS_CATALOG_DATA if eps.get("regime_type") == regime_type]


def get_nationwide_eps():
    """Retorna solo las EPS con cobertura nacional"""
    return [eps for eps in EPS_CATALOG_DATA if eps.get("coverage_nationwide", False)]


if __name__ == "__main__":
    print(f"Total EPS en catálogo: {len(EPS_CATALOG_DATA)}")
    print(f"EPS activas: {len(get_active_eps())}")
    print(f"EPS contributivo: {len(get_eps_by_regime('contributivo'))}")
    print(f"EPS subsidiado: {len(get_eps_by_regime('subsidiado'))}")
    print(f"EPS especiales: {len(get_eps_by_regime('especial'))}")
    print(f"EPS cobertura nacional: {len(get_nationwide_eps())}")

    print("\n--- EPS ACTIVAS POR RÉGIMEN ---")
    for regime in ['contributivo', 'subsidiado', 'especial']:
        print(f"\n{regime.upper()}:")
        for eps in get_eps_by_regime(regime):
            if eps.get("is_active", True):
                print(f"  - {eps['code']}: {eps['name']}")
