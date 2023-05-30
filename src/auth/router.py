from datetime import timedelta
from typing import Annotated, Type

import fastapi.routing
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.accounts.domain import Account
from src.accounts.repository import AccountRepository
from src.auth.schemas import Token, LoginData
from src.auth.services import authenticate_user, get_current_active_user, register_user
from src.auth.utils import create_access_token
from src.settings import Settings

router = fastapi.routing.APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(AccountRepository(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token.parse_obj({"access_token": access_token, "token_type": "bearer"})


@router.post("/register", response_model=Token)
async def create_user(
        form_data: LoginData
):
    return await register_user(form_data.email, form_data.password)


@router.get("/users/me/", response_model=Account)
async def read_users_me(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]