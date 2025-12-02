"""
Excel Schema Validator for SAGE3280
Validates Excel files before processing to ensure data quality
"""
from typing import Dict, List, Tuple, Optional
import pandas as pd
from datetime import datetime
import re


class ExcelValidator:
    """Validates Excel schema and data quality before processing"""

    # Required columns (at least one variant must exist)
    REQUIRED_COLUMNS = {
        'document': ['documento', 'cedula', 'cc', 'identificacion', 'doc', 'num_documento'],
        'full_name': ['nombre/apellido', 'nombre_apellido', 'nombre_completo', 'full_name', 'paciente'],
        'first_name': ['nombre', 'nombres', 'primer_nombre', 'name'],
        'last_name': ['apellido', 'apellidos', 'primer_apellido', 'lastname'],
        'age': ['edad', 'age'],
        'birth_date': ['fecha_nacimiento', 'fecha_nac', 'nacimiento', 'fec_nac', 'birthdate', 'fecha_de_nacimiento'],
        'sex': ['sexo', 'genero', 'sex', 'gender'],
    }

    # Optional columns
    OPTIONAL_COLUMNS = {
        'phone': ['telefono', 'teléfono', 'celular', 'tel', 'phone', 'movil'],
        'email': ['email', 'correo', 'mail'],
        'address': ['direccion', 'dirección', 'dir', 'address'],
        'city': ['ciudad', 'municipio', 'city'],
        'eps': ['eps', 'aseguradora', 'seguro'],
        'diagnoses': ['diagnostico', 'diagnosticos', 'diagnósticos', 'dx', 'diagnoses'],
        'last_control': ['ultimo_control', 'último_control', 'ult_control', 'last_control', 'fecha_ultimo_control', 'fecha_último_control'],
    }

    # Valid values
    VALID_SEX_VALUES = ['M', 'F', 'MASCULINO', 'FEMENINO', 'HOMBRE', 'MUJER', 'H', 'O', 'OTRO']

    @classmethod
    def validate_file(cls, df: pd.DataFrame) -> Dict:
        """
        Validates the Excel file schema and data quality

        Returns:
            dict with validation results: {
                'valid': bool,
                'errors': list,
                'warnings': list,
                'stats': dict,
                'column_mapping': dict
            }
        """
        errors = []
        warnings = []
        stats = {}
        column_mapping = {}

        # 1. Check if DataFrame is empty
        if df.empty:
            errors.append("El archivo está vacío")
            return {
                'valid': False,
                'errors': errors,
                'warnings': warnings,
                'stats': stats,
                'column_mapping': column_mapping
            }

        # 2. Normalize column names
        df.columns = df.columns.str.lower().str.strip()

        # 3. Check required columns
        missing_required = []
        for field, variants in cls.REQUIRED_COLUMNS.items():
            found = False
            for variant in variants:
                if variant in df.columns:
                    column_mapping[field] = variant
                    found = True
                    break

            if not found:
                missing_required.append(field)

        # Special handling for name fields: accept either full_name OR (first_name AND last_name)
        has_full_name = 'full_name' not in missing_required
        has_split_names = 'first_name' not in missing_required and 'last_name' not in missing_required

        if not has_full_name and not has_split_names:
            # Neither format is present
            errors.append("Se requiere 'Nombre/Apellido' (combinado) O 'Nombre' y 'Apellido' (separados)")
        else:
            # Remove name fields from missing_required if we have either format
            missing_required = [f for f in missing_required if f not in ['full_name', 'first_name', 'last_name']]

        if missing_required:
            errors.append(f"Faltan columnas requeridas: {', '.join(missing_required)}")
            errors.append(f"Columnas encontradas: {', '.join(df.columns.tolist())}")
            return {
                'valid': False,
                'errors': errors,
                'warnings': warnings,
                'stats': stats,
                'column_mapping': column_mapping
            }

        # 4. Map optional columns
        for field, variants in cls.OPTIONAL_COLUMNS.items():
            for variant in variants:
                if variant in df.columns:
                    column_mapping[field] = variant
                    break

        # 5. Validate data quality
        total_rows = len(df)
        stats['total_rows'] = total_rows

        # Check document numbers
        doc_col = column_mapping.get('document')
        if doc_col:
            null_docs = df[doc_col].isnull().sum()
            if null_docs > 0:
                warnings.append(f"{null_docs} registros sin número de documento")

            # Check for duplicates
            duplicates = df[doc_col].duplicated().sum()
            if duplicates > 0:
                warnings.append(f"{duplicates} documentos duplicados en el archivo")
                stats['duplicates_in_file'] = duplicates

            # Check document format (should be numeric)
            invalid_docs = 0
            for doc in df[doc_col].dropna():
                if not str(doc).replace('.', '').replace(',', '').isdigit():
                    invalid_docs += 1

            if invalid_docs > 0:
                warnings.append(f"{invalid_docs} documentos con formato inválido (no numérico)")

        # Check names
        first_name_col = column_mapping.get('first_name')
        last_name_col = column_mapping.get('last_name')

        if first_name_col:
            null_names = df[first_name_col].isnull().sum()
            if null_names > 0:
                warnings.append(f"{null_names} registros sin nombre")

        if last_name_col:
            null_lastnames = df[last_name_col].isnull().sum()
            if null_lastnames > 0:
                warnings.append(f"{null_lastnames} registros sin apellido")

        # Check age and birth_date
        age_col = column_mapping.get('age')
        birth_col = column_mapping.get('birth_date')

        if age_col:
            null_ages = df[age_col].isnull().sum()
            if null_ages > 0 and not birth_col:
                errors.append(f"{null_ages} registros sin edad ni fecha de nacimiento")

            # Check age range
            valid_ages = df[age_col].dropna()
            if len(valid_ages) > 0:
                invalid_ages = ((valid_ages < 0) | (valid_ages > 120)).sum()
                if invalid_ages > 0:
                    warnings.append(f"{invalid_ages} edades fuera de rango (0-120)")

                stats['age_range'] = {
                    'min': int(valid_ages.min()) if len(valid_ages) > 0 else 0,
                    'max': int(valid_ages.max()) if len(valid_ages) > 0 else 0,
                    'avg': round(valid_ages.mean(), 1) if len(valid_ages) > 0 else 0
                }

        # Check sex
        sex_col = column_mapping.get('sex')
        if sex_col:
            null_sex = df[sex_col].isnull().sum()
            if null_sex > 0:
                warnings.append(f"{null_sex} registros sin sexo especificado")

            # Check valid sex values
            invalid_sex = 0
            for sex in df[sex_col].dropna():
                if str(sex).upper() not in cls.VALID_SEX_VALUES:
                    invalid_sex += 1

            if invalid_sex > 0:
                warnings.append(f"{invalid_sex} valores de sexo inválidos (usar M/F)")

            # Sex distribution
            sex_counts = df[sex_col].value_counts().to_dict()
            stats['sex_distribution'] = sex_counts

        # Check phone numbers
        phone_col = column_mapping.get('phone')
        if phone_col:
            null_phones = df[phone_col].isnull().sum()
            stats['without_phone'] = null_phones
            if null_phones > total_rows * 0.5:
                warnings.append(f"{null_phones} registros sin teléfono (dificulta contacto)")

        # Overall stats
        stats['valid_rows_estimate'] = total_rows - len([e for e in errors if 'registros' in e])
        stats['data_quality_score'] = round((1 - len(warnings) / max(total_rows, 1)) * 100, 1)

        # Determine if valid
        is_valid = len(errors) == 0

        return {
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'stats': stats,
            'column_mapping': column_mapping,
            'preview_data': df.head(5).to_dict('records') if is_valid else None
        }

    @classmethod
    def check_consistency(cls, df: pd.DataFrame, column_mapping: Dict) -> List[str]:
        """
        Check data consistency (age vs birth_date, etc.)

        Returns:
            List of inconsistency warnings
        """
        warnings = []

        age_col = column_mapping.get('age')
        birth_col = column_mapping.get('birth_date')

        if age_col and birth_col:
            # Check age vs birth_date consistency
            inconsistent = 0
            current_year = datetime.now().year

            for idx, row in df.iterrows():
                if pd.notna(row[age_col]) and pd.notna(row[birth_col]):
                    stated_age = int(row[age_col])

                    # Try to parse birth date
                    try:
                        if isinstance(row[birth_col], datetime):
                            birth_year = row[birth_col].year
                        else:
                            birth_year = pd.to_datetime(row[birth_col]).year

                        calculated_age = current_year - birth_year

                        # Allow 1 year tolerance
                        if abs(calculated_age - stated_age) > 1:
                            inconsistent += 1
                    except:
                        pass

            if inconsistent > 0:
                warnings.append(f"{inconsistent} registros con inconsistencia entre edad y fecha de nacimiento")

        return warnings

    @classmethod
    def generate_validation_report(cls, validation_result: Dict) -> str:
        """
        Generate a human-readable validation report
        """
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE VALIDACIÓN DE ARCHIVO EXCEL")
        report.append("=" * 60)
        report.append("")

        if validation_result['valid']:
            report.append("✅ ARCHIVO VÁLIDO - Listo para procesar")
        else:
            report.append("❌ ARCHIVO INVÁLIDO - Se encontraron errores críticos")

        report.append("")

        # Errors
        if validation_result['errors']:
            report.append("🚨 ERRORES CRÍTICOS:")
            for error in validation_result['errors']:
                report.append(f"  - {error}")
            report.append("")

        # Warnings
        if validation_result['warnings']:
            report.append("⚠️  ADVERTENCIAS:")
            for warning in validation_result['warnings']:
                report.append(f"  - {warning}")
            report.append("")

        # Stats
        if validation_result['stats']:
            report.append("📊 ESTADÍSTICAS:")
            stats = validation_result['stats']

            if 'total_rows' in stats:
                report.append(f"  - Total de registros: {stats['total_rows']}")

            if 'duplicates_in_file' in stats:
                report.append(f"  - Duplicados en archivo: {stats['duplicates_in_file']}")

            if 'without_phone' in stats:
                report.append(f"  - Sin teléfono: {stats['without_phone']}")

            if 'age_range' in stats:
                age_range = stats['age_range']
                report.append(f"  - Rango de edad: {age_range['min']}-{age_range['max']} años (promedio: {age_range['avg']})")

            if 'sex_distribution' in stats:
                report.append(f"  - Distribución por sexo: {stats['sex_distribution']}")

            if 'data_quality_score' in stats:
                report.append(f"  - Calidad de datos: {stats['data_quality_score']}%")

            report.append("")

        # Column mapping
        if validation_result['column_mapping']:
            report.append("🗂️  MAPEO DE COLUMNAS:")
            for field, column in validation_result['column_mapping'].items():
                report.append(f"  - {field} → {column}")
            report.append("")

        report.append("=" * 60)

        return "\n".join(report)
