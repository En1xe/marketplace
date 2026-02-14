from random import randint
from datetime import datetime, timedelta
from typing import Any

from core.constants import VERIFICATION_CODE_EXPIRE_MINUTES


def generate_6_digits_code() -> str:
    """Generates random six-digit verification code"""
    
    return ''.join([str(randint(0, 9)) for _ in range(6)])


def get_verification_code_expire_time() -> datetime:
    """Returns the expiration time of the verification code"""
    
    return datetime.now() + timedelta(minutes=VERIFICATION_CODE_EXPIRE_MINUTES)


def create_test_verification_code_data(
    user_id: int | None = None,
    operation_type: str = 'verification',
    field_value: str | None = None
) -> dict[str, Any]:
    return {
        'user_id': user_id,
        'operation_type': operation_type,
        'field_value': field_value,
    }
    