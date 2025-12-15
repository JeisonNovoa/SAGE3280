import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, date
import re
from app.services.excel_validator import ExcelValidator


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

    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.column_map: Dict[str, str] = {}
        self.validation_result: Optional[Dict] = None

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

        try:
            if isinstance(date_value, (datetime, pd.Timestamp)):
                return date_value.date()
            elif isinstance(date_value, str):
                # Try common date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
                    try:
                        return datetime.strptime(date_value, fmt).date()
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
                    'eps': str(self._get_column_value(row, 'eps', '')).strip() or None,
                    'tipo_convenio': str(self._get_column_value(row, 'tipo_convenio', '')).strip() or None,
                    'diagnoses': str(diagnoses_value) if not pd.isna(diagnoses_value) else None,
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
        }
