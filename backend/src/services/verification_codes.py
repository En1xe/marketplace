from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from models.verification_codes import VerificationCodesModel
from repositories.verification_codes import VerificationCodesRepository
from schemas.verification_codes import VerificationCodeCreateSchema
from core.exceptions import ObjectExpiredException, IncorrectDataException
from core.logging import get_logger


logger = get_logger(__name__)

class VerificationCodesService:
    verification_code_expired_exception = ObjectExpiredException(object_name='verification code')
    
    def __init__(self, verification_codes_repo: VerificationCodesRepository):
        self.verification_codes_repo = verification_codes_repo

    async def get_one_verification_code(
        self,
        session: AsyncSession,
        uuid: UUID,
        **kwargs
    ) -> VerificationCodesModel:
        logger.info('Getting a verification code by uuid')
        
        verification_code = await self.verification_codes_repo.get_one(
            session, 
            uuid=uuid, 
            **kwargs
        )
        logger.info('Verification code found: %s', verification_code.id)
        
        return verification_code

    async def add_one_verification_code(
        self,
        session: AsyncSession,
        data: VerificationCodeCreateSchema
    ) -> VerificationCodesModel:
        logger.info('Creating a verification code')
        
        
        verification_code_data = data.model_dump()
        del verification_code_data['email']
        
        verification_code = await self.verification_codes_repo.add_one(
            session, 
            verification_code_data
        )
        logger.info('Verification code created: %s', verification_code.id)
        
        return verification_code

    
    async def validate_verification_code(
        self,
        session: AsyncSession,
        uuid: UUID,
    ) -> VerificationCodesModel:
        logger.info('Validation verification code')
        
        verification_code = await self.get_one_verification_code(
            session, 
            uuid=uuid
        )

        if not verification_code:
            logger.error('Verification code was not found')
            raise self.verification_codes_repo.no_object_was_found_exception
        
        if verification_code.expire_at < datetime.now():
            logger.error('Verification code is expired')
            raise self.verification_code_expired_exception
        
        logger.info("Validated successfully")
        return verification_code
        
    async def confirm_verification_code(
        self,
        session: AsyncSession,
        uuid: UUID,
        code: str | None
    ) -> VerificationCodesModel:
        logger.info('Confirming verification code')
    
        verification_code = await self.validate_verification_code(
            session,
            uuid=uuid
        )
        
        if not (verification_code.code == code):
            logger.error('Given code is incorrect')
            raise IncorrectDataException(object_name='verification code')
        
        logger.info("Validated and confirmed successfully")    
        return verification_code
    
    