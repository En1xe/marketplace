import pytest
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile
from io import BytesIO
from unittest.mock import MagicMock

from utils.files import *
from core.exceptions import InvalidFileExtension, TooLargeEntityException


class TestUtilsFiles:
    
    def test_get_file_extension(
        self,
        mocker
    ):
        mock_file = mocker.Mock()
        mock_file.content_type = 'image/png'
        
        result = get_file_extension(mock_file)
        assert result == 'png'
        
        mock_file = mocker.Mock()
        mock_file.content_type = ''
        
        result = get_file_extension(mock_file)
        assert result == ''
        
    def test_get_file_name_from_s3_path(self):
        filename = 'image.png'
        assert get_file_name_from_s3_path(filename) == filename
        
        path = 'http://image.png'
        assert get_file_name_from_s3_path(path) == filename
        
    @pytest.mark.asyncio
    async def test_get_file_data(self):
        file = BytesIO(b'test data')
        filename = 'file.txt'
        
        upload_file = UploadFile(
            filename=filename,
            file=file
        )
        
        result = await get_file_data(upload_file)
        
        assert result['type'] == ''
        assert result['name'] == 'file.txt'
        assert isinstance(result['obj'], BytesIO)
        
    def test_verify_image_file(self):
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = 'image/png'
        mock_file.size = 500 * 1024
        
        verify_image_file(mock_file)
        
        mock_file.content_type = 'video/mp4'
        
        with pytest.raises(InvalidFileExtension):
            verify_image_file(mock_file)
            
        mock_file.content_type = 'image/png'
        mock_file.size = 1024 ** 3
        
        with pytest.raises(TooLargeEntityException):
            verify_image_file(mock_file)
            
    def test_verify_video_file(self):
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = 'video/mp4'
        mock_file.size = 500 * 1024
        
        verify_video_file(mock_file)
        
        mock_file.content_type = 'image/png'
        
        with pytest.raises(InvalidFileExtension):
            verify_video_file(mock_file)
            
        mock_file.content_type = 'video/mp4'
        mock_file.size = 1024 ** 4
        
        with pytest.raises(TooLargeEntityException):
            verify_video_file(mock_file)
    
    @pytest.mark.asyncio
    async def test_get_image_data(self, mocker):
        mock_file = MagicMock(spec=UploadFile)
        
        mock_verify_image_file = mocker.Mock()
        mock_verify_image_file = mocker.patch('utils.files.verify_image_file')
        
        mock_get_file_data = mocker.AsyncMock()
        mock_get_file_data.return_value = {
            'obj': BytesIO(),
            'filename': 'filename',
            'type': 'png'
        }
        mock_get_file_data = mocker.patch('utils.files.get_file_data')
        
        result = await get_image_data(mock_file)
        
        assert result == mock_get_file_data.return_value
        
        mock_verify_image_file.assert_called_once()
        mock_get_file_data.assert_awaited_once()
        
    @pytest.mark.asyncio
    async def test_get_media_file_image(self, mocker):
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = 'image'
        
        mock_verify_image_file = mocker.Mock()
        mock_verify_image_file = mocker.patch('utils.files.verify_image_file')
        
        mock_get_file_data = mocker.AsyncMock()
        mock_get_file_data.return_value = {
            'obj': BytesIO(),
            'filename': 'filename',
            'type': 'png'
        }
        mock_get_file_data = mocker.patch('utils.files.get_file_data')   
        
        result = await get_media_file_data(mock_file)
        assert result == mock_get_file_data.return_value
        
        mock_verify_image_file.assert_called_once()
        mock_get_file_data.assert_awaited_once()

            
    @pytest.mark.asyncio
    async def test_get_media_file_video(self, mocker):
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = 'video'
        
        mock_verify_video_file = mocker.Mock()
        mock_verify_video_file = mocker.patch('utils.files.verify_video_file')
        
        mock_get_file_data = mocker.AsyncMock()
        mock_get_file_data.return_value = {
            'obj': BytesIO(),
            'filename': 'filename',
            'type': 'mp4'
        }
        mock_get_file_data = mocker.patch('utils.files.get_file_data')
        
        result = await get_media_file_data(mock_file)
        assert result == mock_get_file_data.return_value
        
        mock_verify_video_file.assert_called_once()
        mock_get_file_data.assert_awaited_once()
        
    @pytest.mark.asyncio
    async def test_get_media_file_error(self, mocker):
        mock_file = MagicMock(spec=UploadFile)
        mock_file.content_type = ''
        
        mock_verify_video_file = mocker.Mock()
        mock_verify_video_file = mocker.patch('utils.files.verify_video_file')
        
        mock_get_file_data = mocker.AsyncMock()
        mock_get_file_data.return_value = {
            'obj': BytesIO(),
            'filename': 'filename',
            'type': 'mp4'
        }
        mock_get_file_data = mocker.patch('utils.files.get_file_data')
        
        with pytest.raises(InvalidFileExtension):
            await get_media_file_data(mock_file)
            
    @pytest.mark.asyncio
    async def test_get_compressed_image(
        self,
        sample_image: BytesIO,
    ):
        compressed_image = await get_compressed_image(sample_image)
        
        assert isinstance(compressed_image, BytesIO)
        
        result_image = Image.open(compressed_image)
        
        assert result_image.format == 'WEBP'
        assert result_image.width < 600
        assert result_image.height < 400
        
        with pytest.raises(UnidentifiedImageError):
            compressed_image = await get_compressed_image(
                BytesIO(b'')
            ) 
        
    @pytest.mark.asyncio
    async def test_get_compressed_image_rgb(
        self,
        sample_transparent_image: BytesIO
    ):
        compressed_image = await get_compressed_image(sample_transparent_image)
        
        assert isinstance(compressed_image, BytesIO)
        
        result_image = Image.open(compressed_image)
        
        assert result_image.mode == 'RGB'
        assert result_image.format == 'WEBP'
        assert result_image.width < 600
        assert result_image.height < 400
        
    @pytest.mark.asyncio
    async def test_get_compressed_image_custom_dimension(
        self,
        sample_transparent_image: BytesIO
    ):
        custom_width = 1000
        custom_height = 1000
        
        compressed_image = await get_compressed_image(
            sample_transparent_image,
            width=custom_width,
            height=custom_height
        ) 
        result_image = Image.open(compressed_image)
        
        assert result_image.width <= custom_width
        assert result_image.height <= custom_height
