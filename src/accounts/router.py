from typing import Annotated

import fastapi
from fastapi import Depends

from src.accounts.domain import Account
from src.auth.services import get_current_active_user

account_router = fastapi.routing.APIRouter(
    dependencies=[Depends(get_current_active_user)],
    prefix='/accounts'
)


@account_router.get("/me/", response_model=Account)
async def read_users_me(
        current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user
