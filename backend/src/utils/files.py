import subprocess

from PIL import Image
from fastapi import UploadFile
from io import BytesIO

from core.logging import get_logger
from core.exceptions import InvalidFileExtension, TooLargeEntityException
from core.constants import ALLOWED_IMAGE_FILE_MIME_TYPES, ALLOWED_VIDEO_FILE_MIME_TYPES


logger = get_logger(__name__)

def get_file_extension(file: UploadFile):
    content_type = file.content_type
    
    if not content_type: 
        return ''
    
    return content_type.split('/')[-1]


def get_file_name_from_s3_path(path: str):
    """Extract a file name from the s3 storage path"""
    
    return path.split('/')[-1]


async def get_file_data(file: UploadFile):
    """Returns a BytesIO object and metadata."""
    logger.info('Reading file data')
    
    content = await file.read()
    file_obj = BytesIO(content)
    
    logger.info('File object was created')
    return {
        'obj': file_obj,
        'name': file.filename,
        'type': get_file_extension(file)
    }
    
    
async def get_image_data(file: UploadFile):
    """Gets image data with pre-flight checking"""
    logger.info('Getting image file data')
    
    verify_image_file(file)
    
    data = await get_file_data(file)
    logger.info('Retrieved file data')
    return data

async def get_media_file_data(file: UploadFile):
    """Gets file data with type checking (image/video)"""
    logger.info('Getting media file data')
    
    file_type = file.content_type if file.content_type else ''
    
    if 'video' in file_type:
        verify_video_file(file)
    elif 'image' in file_type:
        verify_image_file(file)
    else:
        logger.error('Media file extension is not allowed')
        raise InvalidFileExtension()
    
    data = await get_file_data(file)
    logger.info('Retrieved file data')
    return data


def verify_image_file(file: UploadFile):
    """Checks that the file is a valid image."""
    logger.info('Verifying the image file')
    
    if get_file_extension(file) not in ALLOWED_IMAGE_FILE_MIME_TYPES:
        logger.error('The image file extension is not allowed')
        raise InvalidFileExtension(
            allowed_types=ALLOWED_IMAGE_FILE_MIME_TYPES
        )
         
    file_size = file.size / 1024 / 1024 if file.size else 0 # MBytes
    
    if file_size > 1:
        logger.error('The image file size is too large')
        raise TooLargeEntityException(max_size=1)    
    
    
def verify_video_file(file: UploadFile):
    """Checks that the file is a valid video."""
    logger.info('Verifying the video file')
    
    if get_file_extension(file) not in ALLOWED_VIDEO_FILE_MIME_TYPES:
        logger.error('The video file extension is not allowed')
        raise InvalidFileExtension(
            allowed_types=ALLOWED_VIDEO_FILE_MIME_TYPES
        )
         
    file_size = file.size / 1024 / 1024 if file.size else 0 # MBytes
    
    if file_size > 100:
        logger.error('THe video file size is too large')
        raise TooLargeEntityException(max_size=1)    
    
    
async def get_compressed_image(
    file: BytesIO,
    width: int = 300,
    height: int = 300,
) -> BytesIO:
    """Compresses the image to the specific dimensions"""
    logger.info('Compressing the image file')
    
    file.seek(0)
    
    img = Image.open(file) 
    img.thumbnail(
        (width, height), 
        Image.Resampling.LANCZOS
    )
    
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
        
    compressed_img = BytesIO()
    img.save(
        compressed_img, 
        format='webp', 
        quality=80, 
        optimize=True
    )
    compressed_img.seek(0)
    
    logger.info('The image file was compressed successfully')
    return compressed_img


def get_compressed_video(
    file: BytesIO,
    crf: int = 23,
) -> BytesIO:
    """Compresses the video to the specific dimensions"""
    logger.info('Compressing the video file')
    
    cmd = [
        'ffmpeg',
        '-i', 'pipe:0',
        '-c:v', 'libx264',
        '-crf', str(crf),
        '-preset', 'medium',
        '-f', 'mp4',
        'pipe:1'
    ]
    
    process = subprocess.Popen(
        cmd, 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    stdout, _ = process.communicate(input=file.getvalue())
    
    res = BytesIO(stdout)
    logger.info('The video file was compressed successfully')
    return res