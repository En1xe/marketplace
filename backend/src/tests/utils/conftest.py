from pytest import fixture
from io import BytesIO
from PIL import Image


@fixture
def sample_image():
    img = Image.new('RGB', (600, 400), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

@fixture
def sample_transparent_image():
    img = Image.new('RGBA', (600, 400), color=(255, 0, 0, 128))
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes