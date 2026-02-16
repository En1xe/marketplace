import uvicorn
from core.create_app import create_application
from core.logging import setup_logging


setup_logging()

app = create_application()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8000)
    