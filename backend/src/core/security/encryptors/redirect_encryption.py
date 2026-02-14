import json
from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from secrets import token_bytes

from core.exceptions import IncorrectDataException
from core.config import settings


class RedirectEncryptor:
    """Encryptor for secure redirects
    
    Uses AES-GCM algorithm for authenticated data encryption,
    which passes via URLs
    """
    
    def __init__(self) -> None:
        self.key = urlsafe_b64decode(
            settings.REDIRECT_ENCRYPTION_KEY
        )
        self.aesgcm = AESGCM(self.key)
        
    def encrypt(self, data: dict) -> str:
        """Encrypts a dict into a url-safe string"""
        
        try:
            json_data = json.dumps(data).encode()
            nonce = token_bytes(12)
            
            cipher_text = self.aesgcm.encrypt(
                nonce, 
                json_data,
                b''
            )
            
            tag = cipher_text[-16:]
            encrypted_data = cipher_text[:-16]
            
            result = {
                'nonce': urlsafe_b64encode(nonce).decode(),
                'encrypted_data': urlsafe_b64encode(encrypted_data).decode(),
                'tag': urlsafe_b64encode(tag).decode(),
            }
            
            return urlsafe_b64encode(
                json.dumps(result).encode()
            ).decode()
        except:
            raise IncorrectDataException
    
    def decrypt(self, encrypted_data: str) -> dict:
        """Decrypt string back into the dict"""
        
        try:
            decoded_data = json.loads(
                urlsafe_b64decode(encrypted_data).decode()
            )
            
            nonce = urlsafe_b64decode(decoded_data['nonce'])
            encrypted_data = urlsafe_b64decode(decoded_data['encrypted_data'])
            tag = urlsafe_b64decode(decoded_data['tag'])
            
            full_cipher_text = encrypted_data + tag
            
            cipher_text = self.aesgcm.decrypt(
                nonce,
                full_cipher_text, 
                b''
            )
            
            return json.loads(cipher_text.decode())
        except:
            raise IncorrectDataException(object_name='token')
    
    
redirect_encryptor = RedirectEncryptor()\
    