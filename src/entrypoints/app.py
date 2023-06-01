from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.accounts.router import account_router
from src.database import init_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix='/api/v1')
app.include_router(account_router, prefix='/api/v1')

app.add_event_handler('startup', init_database)
