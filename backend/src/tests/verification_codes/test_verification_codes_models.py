import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories.verification_codes import create_verification_code_factory
from core.constants import VERIFICATION_CODE_EXPIRE_MINUTES


class TestVerificationCodesModel:
    
    @pytest.mark.asyncio
    async def test_nullable_fields(
        self,
        db_session: AsyncSession  
    ):
        verification_code = await create_verification_code_factory(
            db_session,
        )
        
        assert verification_code.user_id == None
        assert verification_code.operation_type == 'verification'
        assert verification_code.field_value == None
        
    @pytest.mark.asyncio
    async def test_default_fields(
        self,
        db_session: AsyncSession  
    ):
        verification_code = await create_verification_code_factory(
            db_session,
        )
        
        assert isinstance(verification_code.code, str)
        assert len(verification_code.code) == 6
        assert verification_code.code.isdigit()
        
        expire_at = datetime.now() + timedelta(minutes=VERIFICATION_CODE_EXPIRE_MINUTES)
        
        assert isinstance(verification_code.expire_at, datetime)
        assert expire_at.timestamp() - verification_code.expire_at.timestamp() < 2
        