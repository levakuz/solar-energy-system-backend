from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.accounts.exceptions import InactiveUserException
from src.accounts.router import account_router
from src.auth.router import router as auth_router
from src.core.scheduler import service_scheduler
from src.database import init_postgres_database, init_mongodb_database
from src.device_types.router import device_type_router
from src.location_weather.router import location_weather_router
from src.locations.router import locations_router

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
app.include_router(device_type_router, prefix='/api/v1')
app.include_router(locations_router, prefix='/api/v1')
app.include_router(location_weather_router, prefix='/api/v1')

app.add_event_handler('startup', init_postgres_database)
app.add_event_handler('startup', init_mongodb_database)
app.add_event_handler('startup', service_scheduler.start)


@app.exception_handler(InactiveUserException)
async def validation_exception_handler(request, err):
    return JSONResponse(status_code=400, content={"detail": f"{err}"})
