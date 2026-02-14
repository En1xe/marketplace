from urllib.parse import urlencode, quote
from httpx import AsyncClient
from secrets import token_urlsafe

from core.config import settings
from core.constants import GITHUB_REDIRECT_URL, GITHUB_TOKEN_URL
from .core import AbstractOAuthService
from core.logging import get_logger


logger = get_logger(__name__)

class GithubOAuthService(AbstractOAuthService):
    
    def get_oauth_redirect_uri(self):
        logger.info("Generating redirect url for GitHub OAuth")
        random_state = token_urlsafe(16)

        base_url = 'https://github.com/login/oauth/authorize'
        params = {
            'client_id': settings.GITHUB_OAUTH_CLIENT_ID,
            'redirect_uri': GITHUB_REDIRECT_URL,
            'scope': ' '.join([ 
                'user',
                'repo'
            ]),
            'state': random_state
        }

        query_string = urlencode(
            params, 
            quote_via=quote
        )
        logger.info("Generated successfully")
        return f'{base_url}?{query_string}'
    
    async def get_user_data(
        self,
        code: str
    ):
        logger.info('Getting user data from GitHub')
        
        async with AsyncClient() as client:
            response = await client.post(
                url=GITHUB_TOKEN_URL,
                data={
                    'client_id': settings.GITHUB_OAUTH_CLIENT_ID,
                    'client_secret': settings.GITHUB_OAUTH_CLIENT_SECRET,
                    'code': code,
                    'redirect_uri': GITHUB_REDIRECT_URL,
                },
                headers={"Accept": "application/json"}
            )
            
            data = response.json()
            access_token = data.get('access_token')
            logger.info("Received access token of the user")
            
            user_response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )
            logger.info("Received information about the user")
            
            user_data = user_response.json()

            
            email_response = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            email_data = email_response.json()
            logger.info("Received an email of the user")

            logger.info('Retrieved successfully')
            return {
                'username': user_data.get('login'),
                'avatar': user_data.get('avatar_url'),
                'email': email_data[0].get('email'),
                'password': token_urlsafe(16),
            }
            