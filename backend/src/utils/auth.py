import jwt
from datetime import datetime, timezone, timedelta
from fastapi import Response
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

from core.config import settings
from core.logging import get_logger
from core.exceptions import InvalidTokenException
from schemas.auth import CreateAccessTokenSchema, CreateRefreshTokenSchema


logger = get_logger(__name__)

pwd_context = CryptContext(
    schemes=['bcrypt'], 
    deprecated='auto'
)

def encode_jwt(
    payload: dict,
    expire_timedelta: timedelta = timedelta(
        minutes=settings.auth.access_token_expire_minutes
    ),
    key=settings.auth.PRIVATE_KEY.read_text(),
    algorithm=settings.auth.algorithm,
) -> str:
    """Encodes the payload into a JWT token"""
    logger.info('Encoding JWT token')
    
    now = datetime.now(timezone.utc)
    expire = now + expire_timedelta

    to_encode = payload.copy()
    to_encode.update(
        iat=now,
        exp=expire
    )

    encoded_token = jwt.encode(
        to_encode,
        key,
        algorithm
    )
    logger.info('JWT token was encoded successfully')

    return encoded_token


def decode_jwt(
    token: str | bytes,
    public_key=settings.auth.PUBLIC_KEY.read_text(),
    algorithm=settings.auth.algorithm
) -> dict:
    """Decodes and verify the JWT token"""
    logger.info('Decoding JWT token')
    
    try:
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm]
        )
        logger.info('JWT token was decoded successfully')
        
        return decoded_token
    except jwt.InvalidTokenError:
        logger.error('JWT token is invalid')
        raise InvalidTokenException


def get_access_token(user: CreateAccessTokenSchema) -> str:
    """Creates an access token for the user"""
    logger.info('Creating access token')
    
    access_token = encode_jwt(
        payload={
            'sub': user.email,
            'email': user.email,
            'id': user.id,
        }
    )
    
    logger.info('Access token created')
    
    return access_token


def get_refresh_token(user: CreateRefreshTokenSchema) -> str:
    """Creates a refresh token for the user"""
    logger.info('Creating refresh token')
    
    refresh_token = encode_jwt(
        payload={
            'sub': user.email
        },
        expire_timedelta=timedelta(
            days=settings.auth.refresh_token_expire_days
        )
    )
    
    logger.info('Refresh token created')

    return refresh_token


def hash_password(pwd: str) -> str:
    """Hashes a password using bcrypt"""
    logger.info('Hashing password')
    password = pwd_context.hash(pwd)
    
    logger.info('Password hashed successfully')
    return password


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    """Checks the password against its hash"""
    logger.info('Verifying password')
    is_valid = pwd_context.verify(plain_pwd, hashed_pwd)
    
    logger.info('Password verified successfully')
    return is_valid


def set_refresh_token_cookie(
    refresh_token: str | None, 
    response: Response
) -> None:
    """Sets a refresh token into an http-only cookies"""
    
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        max_age=settings.auth.refresh_token_expire_days * 24 * 60 * 60
    )
