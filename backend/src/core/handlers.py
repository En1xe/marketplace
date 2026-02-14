from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .exceptions import *
from utils.text import get_text_by_condition


def handle_sql_integrity_error(error: IntegrityError):
    """Handles integrity data error SQLAlchemy"""
    
    original_error = error.orig

    if 'asyncpg.exceptions.ForeignKeyViolationError' in str(original_error):
        raise ForeignKeyViolationException
    else:
        raise DuplicateEntryFoundException
    

def register_exception_handlers(app: FastAPI) -> None:
    """Registers all custom exception handler in FastAPI application"""

    @app.exception_handler(InvalidPasswordException)
    def invalid_password_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'message': 'Invalid password'}
        )
        
        
    @app.exception_handler(InvalidTokenException)
    def invalid_token_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'message': 'Invalid token'}
        )
        
        
    @app.exception_handler(ObjectExpiredException)
    def object_expired_exception_handler(
        req: Request,
        exc: ObjectExpiredException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={'message': f'{exc.object_name.capitalize()} expired'}
        )
        
        
    @app.exception_handler(NoObjectWasFoundException)
    def no_object_was_found_exception_handler(
        req: Request,
        exc: NoObjectWasFoundException
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': f'No {exc.object_name} was found'}
        )
        
    @app.exception_handler(DuplicateEntryFoundException)
    def duplicate_was_found_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'A record with these details already exists'}
        )
        
    @app.exception_handler(SMTPException)
    def smtp_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={'message': 'SMTP server is unavailable'}
        )
        

    @app.exception_handler(IncorrectDataException)
    def incorrect_data_exception_handler(
        req: Request,
        exc: IncorrectDataException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': f'Given {exc.object_name} is incorrect'}
        )
        
    @app.exception_handler(UnauthorizedException)
    def unauthorized_exception_handler(
        req: Request,
        exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'message': exc.detail}
        )
        
    @app.exception_handler(ForbiddenException)
    def forbidden_exception_handler(
        req: Request,
        exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'message': exc.detail}
        )
        
    @app.exception_handler(MethodNotImplementedException)
    def method_is_not_implemented_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            content={'message': 'The method is not implemented'}
        )
        
    @app.exception_handler(ForeignKeyViolationException)
    def foreign_key_violation_exception(*args):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Foreign key violation'}
        )
        
    @app.exception_handler(ObjectCompletedException)
    def object_completed_exception(
        req: Request,
        exc: ObjectCompletedException
    ):
        return JSONResponse(
            status_code=status.HTTP_410_GONE,
            content={'message': f'{exc.object_name.upper()} is completed.'}
        )
        
    @app.exception_handler(InvalidFileExtension)
    def invalid_file_extension_exception(
        req: Request,
        exc: InvalidFileExtension
    ):
        message = get_text_by_condition(
            main_text='This extension is not appropriate.',
            optional_text=f'Allowed types: {', '.join(exc.allowed_types)}',
            value_condition=exc.allowed_types
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': message}
        )
        
    @app.exception_handler(TooLargeEntityException)
    def too_large_entity_exception(
        req: Request,
        exc: TooLargeEntityException
    ):
        message = get_text_by_condition(
            main_text='The file is too big.',
            optional_text=f'Max size: {exc.max_size} MBytes',
            value_condition=exc.max_size
        )
        
        return JSONResponse(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            content={'message': message}
        )
        
        
    @app.exception_handler(TooManyRequestsException)
    def too_many_requests_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={'message': 'Too many requests were sent to the server'}
        )
        
    @app.exception_handler(OwnListingFavoriteException)
    def own_listing_favorite_exception_handler(*args):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'You cannot add your own listing to favorite'}
        )
        