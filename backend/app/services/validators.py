from typing import Tuple


class DocumentValidator:
    """
    Validators for Colombian identity documents.

    Implements official algorithms for document verification.
    """

    @staticmethod
    def validate_cedula_digito_verificador(cedula: str) -> Tuple[bool, str]:
        """
        Validate Colombian cédula with check digit (dígito verificador).

        Colombian cédulas don't have an official check digit algorithm,
        but we can validate format and basic rules.

        Args:
            cedula: Document number as string

        Returns:
            Tuple of (is_valid, message)
        """
        # Remove spaces and dots
        cedula = cedula.replace(" ", "").replace(".", "").replace(",", "")

        # Basic format validation
        if not cedula.isdigit():
            return False, "La cédula debe contener solo números"

        # Length validation (Colombian cédulas are typically 6-10 digits)
        if len(cedula) < 6 or len(cedula) > 10:
            return False, "La cédula debe tener entre 6 y 10 dígitos"

        # Cannot start with 0 (except for very old cédulas)
        if len(cedula) > 6 and cedula[0] == '0':
            return False, "La cédula no debe comenzar con 0"

        return True, "Cédula válida"

    @staticmethod
    def validate_nit(nit: str) -> Tuple[bool, str]:
        """
        Validate Colombian NIT (Número de Identificación Tributaria) with check digit.

        Uses official DIAN algorithm for NIT validation.

        Args:
            nit: NIT number with or without check digit (format: "123456789" or "123456789-0")

        Returns:
            Tuple of (is_valid, message)
        """
        # Remove spaces, dots, and hyphens
        nit_clean = nit.replace(" ", "").replace(".", "").replace("-", "")

        if not nit_clean.isdigit():
            return False, "El NIT debe contener solo números"

        if len(nit_clean) < 9 or len(nit_clean) > 10:
            return False, "El NIT debe tener 9 o 10 dígitos"

        # Separate number and check digit
        if len(nit_clean) == 10:
            nit_number = nit_clean[:9]
            check_digit = int(nit_clean[9])
        else:
            nit_number = nit_clean
            check_digit = None  # Will calculate expected

        # DIAN Algorithm for NIT check digit
        # Multiply each digit by its corresponding weight
        weights = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]

        total = 0
        for i, digit in enumerate(reversed(nit_number)):
            total += int(digit) * weights[i]

        # Calculate check digit
        remainder = total % 11
        if remainder == 0 or remainder == 1:
            expected_check = remainder
        else:
            expected_check = 11 - remainder

        if check_digit is None:
            return True, f"Dígito verificador esperado: {expected_check}"

        if check_digit == expected_check:
            return True, "NIT válido"
        else:
            return False, f"Dígito verificador incorrecto. Esperado: {expected_check}, Recibido: {check_digit}"

    @staticmethod
    def format_cedula(cedula: str) -> str:
        """
        Format Colombian cédula with dots for readability.

        Args:
            cedula: Raw cédula number

        Returns:
            Formatted cédula (e.g., "1.234.567")
        """
        cedula_clean = cedula.replace(" ", "").replace(".", "").replace(",", "")

        if not cedula_clean.isdigit():
            return cedula

        # Add dots every 3 digits from right to left
        formatted = ""
        for i, digit in enumerate(reversed(cedula_clean)):
            if i > 0 and i % 3 == 0:
                formatted = "." + formatted
            formatted = digit + formatted

        return formatted

    @staticmethod
    def format_nit(nit: str) -> str:
        """
        Format Colombian NIT with check digit.

        Args:
            nit: Raw NIT number

        Returns:
            Formatted NIT (e.g., "123.456.789-0")
        """
        is_valid, message = DocumentValidator.validate_nit(nit)

        nit_clean = nit.replace(" ", "").replace(".", "").replace("-", "")

        if len(nit_clean) == 9:
            # Calculate check digit
            weights = [3, 7, 13, 17, 19, 23, 29, 37, 41]
            total = sum(int(digit) * weight for digit, weight in zip(reversed(nit_clean), weights))
            remainder = total % 11
            check = remainder if remainder <= 1 else 11 - remainder
            nit_clean += str(check)

        if len(nit_clean) != 10:
            return nit

        # Format: XXX.XXX.XXX-X
        formatted = f"{nit_clean[0:3]}.{nit_clean[3:6]}.{nit_clean[6:9]}-{nit_clean[9]}"
        return formatted


class EpsValidator:
    """
    Validators for EPS-related data.
    """

    @staticmethod
    def validate_eps_code(code: str) -> Tuple[bool, str]:
        """
        Validate EPS code format.

        EPS codes are typically alphanumeric codes assigned by Supersalud.

        Args:
            code: EPS code

        Returns:
            Tuple of (is_valid, message)
        """
        if not code:
            return False, "Código de EPS requerido"

        # Basic format validation
        if len(code) < 3 or len(code) > 20:
            return False, "Código de EPS debe tener entre 3 y 20 caracteres"

        return True, "Código válido"


class Cie10Validator:
    """
    Validators for CIE-10 codes.
    """

    @staticmethod
    def validate_cie10_code(code: str) -> Tuple[bool, str]:
        """
        Validate CIE-10 code format.

        CIE-10 codes follow pattern: Letter + Numbers + optional decimal
        Examples: I10, E11.9, C50.1

        Args:
            code: CIE-10 code

        Returns:
            Tuple of (is_valid, message)
        """
        if not code:
            return False, "Código CIE-10 requerido"

        code = code.upper().strip()

        # Must start with a letter (A-Z, except U which is reserved)
        if not code[0].isalpha() or code[0] == 'U':
            return False, "Código CIE-10 debe comenzar con una letra (A-Z, excepto U)"

        # Must have at least 3 characters (e.g., I10)
        if len(code) < 3:
            return False, "Código CIE-10 debe tener al menos 3 caracteres"

        # After the first letter, must be digits or decimal point
        remaining = code[1:]

        # Split by decimal point
        parts = remaining.split('.')

        if len(parts) > 2:
            return False, "Código CIE-10 solo puede tener un punto decimal"

        # First part (before decimal) must be 2 digits
        if not parts[0].isdigit() or len(parts[0]) != 2:
            return False, "Código CIE-10 debe tener formato: Letra + 2 dígitos (ej: I10, E11)"

        # Second part (after decimal) if exists, must be 1-2 digits
        if len(parts) == 2:
            if not parts[1].isdigit() or len(parts[1]) < 1 or len(parts[1]) > 2:
                return False, "Subcategoría CIE-10 debe ser 1-2 dígitos"

        return True, "Código CIE-10 válido"


class CupsValidator:
    """
    Validators for CUPS codes.
    """

    @staticmethod
    def validate_cups_code(code: str) -> Tuple[bool, str]:
        """
        Validate CUPS code format.

        Colombian CUPS codes are typically 6-digit numeric codes.

        Args:
            code: CUPS code

        Returns:
            Tuple of (is_valid, message)
        """
        if not code:
            return False, "Código CUPS requerido"

        code = code.strip()

        # CUPS codes are typically 6 digits
        if not code.isdigit():
            return False, "Código CUPS debe ser numérico"

        if len(code) != 6:
            return False, "Código CUPS debe tener 6 dígitos"

        return True, "Código CUPS válido"
