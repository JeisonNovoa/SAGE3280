import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, date
import re
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.excel_validator import ExcelValidator
from app.models.eps import Eps
from app.models.cie10 import Cie10


class ExcelProcessor:
    """
    Service to process Excel files and extract patient information.
    Handles different Excel formats and column names.
    """

    # Possible column name mappings (flexible to handle different formats)
    # NOTE: All variants should be normalized (no accents, lowercase, underscores)
    COLUMN_MAPPINGS = {
        'document': ['documento', 'cedula', 'cc', 'identificacion', 'doc', 'numero_documento'],
        'document_type': ['tipo_de_documento', 'tipo_documento', 'tipo_doc', 'tipodocumento'],
        'first_name': ['nombres', 'nombre', 'primer_nombre', 'name', 'first_name'],
        'last_name': ['apellidos', 'apellido', 'last_name', 'surname'],
        'birth_date': ['fecha_de_nacimiento', 'fecha_nacimiento', 'nacimiento', 'fecha_nac', 'birth_date', 'dob', 'fec_nacimiento', 'fechanacimiento'],
        'sex': ['sexo', 'genero', 'sex', 'gender'],
        'phone': ['telefono', 'celular', 'tel', 'phone', 'movil'],
        'email': ['correo', 'email', 'e-mail', 'mail'],
        'neighborhood': ['barrio___vereda', 'barrio__vereda', 'barrio_vereda', 'barrio', 'vereda'],
        'city': ['municipio', 'ciudad', 'city'],
        'eps': ['eps', 'aseguradora', 'eapb'],
        'tipo_convenio': ['tipo_de_convenio', 'tipo_convenio', 'tipoconvenio', 'convenio'],
        'diagnoses': ['diagnosticos_texto_libre_y_o_codigos_cie-10', 'diagnosticos', 'codigos_cie-10', 'codigos_cie10', 'dx', 'diagnoses', 'patologias'],
        'last_general_control': ['fecha_ultimo_control_general', 'ultimo_control_general', 'ult_control_general', 'fechaultimocontrolgeneral'],
        'last_3280_control': ['fecha_ultimo_control_3280', 'ultimo_control_3280', 'ult_control_3280', 'fechaultimocontrol3280'],
        'last_hta_control': ['fecha_ultimo_control_hta', 'ultimo_control_hta', 'ult_control_hta', 'fechaultimocontrolhta'],
        'last_dm_control': ['fecha_ultimo_control_dm', 'ultimo_control_dm', 'ult_control_dm', 'fechaultimocontroldm'],
    }

    def __init__(self, db: Optional[Session] = None):
        self.df: Optional[pd.DataFrame] = None
        self.column_map: Dict[str, str] = {}
        self.validation_result: Optional[Dict] = None
        self.db = db
        self.eps_normalization_stats = {
            'total': 0,
            'normalized': 0,
            'not_found': 0,
            'empty': 0
        }
        self.cie10_normalization_stats = {
            'total_codes_found': 0,
            'normalized': 0,
            'not_found': 0,
            'patients_with_codes': 0
        }

    def _normalize_column_name(self, col_name: str) -> str:
        """
        Normalize column name: lowercase, no spaces, no accents.
        """
        import unicodedata
        # Remove accents/tildes
        normalized = unicodedata.normalize('NFKD', str(col_name))
        without_accents = ''.join([c for c in normalized if not unicodedata.combining(c)])
        # Lowercase and replace spaces/special chars with underscore
        clean = without_accents.lower().strip().replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
        return clean

    def load_file(self, file_path: str) -> Tuple[bool, str, int]:
        """
        Load Excel or CSV file with validation.
        Returns: (success, message, row_count)
        """
        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(file_path)
            else:
                return False, "Formato de archivo no soportado", 0

            if self.df.empty:
                return False, "El archivo está vacío", 0

            # Clean column names (lowercase, no spaces, no accents)
            self.df.columns = [self._normalize_column_name(col) for col in self.df.columns]

            # VALIDATE SCHEMA BEFORE PROCESSING
            self.validation_result = ExcelValidator.validate_file(self.df)

            if not self.validation_result['valid']:
                error_msg = "Errores de validación:\n" + "\n".join(self.validation_result['errors'])
                return False, error_msg, 0

            # Use validated column mapping
            self.column_map = self.validation_result['column_mapping']

            # Log warnings if any
            if self.validation_result['warnings']:
                warnings_msg = "\n".join(self.validation_result['warnings'])
                print(f"⚠️  ADVERTENCIAS:\n{warnings_msg}")

            return True, "Archivo cargado y validado exitosamente", len(self.df)

        except Exception as e:
            return False, f"Error al cargar archivo: {str(e)}", 0

    def get_validation_report(self) -> Optional[str]:
        """Get human-readable validation report"""
        if self.validation_result:
            return ExcelValidator.generate_validation_report(self.validation_result)
        return None

    def _get_column_value(self, row: pd.Series, field: str, default=None):
        """
        Get value from row using mapped column name.
        """
        if field in self.column_map:
            col_name = self.column_map[field]
            value = row.get(col_name, default)
            # Handle NaN values
            if pd.isna(value):
                return default
            return value
        return default

    def _parse_date(self, date_value) -> Optional[date]:
        """
        Parse date from various formats.
        """
        if pd.isna(date_value):
            return None

        # Handle empty strings
        if isinstance(date_value, str) and date_value.strip() == '':
            return None

        try:
            if isinstance(date_value, (datetime, pd.Timestamp)):
                return date_value.date()
            elif isinstance(date_value, str):
                # Try common date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                    try:
                        return datetime.strptime(date_value.strip(), fmt).date()
                    except ValueError:
                        continue
            return None
        except:
            return None

    def _calculate_age(self, birth_date: Optional[date]) -> Optional[int]:
        """
        Calculate age from birth date.
        """
        if not birth_date:
            return None
        today = date.today()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age

    def _normalize_sex(self, sex_value) -> Optional[str]:
        """
        Normalize sex value to M/F/O.
        """
        if pd.isna(sex_value):
            return None

        sex_str = str(sex_value).upper().strip()

        if sex_str in ['M', 'MASCULINO', 'HOMBRE', 'MALE', '1']:
            return 'M'
        elif sex_str in ['F', 'FEMENINO', 'MUJER', 'FEMALE', '2']:
            return 'F'
        else:
            return 'O'

    def _extract_diagnoses(self, diagnoses_value) -> Tuple[bool, bool, bool]:
        """
        Extract health conditions from diagnoses string.
        Returns: (is_hypertensive, is_diabetic, is_pregnant)
        """
        if pd.isna(diagnoses_value):
            return False, False, False

        diagnoses_str = str(diagnoses_value).upper()

        # Check for hypertension
        is_hypertensive = any(term in diagnoses_str for term in [
            'HIPERTENSION', 'HTA', 'HIPERTENSO', 'PRESION ALTA', 'HIPERTENSIÓN'
        ])

        # Check for diabetes
        is_diabetic = any(term in diagnoses_str for term in [
            'DIABETES', 'DM', 'DIABETICO', 'DIABÉTICO', 'MELLITUS'
        ])

        # Check for pregnancy
        is_pregnant = any(term in diagnoses_str for term in [
            'EMBARAZO', 'GESTANTE', 'PREGNANT', 'EMBARAZADA', 'PRENATAL'
        ])

        return is_hypertensive, is_diabetic, is_pregnant

    def _normalize_eps(self, eps_value) -> Tuple[Optional[str], bool]:
        """
        Normalize EPS value using the official catalog.
        Returns: (normalized_eps_string, was_normalized)

        Format: "CODE - NAME" (e.g., "EPS010 - EPS SURA")
        """
        if pd.isna(eps_value) or not eps_value:
            self.eps_normalization_stats['empty'] += 1
            return None, False

        self.eps_normalization_stats['total'] += 1

        # If no database session, return original value
        if not self.db:
            return str(eps_value).strip(), False

        search_term = str(eps_value).strip()
        search_term_lower = search_term.lower()

        # Try to find EPS in catalog using fuzzy search
        # 1. Try exact code match (case-insensitive)
        eps = self.db.query(Eps).filter(
            func.lower(Eps.code) == search_term_lower,
            Eps.is_active == True
        ).first()

        if eps:
            normalized = f"{eps.code} - {eps.name}"
            self.eps_normalization_stats['normalized'] += 1
            return normalized, True

        # 2. Try by NIT (exact)
        eps = self.db.query(Eps).filter(
            Eps.nit == search_term,
            Eps.is_active == True
        ).first()

        if eps:
            normalized = f"{eps.code} - {eps.name}"
            self.eps_normalization_stats['normalized'] += 1
            return normalized, True

        # 3. Try by short_name (case-insensitive, partial match)
        eps = self.db.query(Eps).filter(
            func.lower(Eps.short_name).like(f"%{search_term_lower}%"),
            Eps.is_active == True
        ).first()

        if eps:
            normalized = f"{eps.code} - {eps.name}"
            self.eps_normalization_stats['normalized'] += 1
            return normalized, True

        # 4. Try by official name (case-insensitive, partial match)
        eps = self.db.query(Eps).filter(
            func.lower(Eps.name).like(f"%{search_term_lower}%"),
            Eps.is_active == True
        ).first()

        if eps:
            normalized = f"{eps.code} - {eps.name}"
            self.eps_normalization_stats['normalized'] += 1
            return normalized, True

        # 5. Try partial code match (e.g., "EPS010" or "010")
        eps = self.db.query(Eps).filter(
            func.lower(Eps.code).like(f"%{search_term_lower}%"),
            Eps.is_active == True
        ).first()

        if eps:
            normalized = f"{eps.code} - {eps.name}"
            self.eps_normalization_stats['normalized'] += 1
            return normalized, True

        # Not found in catalog - return original with warning flag
        self.eps_normalization_stats['not_found'] += 1
        return f"[NO_NORMALIZADA] {search_term}", False

    def _extract_and_normalize_cie10_codes(self, diagnoses_value) -> List[str]:
        """
        Extract and normalize CIE-10 codes from diagnoses text.
        Returns: List of normalized CIE-10 codes in format "CODE - DESCRIPTION"

        Searches for CIE-10 code patterns like:
        - I10, E11, J44 (single letter + 2 digits)
        - E11.9, I11.9 (with decimal subcategory)
        - Also searches for disease keywords to suggest codes
        """
        if pd.isna(diagnoses_value) or not diagnoses_value:
            return []

        if not self.db:
            return []  # No database, can't normalize

        diagnoses_str = str(diagnoses_value).upper()
        normalized_codes = []
        found_codes = set()  # Track to avoid duplicates

        # Regex pattern for CIE-10 codes: Letter(s) + Digits + optional (.Digits)
        # Examples: I10, E11.9, J44, N18.3
        cie10_pattern = r'\b([A-Z]\d{2}(?:\.\d{1,2})?)\b'

        # Find all CIE-10 code patterns in text
        matches = re.findall(cie10_pattern, diagnoses_str)

        for code in matches:
            if code in found_codes:
                continue  # Skip duplicates

            self.cie10_normalization_stats['total_codes_found'] += 1

            # Try to find code in catalog (case-insensitive)
            cie10 = self.db.query(Cie10).filter(
                func.upper(Cie10.code) == code.upper()
            ).first()

            if cie10:
                normalized = f"{cie10.code} - {cie10.short_description}"
                normalized_codes.append(normalized)
                found_codes.add(code)
                self.cie10_normalization_stats['normalized'] += 1
            else:
                # Code not found in catalog
                normalized_codes.append(f"[NO_NORMALIZADO] {code}")
                found_codes.add(code)
                self.cie10_normalization_stats['not_found'] += 1

        # If no codes found with regex, try keyword search for common conditions
        if not normalized_codes:
            # Search for keywords that might match CIE-10 descriptions
            keywords = []

            # Extract meaningful words (3+ chars) from diagnoses
            words = re.findall(r'\b[A-ZÁÉÍÓÚÑ]{3,}\b', diagnoses_str)

            # Filter to get most relevant keywords (skip common words)
            common_words = {'CON', 'SIN', 'PARA', 'LOS', 'LAS', 'DEL', 'UNA', 'POR', 'QUE'}
            keywords = [w for w in words if w not in common_words][:3]  # Max 3 keywords

            for keyword in keywords:
                # Search in CIE-10 catalog by description
                cie10_matches = self.db.query(Cie10).filter(
                    func.upper(Cie10.short_description).like(f"%{keyword}%")
                ).filter(
                    Cie10.is_common == True  # Only search common codes
                ).limit(1).all()  # Limit to 1 to avoid too many matches

                for cie10 in cie10_matches:
                    if cie10.code not in found_codes:
                        normalized = f"{cie10.code} - {cie10.short_description} [SUGERIDO]"
                        normalized_codes.append(normalized)
                        found_codes.add(cie10.code)
                        self.cie10_normalization_stats['total_codes_found'] += 1
                        self.cie10_normalization_stats['normalized'] += 1

        if normalized_codes:
            self.cie10_normalization_stats['patients_with_codes'] += 1

        return normalized_codes

    def extract_patients(self) -> List[Dict]:
        """
        Extract patient data from DataFrame.
        Returns list of patient dictionaries ready for database insertion.
        """
        if self.df is None:
            return []

        patients = []

        for idx, row in self.df.iterrows():
            try:
                # Extract basic info
                document = str(self._get_column_value(row, 'document', '')).strip()
                if not document or document == 'nan':
                    continue  # Skip rows without document

                document_type = str(self._get_column_value(row, 'document_type', '')).strip() or None

                first_name = str(self._get_column_value(row, 'first_name', '')).strip()
                last_name = str(self._get_column_value(row, 'last_name', '')).strip()

                if not first_name and not last_name:
                    continue  # Skip if no name

                # Parse birth date and calculate age
                birth_date = self._parse_date(self._get_column_value(row, 'birth_date'))
                age = self._calculate_age(birth_date) if birth_date else None

                # Normalize sex
                sex = self._normalize_sex(self._get_column_value(row, 'sex'))

                # Extract diagnoses
                diagnoses_value = self._get_column_value(row, 'diagnoses')
                is_hypertensive, is_diabetic, is_pregnant = self._extract_diagnoses(diagnoses_value)

                # Extract and normalize CIE-10 codes
                cie10_codes = self._extract_and_normalize_cie10_codes(diagnoses_value)

                # Parse control dates
                last_general_control = self._parse_date(self._get_column_value(row, 'last_general_control'))
                last_3280_control = self._parse_date(self._get_column_value(row, 'last_3280_control'))
                last_hta_control = self._parse_date(self._get_column_value(row, 'last_hta_control'))
                last_dm_control = self._parse_date(self._get_column_value(row, 'last_dm_control'))

                # Build patient dict
                patient_data = {
                    'document_number': document,
                    'document_type': document_type,
                    'first_name': first_name,
                    'last_name': last_name,
                    'full_name': f"{first_name} {last_name}".strip(),
                    'birth_date': birth_date,
                    'age': age,
                    'sex': sex,
                    'phone': str(self._get_column_value(row, 'phone', '')).strip() or None,
                    'email': str(self._get_column_value(row, 'email', '')).strip() or None,
                    'address': str(self._get_column_value(row, 'address', '')).strip() or None,
                    'neighborhood': str(self._get_column_value(row, 'neighborhood', '')).strip() or None,
                    'city': str(self._get_column_value(row, 'city', '')).strip() or None,
                    'eps': self._normalize_eps(self._get_column_value(row, 'eps'))[0],
                    'tipo_convenio': str(self._get_column_value(row, 'tipo_convenio', '')).strip() or None,
                    'diagnoses': str(diagnoses_value) if not pd.isna(diagnoses_value) else None,
                    'cie10_codes': cie10_codes,  # Normalized CIE-10 codes
                    'cie10_codes_count': len(cie10_codes),  # Number of codes found
                    'is_hypertensive': is_hypertensive,
                    'is_diabetic': is_diabetic,
                    'is_pregnant': is_pregnant,
                    'last_general_control_date': last_general_control,
                    'last_3280_control_date': last_3280_control,
                    'last_hta_control_date': last_hta_control,
                    'last_dm_control_date': last_dm_control,
                }

                patients.append(patient_data)

            except Exception as e:
                # Log error but continue processing
                print(f"Error processing row {idx}: {str(e)}")
                continue

        return patients

    def get_summary(self) -> Dict:
        """
        Get summary statistics of the loaded data.
        """
        if self.df is None:
            return {}

        return {
            'total_rows': len(self.df),
            'columns_found': list(self.column_map.keys()),
            'columns_missing': [k for k in self.COLUMN_MAPPINGS.keys() if k not in self.column_map],
            'eps_normalization': self.eps_normalization_stats,
            'cie10_normalization': self.cie10_normalization_stats,
        }
