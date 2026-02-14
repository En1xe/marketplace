import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from models.users import UsersModel
from core.factories.users import create_user_factory


class TestUserRouters:
    
    @pytest.mark.asyncio
    async def test_get_users_without_request_user(
        self,
        db_session: AsyncSession, 
        client: AsyncClient
    ):
        user = await create_user_factory(db_session)
        
        result = await client.get('/users')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, list)
        assert len(content) == 1
        
        user_data = content[0]
        
        assert 'username' in user_data
        assert 'password' not in user_data
        
    @pytest.mark.asyncio
    async def test_get_users_with_request_user(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):
        user = await create_user_factory(db_session)
        
        result = await client.get('/users')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, list)
        assert len(content) == 2
        
        user_data = content[0]
        
        assert 'username' in user_data
        assert 'email' in user_data
        assert 'is_oauth' in user_data
        
    @pytest.mark.asyncio
    async def test_get_user_by_token(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_user: UsersModel
    ):
        user = await create_user_factory(db_session)
        
        result = await client.get('/users/token')
        content = result.json()
        
        assert result.status_code == 200
        
        assert 'username' in content
        assert 'email' in content
        assert 'is_oauth' in content
        
    @pytest.mark.asyncio
    async def test_get_user_without_request_user(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
    ):
        user = await create_user_factory(db_session)
        
        result = await client.get(f'/users/{user.uuid}')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'username' in content
        
        result = await client.get(f'/users/{user.uuid}?detail=true')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'listings' in content
        
    @pytest.mark.asyncio
    async def test_get_user_with_request_user(
        self, 
        client: AsyncClient,
        request_user: UsersModel
    ):  
        result = await client.get(f'/users/{request_user.uuid}')
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'username' in content
        assert 'email' in content
        assert 'is_oauth' in content
        
        result = await client.get(f'/users/{request_user.uuid}?detail=true')
        content = result.json()

        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'listings' in content
        
    @pytest.mark.asyncio
    async def test_get_user_by_email_without_request_user(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
    ):  
        user = await create_user_factory(db_session)
        
        result = await client.post('/users/email', json={'email': user.email})
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'username' in content
        
    @pytest.mark.asyncio
    async def test_get_user_by_email_with_request_user(
        self,
        client: AsyncClient,
        request_user: UsersModel
    ):  
        result = await client.post('/users/email', json={'email': request_user.email})
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'username' in content
        assert 'email' in content
        assert 'is_oauth' in content
        
    @pytest.mark.asyncio
    async def test_create_user(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
    ):  
        result = await client.post(
            '/users', 
            json={
                'username': 'username',
                'password': '123456',
                'email': 'mail@mail.com'
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert 'username' in content
        assert 'email' in content
        assert 'is_oauth' in content
        
        result = await db_session.execute(select(UsersModel))
        
        assert len(result.scalars().all()) == 1
        
    @pytest.mark.asyncio
    async def test_update_user(
        self, 
        client: AsyncClient,
        request_user: UsersModel
    ):  
        new_username = 'new_username'
        
        result = await client.patch(
            f'/users/{request_user.uuid}', 
            json={
                'username': new_username,
            }
        )
        content = result.json()
        
        assert result.status_code == 200
        assert isinstance(content, dict)
        assert content.get('username') == new_username
        
    @pytest.mark.asyncio
    async def test_delete_user(
        self,
        db_session: AsyncSession, 
        client: AsyncClient,
        request_admin_user: UsersModel
    ):
        result = await client.delete(f'/users/{request_admin_user.uuid}')
        
        assert result.status_code == 204
        
        result = await db_session.execute(select(UsersModel))
        assert len(result.scalars().all()) == 0
        
    @pytest.mark.asyncio
    async def test_upload_user_avatar(
        self,
        client: AsyncClient,
        mock_users_service: UsersModel,
        mock_uploaded_image
    ):
        result = await client.post(f'/users/{mock_users_service.uuid}/avatar')
        content = result.json()

        assert result.status_code == 200
        assert 'username' in content
        