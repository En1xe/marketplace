from uuid import uuid4
from typing import Any

from core.exceptions import (
    ForbiddenException, 
    MethodNotImplementedException
)
from core.types.base import SqlAlchemyModel
from core.logging import get_logger
from models.users import UsersModel


logger = get_logger(__name__)

def verify_if_request_user_is_owner(
    obj: SqlAlchemyModel,
    request_user: UsersModel,
    raise_exception: bool = True
) -> bool:
    """Checks whether the user is the owner of the object"""
    logger.debug('Verifying object ownership')
    
    try:
        if request_user:
            if request_user.id in obj.get_users_id():
                logger.debug('Ownership verified successfully')
                return True
        
        if raise_exception:
            raise ForbiddenException
                
    except AttributeError:
        raise MethodNotImplementedException
    
    logger.debug('User is not owner of the object')
    return False
    


def get_filtered_obj_by_request_user(
    objects: list[SqlAlchemyModel],
    request_user: UsersModel
) -> list:
    """Returns filtered object list, where the user is the owner"""
    
    filtered_data = [
        obj for obj in objects 
        if request_user.id in obj.get_users_id()
    ]
    
    return filtered_data


def create_test_user_data(
    password: str = '', 
    email: str = '',
    is_admin: bool = False
) -> dict[str, Any]:
    unique_id = uuid4()
    return {
        'username': f'user_{unique_id}',
        'password': password if password else '123456',
        'email': email if email else f'mail_{unique_id}@mail.com',
        'avatar': '',
        'is_admin': is_admin
    }
    