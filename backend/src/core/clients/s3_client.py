from io import BytesIO

from aiobotocore.session import get_session
from contextlib import asynccontextmanager

from core.constants import S3_CLIENT_ENDPOINT_URL, S3_CLIENT_REGION
from core.config import settings


class S3Client:
    """A client for asynchronous work with S3 storage"""
    
    def __init__(self) -> None:
        self.config = {
            'aws_access_key_id': settings.S3_CLIENT_ACCESS_KEY,
            'aws_secret_access_key': settings.S3_CLIENT_SECRET_KEY,
            'endpoint_url': S3_CLIENT_ENDPOINT_URL,
            'region_name': S3_CLIENT_REGION
        }
        self.bucket = settings.S3_BUCKET_NAME
        self.session = get_session()
        
    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client
            
            
    async def upload_file(
        self, 
        file_name: str,
        file: BytesIO,
    ) -> str:
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket,
                Key=file_name,
                Body=file
            )
               
        url_to_img = f'{settings.S3_CLIENT_ENDPOINT_URL}/{file_name}'
        return url_to_img
    
    async def delete_file(
        self,
        file_name: str,
    ):
        async with self.get_client() as client:
            await client.delete_object(
                Bucket=self.bucket,
                Key=file_name
            )

    