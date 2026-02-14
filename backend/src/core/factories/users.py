from sqlalchemy.ext.asyncio import AsyncSession

from models.users import UsersModel
from utils.users import create_test_user_data


async def create_user_factory(
    session: AsyncSession, 
    **kwargs
) -> UsersModel:
    user = UsersModel(**create_test_user_data(**kwargs))
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
