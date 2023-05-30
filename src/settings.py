from pydantic import BaseSettings

TORTOISE_ORM = {
    "connections": {"default": "asyncpg://admin:admin@127.0.0.1:5432/test"},
    "apps": {
        "models": {
            "models": [
                "src.accounts.models",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    }}


class Settings(BaseSettings):
    # auth_key: str
    # api_key: str = Field(..., env='my_api_key')
    db_url: str = ''
    SECRET_KEY = 'cd6220207f0b9384a974b86ed73378ca1f6b57bc5af7b1e2eb937e35e78a54dd'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # TORTOISE_ORM: TORTOISE_ORM = TORTOISE_ORM

    class Config:
        fields = {
            'auth_key': {
                'env': 'my_auth_key'
            }
        }
