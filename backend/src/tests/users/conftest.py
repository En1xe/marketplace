from pytest_asyncio import fixture  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from core.factories.users import create_user_factory
from api.dependencies import get_users_service
from main import app


@fixture(autouse=True)
async def clean_up_users(db_session: AsyncSession):
    yield
    
    await db_session.execute(text('DELETE from users'))
    await db_session.commit()
    
    
@fixture
async def mock_users_service(
    db_session: AsyncSession,
    mocker
):
    user = await create_user_factory(db_session)
    
    mock_service = mocker.Mock()
    mock_service.upload_one_user_avatar = mocker.AsyncMock(return_value=user)
    
    async def override_get_users_service():
        return mock_service
    
    app.dependency_overrides[get_users_service] = override_get_users_service
    
    yield user
    
    app.dependency_overrides.pop(get_users_service, None)
    