from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.accounts.router import account_router
from src.database import init_database

app = FastAPI()

app.include_router(auth_router)
app.include_router(account_router)

app.add_event_handler('startup', init_database)
