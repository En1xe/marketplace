from pathlib import Path


# ------------------ Paths -------------------------

BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / 'src'

ENV_PATH = BASE_DIR / '.env'
LOGS_PATH = BASE_DIR / 'logs'
AUTH_PRIVATE_KEY_PATH = SRC_DIR / 'core' / 'security' / 'security_keys' / 'private.pem'
AUTH_PUBLIC_KEY_PATH = SRC_DIR / 'core' / 'security' / 'security_keys' / 'public.pem'


# ------------------ Values -------------------------

VERIFICATION_CODE_EXPIRE_MINUTES = 10

GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'

S3_CLIENT_ENDPOINT_URL = 'https://s3.ru-7.storage.selcloud.ru'
S3_CLIENT_REGION = 'ru-7'

ALLOWED_IMAGE_FILE_MIME_TYPES = [
    'jpeg', 'png', 'gif', 'webp'
]

ALLOWED_VIDEO_FILE_MIME_TYPES = [
    'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm',
    'mpeg', 'mpg', '3gp', 'ogv', 'ts', 'm4v'
]

FORBIDDEN_ENDPOINT_PROP_NAMES = [
    'service',
    'session',
    'request'
]