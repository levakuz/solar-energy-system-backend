from datetime import timedelta
from typing import Annotated

import fastapi.routing
from fastapi import HTTPException, Depends
from starlette import status

from src.accounts.domain import Account
from src.auth.schemas import Token, LoginData
from src.auth.services import authenticate_user
from src.auth.utils import create_access_token
from src.core.repository import AbstractRepository, TortoiseRepository
from src.core.repository_factory import RepositoryFactory
from src.settings import settings

router = fastapi.routing.APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: LoginData,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=Account,
                type_repository=TortoiseRepository
            ))
        ]
):
    user = await authenticate_user(account_repository, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token.parse_obj({"access_token": access_token, "token_type": "bearer"})
