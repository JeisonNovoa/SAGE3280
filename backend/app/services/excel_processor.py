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
    COLUMN_MAPPINGS = {
        'document': ['documento', 'cedula', 'cc', 'identificacion', 'doc', 'numero_documento'],
        'first_name': ['nombre', 'nombres', 'primer_nombre', 'name', 'first_name'],
        'last_name': ['apellido', 'apellidos', 'last_name', 'surname'],
        'birth_date': ['fecha_nacimiento', 'nacimiento', 'fecha_nac', 'birth_date', 'dob', 'fec_nacimiento'],
        'age': ['edad', 'age'],
        'sex': ['sexo', 'genero', 'sex', 'gender'],
        'phone': ['telefono', 'celular', 'tel', 'phone', 'movil'],
        'email': ['correo', 'email', 'e-mail', 'mail'],
        'address': ['direccion', 'address', 'dir'],
        'city': ['ciudad', 'city', 'municipio'],
        'eps': ['eps', 'aseguradora', 'eapb'],
        'diagnoses': ['diagnostico', 'diagnosticos', 'dx', 'diagnoses', 'patologias'],
        'last_control': ['ultimo_control', 'fecha_control', 'last_control', 'fec_control'],
    }

    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.column_map: Dict[str, str] = {}
        self.validation_result: Optional[Dict] = None

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

            # Clean column names (lowercase, no spaces)
            self.df.columns = self.df.columns.str.lower().str.strip().str.replace(' ', '_')

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

                first_name = str(self._get_column_value(row, 'first_name', '')).strip()
                last_name = str(self._get_column_value(row, 'last_name', '')).strip()

                if not first_name and not last_name:
                    continue  # Skip if no name

                # Parse birth date and calculate age
                birth_date = self._parse_date(self._get_column_value(row, 'birth_date'))
                age = self._get_column_value(row, 'age')

                if age and not pd.isna(age):
                    age = int(age)
                elif birth_date:
                    age = self._calculate_age(birth_date)
                else:
                    age = None

                # Normalize sex
                sex = self._normalize_sex(self._get_column_value(row, 'sex'))

                # Extract diagnoses
                diagnoses_value = self._get_column_value(row, 'diagnoses')
                is_hypertensive, is_diabetic, is_pregnant = self._extract_diagnoses(diagnoses_value)

                # Parse last control date
                last_control = self._parse_date(self._get_column_value(row, 'last_control'))

                # Build patient dict
                patient_data = {
                    'document_number': document,
                    'first_name': first_name,
                    'last_name': last_name,
                    'full_name': f"{first_name} {last_name}".strip(),
                    'birth_date': birth_date,
                    'age': age,
                    'sex': sex,
                    'phone': str(self._get_column_value(row, 'phone', '')).strip() or None,
                    'email': str(self._get_column_value(row, 'email', '')).strip() or None,
                    'address': str(self._get_column_value(row, 'address', '')).strip() or None,
                    'city': str(self._get_column_value(row, 'city', '')).strip() or None,
                    'eps': str(self._get_column_value(row, 'eps', '')).strip() or None,
                    'diagnoses': str(diagnoses_value) if not pd.isna(diagnoses_value) else None,
                    'is_hypertensive': is_hypertensive,
                    'is_diabetic': is_diabetic,
                    'is_pregnant': is_pregnant,
                    'last_control_date': last_control,
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
