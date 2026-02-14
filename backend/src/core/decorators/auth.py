from functools import wraps
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from utils.users import (
    verify_if_request_user_is_owner, 
    get_filtered_obj_by_request_user
)
from models.users import UsersModel
from core.exceptions import (
    UnauthorizedException, 
    ForbiddenException
)


def is_authenticated(func: Callable) -> Callable:
    """Checks whether request user is authenticated"""
    
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        user = request.state.user

        if not user:
            raise UnauthorizedException
        
        return await func(request, *args, **kwargs)
        
    return wrapper


def is_admin(func: Callable) -> Callable:
    """Checks whether request user is admin"""
    
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        user = request.state.user

        if not user:
            raise UnauthorizedException
        
        if not user.is_admin:
            raise ForbiddenException

        return await func(request, *args, **kwargs)
        
    return wrapper


def is_owner_or_admin(func: Callable) -> Callable:
    """Checks whether request user is object owner or admin"""
    
    @wraps(func)
    async def wrapper(
        self, 
        session: AsyncSession, 
        request_user: UsersModel | None = None, 
        *args, 
        **kwargs
    ):
        data = await func(self, session, *args, **kwargs)
        
        if not request_user:
            raise UnauthorizedException

        if request_user.is_admin:
            return data

        if isinstance(data, list):
            data = get_filtered_obj_by_request_user(data, request_user)
        else:
            verify_if_request_user_is_owner(data, request_user)

        return data
    
    return wrapper
