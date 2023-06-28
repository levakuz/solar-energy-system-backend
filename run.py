import uvicorn

from src.settings import settings

if __name__ == '__main__':
    uvicorn.run('src.entrypoints.app:app', reload=True, port=settings.SERVER_PORT)
