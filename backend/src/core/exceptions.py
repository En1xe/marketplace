class InvalidPasswordException(Exception):
    ...
    
    
class InvalidFileExtension(Exception):
    def __init__(self, allowed_types: list = []) -> None:
        self.allowed_types = allowed_types
    

class InvalidTokenException(Exception):
    ...
    
    
class ObjectExpiredException(Exception):
    def __init__(self, object_name: str = 'object', status_code: int = 403) -> None:
        self.object_name = object_name
        self.status_code = status_code
    
    
class DuplicateEntryFoundException(Exception):
    ...
    

class NoObjectWasFoundException(Exception):
    def __init__(self, object_name: str = 'object') -> None:
        self.object_name = object_name
        

class SMTPException(Exception):
    ...


class IncorrectDataException(Exception):
    def __init__(self, object_name: str = 'object') -> None:
        self.object_name = object_name
        
        
class UnauthorizedException(Exception):
    def __init__(self, detail = 'Unauthorized access') -> None:
        self.detail = detail
        
        
class ForbiddenException(Exception):
    def __init__(self, detail = 'You don\'t have permission') -> None:
        self.detail = detail
        
        
class MethodNotImplementedException(Exception):
    def __init__(self) -> None:
        ...
        
        
class ForeignKeyViolationException(Exception):
    ...
    

class ObjectCompletedException(Exception):
    def __init__(self, object_name) -> None:
        self.object_name = object_name
        

class TooLargeEntityException(Exception):
    def __init__(self, max_size: int = 0) -> None:
        self.max_size = max_size
        
        
class TooManyRequestsException(Exception):
    ...
    

class OwnListingFavoriteException(Exception):
    ...