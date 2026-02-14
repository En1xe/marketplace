import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.listings import ListingMediaModel
from core.factories.listings import (
    create_listing_media_factory,
    create_listing_factory
)
from core.factories.users import create_user_factory

from services.listings.media import ListingMediaService
from repositories.listings import ListingMediaRepository, ListingsRepository


class TestListingMediaService:
    
    service = ListingMediaService(
        listings_repo=ListingsRepository(),
        listing_media_repo=ListingMediaRepository()
    )
    
    @pytest.mark.asyncio
    async def test_get_all_listing_media(
        self,
        db_session: AsyncSession
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        await create_listing_media_factory(
            db_session,
            listing_id=listing.id
        )
        await create_listing_media_factory(
            db_session,
            listing_id=listing.id
        )
            
        result = await self.service.get_all_listing_media(db_session)
            
        assert len(result) == 2
        
    @pytest.mark.asyncio
    async def test_process_and_upload_media(
        self,
        db_session: AsyncSession,
        mocker
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        mock_get_compressed_image = mocker.AsyncMock()
        mock_get_compressed_video = mocker.Mock()
        mock_get_compressed_image = mocker.patch('services.listings.media.get_compressed_image', return_value=None)
        mock_get_compressed_video = mocker.patch('services.listings.media.get_compressed_video', return_value=None)
        
        mock_s3_client = mocker.AsyncMock()
        mock_s3_client.upload_file.return_value = 'path_to_img'
        
        result = await self.service.process_and_upload_media(
            session=db_session,
            s3_client=mock_s3_client,
            listing_id=listing.id,
            file={
                'type': 'png',
                'obj': None,
                'name': 'name'
            }
        )
        
        assert isinstance(result, ListingMediaModel) 
        mock_get_compressed_image.assert_awaited_once()
        
        result = await self.service.process_and_upload_media(
            session=db_session,
            s3_client=mock_s3_client,
            listing_id=listing.id,
            file={
                'type': 'video',
                'obj': None,
                'name': 'name'
            }
        )
        
        assert isinstance(result, ListingMediaModel) 
        mock_get_compressed_video.assert_called_once()
        
        assert mock_s3_client.upload_file.await_count == 2
        
    @pytest.mark.asyncio
    async def test_add_listing_media(
        self,
        db_session: AsyncSession,
        mocker
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        mock_get_compressed_image = mocker.AsyncMock()
        mock_get_compressed_video = mocker.Mock()
        mock_get_compressed_image = mocker.patch('services.listings.media.get_compressed_image', return_value=None)
        mock_get_compressed_video = mocker.patch('services.listings.media.get_compressed_video', return_value=None)
        
        mock_s3_client = mocker.AsyncMock()
        mock_s3_client.upload_file.return_value = 'path_to_img'
        
        results = await self.service.add_listing_media(
            session=db_session,
            s3_client=mock_s3_client,
            listing_id=listing.id,
            files=[
                {
                    'type': 'png',
                    'obj': None,
                    'name': 'name'
                },
                {
                    'type': 'mp4',
                    'obj': None,
                    'name': 'name'
                },
            ],
            request_user=user
        )

        for result in results:
            assert isinstance(result, ListingMediaModel)
            
        assert mock_s3_client.upload_file.await_count == 2
        mock_get_compressed_image.assert_awaited_once()
        mock_get_compressed_video.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_update_listing_media(
        self,
        db_session: AsyncSession,
        mocker
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        mock_get_compressed_image = mocker.AsyncMock()
        mock_get_compressed_video = mocker.Mock()
        mock_get_compressed_image = mocker.patch('services.listings.media.get_compressed_image', return_value=None)
        mock_get_compressed_video = mocker.patch('services.listings.media.get_compressed_video', return_value=None)
        
        mock_s3_client = mocker.AsyncMock()
        mock_s3_client.upload_file.return_value = 'file3'
        
        listing_media = await create_listing_media_factory(
            db_session,
            listing_id=listing.id,
            url='file1'
        )
        listing_media = await create_listing_media_factory(
            db_session,
            listing_id=listing.id,
            url='file2'
        )
        
        existing_files = ['file2']
        files = [{
            'type': 'mp4',
            'obj': None,
            'name': 'file3'
        }]
        
        await self.service.update_listing_media(
            session=db_session,
            s3_client=mock_s3_client,
            listing_id=listing.id,
            existing_files=existing_files,
            files=files,
            request_user=user
        )
        
        result = await db_session.execute(select(ListingMediaModel))
        result = result.scalars().all()
        file_urls = [file.url for file in result]
        
        assert len(result) == 2
        assert 'file2' in file_urls
        assert 'file3' in file_urls
        
    @pytest.mark.asyncio
    async def test_delete_one_listing_media(
        self,
        db_session: AsyncSession,
        mocker
    ):
        user = await create_user_factory(db_session)
        listing = await create_listing_factory(db_session, publisher_id=user.id)
        
        listing_media = await create_listing_media_factory(
            db_session,
            listing_id=listing.id
        )
        
        mock_s3_client = mocker.AsyncMock()
        mock_s3_client.delete_file.return_value = 'path_to_img'
        
        await self.service.delete_one_listing_media(
            db_session,
            mock_s3_client,
            listing_media_id=listing_media.id,
            request_user=user
        )