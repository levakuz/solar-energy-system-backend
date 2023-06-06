import uvicorn

if __name__ == '__main__':
    uvicorn.run('src.entrypoints.app:app', reload=True, port=8000)