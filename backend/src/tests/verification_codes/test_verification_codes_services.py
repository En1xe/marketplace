import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from core.factories.verification_codes import create_verification_code_factory
from core.factories.users import create_user_factory
from core.exceptions import (
    NoObjectWasFoundException, 
    ObjectExpiredException,
    IncorrectDataException
)
from models.verification_codes import VerificationCodesModel
from utils.verification_codes import create_test_verification_code_data
from schemas.verification_codes import VerificationCodeCreateSchema
from services.verification_codes import VerificationCodesService
from repositories.verification_codes import VerificationCodesRepository


class TestVerificationCodesService:
    
    service = VerificationCodesService(VerificationCodesRepository())

    @pytest.mark.asyncio
    async def test_get_one_verification_code(
        self,
        db_session: AsyncSession
    ):
        verification_code = await create_verification_code_factory(db_session)
        
        result = await self.service.get_one_verification_code(
            db_session, 
            uuid=verification_code.uuid
        )
        
        assert verification_code.uuid == result.uuid
        
    @pytest.mark.asyncio
    async def test_add_one_verification_code(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        data = create_test_verification_code_data(
            user_id=user.id,
            field_value=''
        )
        
        verification_code = await self.service.add_one_verification_code(
            db_session,
            VerificationCodeCreateSchema.model_validate(data)
        )
        
        assert isinstance(verification_code, VerificationCodesModel)    
        
        
    @pytest.mark.asyncio
    async def test_validate_verification_code(
        self,
        db_session: AsyncSession
    ):
        verification_code = await create_verification_code_factory(db_session)
        
        await self.service.validate_verification_code(
            db_session,
            uuid=verification_code.uuid
        )
        
    @pytest.mark.asyncio
    async def test_validate_verification_code_errors(
        self,
        db_session: AsyncSession,
        mocker
    ):
        verification_code = await create_verification_code_factory(db_session)
        
        mock_datetime = mocker.Mock()
        mock_datetime.now.return_value = datetime.now() + timedelta(minutes=30)
        mocker.patch('services.verification_codes.datetime', mock_datetime)
        
        with pytest.raises(NoObjectWasFoundException):
            await self.service.validate_verification_code(
                db_session,
                uuid=uuid4()
            )
            
        with pytest.raises(ObjectExpiredException):
            await self.service.validate_verification_code(
                    db_session,
                    uuid=verification_code.uuid
                )
            
    @pytest.mark.asyncio
    async def test_confirm_verification_code(
        self,
        db_session: AsyncSession
    ):
        verification_code = await create_verification_code_factory(db_session)
        
        result = await self.service.confirm_verification_code(
            db_session,
            uuid=verification_code.uuid,
            code=verification_code.code
        )
        
        assert isinstance(result, VerificationCodesModel)
        
        with pytest.raises(IncorrectDataException):
            await self.service.confirm_verification_code(
                db_session,
                uuid=verification_code.uuid,
                code='abcdef'
            )