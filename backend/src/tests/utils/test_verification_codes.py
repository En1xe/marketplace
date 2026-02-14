from datetime import datetime, timedelta

from utils.verification_codes import *
from core.constants import VERIFICATION_CODE_EXPIRE_MINUTES


class TestUtilsVerificationCodes:
    
    def test_generate_6_digits_code(self):
        code_1 = generate_6_digits_code()
        code_2 = generate_6_digits_code()
        
        assert len(code_1) == 6
        assert code_1 != code_2
        
    def test_get_verification_code_expire_time(self):
        expire_time_1 = get_verification_code_expire_time()
        expire_time_2 = datetime.now() + timedelta(
            minutes=VERIFICATION_CODE_EXPIRE_MINUTES
        )
        
        assert expire_time_2.timestamp() - expire_time_1.timestamp() < 1