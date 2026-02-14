import pytest

from utils.auth import *
from core.exceptions import InvalidTokenException
from schemas.auth import CreateAccessTokenSchema, CreateRefreshTokenSchema


class TestUtilsAuth:
    
    def test_encode_jwt(self):
        payload = {
            'email': 'mail@mail.com',
            'data': 'data'
        }
        
        token = encode_jwt(payload)

        assert len(token.split('.')) == 3
        
    def test_decode_jwt(self):
        payload = {
            'email': 'mail@mail.com',
            'data': 'data'
        }
        
        token = encode_jwt(payload)
        decoded_payload = decode_jwt(token)
        
        assert decoded_payload['email'] == 'mail@mail.com'
        assert decoded_payload['data'] == 'data'
        
        with pytest.raises(InvalidTokenException):
            decode_jwt('token')
            
    def test_get_access_token(self):
        token = get_access_token(CreateAccessTokenSchema(
            email='email@email.com',
            id=1
        ))

        assert len(token.split('.')) == 3
        
    def test_get_refresh_token(self):
        token = get_refresh_token(CreateRefreshTokenSchema(
            email='email@email.com',
        ))

        assert len(token.split('.')) == 3
