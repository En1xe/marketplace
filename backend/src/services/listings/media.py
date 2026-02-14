from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.listings import ListingMediaRepository, ListingsRepository
from models.listings import ListingMediaModel
from core.clients.s3_client import S3Client
from utils.files import (
    get_compressed_image, 
    get_compressed_video, 
    get_file_name_from_s3_path
)
from core.constants import ALLOWED_IMAGE_FILE_MIME_TYPES
from core.logging import get_logger


logger = get_logger(__name__)

class ListingMediaService:
    def __init__(
        self, 
        listing_media_repo: ListingMediaRepository,
        listings_repo: ListingsRepository
    ):
        self.listing_media_repo = listing_media_repo
        self.listings_repo = listings_repo

    async def get_all_listing_media(
        self, 
        session: AsyncSession, 
        **kwargs
    ) -> list[ListingMediaModel]:
        logger.info('Getting all listing media')
        
        listing_media = await self.listing_media_repo.get_all(
            session, 
            **kwargs
        )
        logger.info('Retrieved %s listing media', len(listing_media))
        
        return listing_media
    
    async def process_and_upload_media(
        self, 
        session: AsyncSession, 
        s3_client: S3Client,
        listing_id: int,
        file: dict[str, Any],
    ) -> ListingMediaModel:
        """Uploads a media file to the S3 storage 
           and create a new record to the db
        """
        logger.info("Processing and uploading the file")
    
        if file['type'] in ALLOWED_IMAGE_FILE_MIME_TYPES:
            compressed_file = await get_compressed_image(file['obj'])
        else:
            compressed_file = get_compressed_video(file['obj'])

        url_to_img = await s3_client.upload_file(
            file=compressed_file,
            file_name=file['name']
        )
        logger.info('Uploaded the file to the S3 storage')

        listing_media_data = {}
        listing_media_data['listing_id'] = listing_id
        listing_media_data['url'] = url_to_img
        listing_media_obj = await self.listing_media_repo.add_one(
            session, 
            listing_media_data
        )
        logger.info("Listing media was created: %s", listing_media_obj.id)
        
        return listing_media_obj
    
    async def add_listing_media(
        self, 
        session: AsyncSession, 
        s3_client: S3Client,
        listing_id: int,
        files: list[dict[str, Any]],
        **kwargs
    ) -> list[ListingMediaModel]:
        """Processes and uploads media files"""
        logger.info("Creating and uploading multiple files")
        
        listing = await self.listings_repo.get_one_with_validation(
            session,
            id=listing_id,
            **kwargs
        )
        logger.info("Listing found: %s", listing.id)
        
        results = []
        
        for file in files:
            listing_media_obj = await self.process_and_upload_media(
                session, 
                s3_client, 
                listing_id, 
                file
            )
            
            results.append(listing_media_obj)
            
        logger.info("Files was created and uploaded successfully")
        return results
    
    async def update_listing_media(
        self,
        session: AsyncSession, 
        s3_client: S3Client,
        listing_id: int,
        existing_files: list[str],
        files: list[dict[str, Any]],
        **kwargs
    ):
        """Uploads listing media files
           
        1. Firstly, deletes listing media records, which exist in the db, 
           but don't exist in existing files list
        2. Adds new listing media files, which aren't in the db.

        Args:
            existing_files: Url files list, which must stay in S3 storage
            files: new media files for uploading
        """
        logger.info("Updating listing media")
        
        listing_media = await self.get_all_listing_media(
            session, 
            listing_id=listing_id
        )
        
        listing_filenames = [
            get_file_name_from_s3_path(listing_media_obj.url)
            for listing_media_obj in listing_media
        ]
        
        for listing_media_obj in listing_media:
            if listing_media_obj.url not in existing_files:
                await self.delete_one_listing_media(
                    session, 
                    s3_client, 
                    listing_media_obj.id, 
                    **kwargs
                )
        
        for file in files:
            if file['name'] not in listing_filenames:
                listing_media_obj = await self.process_and_upload_media(
                    session, 
                    s3_client, 
                    listing_id, 
                    file
                )
                
        logger.info("Listing media updated successfully")
            
    
    async def delete_one_listing_media(
        self, 
        session: AsyncSession, 
        s3_client: S3Client,
        listing_media_id: int,
        **kwargs
    ) -> None:
        """Deletes listing media record and media file from S3 storage"""
        logger.info("Deleting listing media")
        
        listing_media = await self.listing_media_repo.delete_one(
            session, 
            id=listing_media_id, 
            **kwargs
        )
        logger.info("Listing media deleted: %s", listing_media.id)
     
        file_name = listing_media.url.split('/')[-1]
     
        await s3_client.delete_file(
            file_name=file_name
        )
        logger.info("File removed from S3 storage successfully")