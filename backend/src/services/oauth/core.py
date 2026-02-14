from abc import abstractmethod, ABC


class AbstractOAuthService(ABC):
    
    @abstractmethod
    def get_oauth_redirect_uri():
        """Generate redirect uri for OAuth authentication"""
        ...
        
    @abstractmethod
    async def get_user_data():
        """Fetches user data from a service"""
        ...