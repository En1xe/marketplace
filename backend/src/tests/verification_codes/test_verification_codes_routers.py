import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models.verification_codes import VerificationCodesModel
from core.factories.users import create_user_factory
from core.factories.verification_codes import create_verification_code_factory


class TestVerificationCodeRouters:
        
    @pytest.mark.asyncio
    async def test_get_verification_code(
        self, 
        db_session: AsyncSession,
        client: AsyncClient
    ):  
        verification_code = await create_verification_code_factory(db_session)
        
        result = await client.get(f'/verification_codes/{verification_code.uuid}')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'code' not in content
        assert 'operation_type' in content
        
    @pytest.mark.asyncio
    async def test_add_verification_code(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        mocker
    ):  
        user = await create_user_factory(db_session)
        
        result = await client.post(
            '/verification_codes/', 
            json={
                'email_request': {
                    'email': "mail@mail.com"
                },
                'data': {
                    'user_id': user.id,
                    'operation_type': 'verification'
                }
            }
        )
        content = result.json()
        
        mock_background_task = mocker.Mock()
        mock_background_task.add_task.return_value = None
        mocker.patch('api.routers.verification_codes.BackgroundTasks', mock_background_task)
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'user_id' not in content
        assert 'user' not in content
        assert 'code' not in content
        assert 'operation_type' in content
        
        result = await db_session.execute(select(VerificationCodesModel))
        assert len(result.scalars().all()) == 1
        
    @pytest.mark.asyncio
    async def test_check_verification_code(
        self, 
        client: AsyncClient,
        db_session: AsyncSession
    ):  
        verification_code = await create_verification_code_factory(db_session)
        
        result = await client.post(
            f'/verification_codes/{verification_code.uuid}/verify', 
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'success' in content
        
    @pytest.mark.asyncio
    async def test_confirm_verification_code(
        self,
        db_session: AsyncSession, 
        client: AsyncClient
    ):
        verification_code = await create_verification_code_factory(db_session)
        
        result = await client.post(
            f'/verification_codes/{verification_code.uuid}/confirm',
            json={
                'code': verification_code.code
            } 
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'success' in content
    