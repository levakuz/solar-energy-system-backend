from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.accounts import services
from src.accounts.domain import Account
from src.accounts.exceptions import (
    AccountDoesNotExistsException,
    CompanyWithNameAlreadyExistsException
)
from src.accounts.models import AccountRole
from src.accounts.schemas import (
    UserRegistrationSchema,
    AccountSchema,
    UserAccountSchema,
    CompanyRegistrationSchema,
    CompanyAccountSchema
)
from src.accounts.unit_of_work import (
    UserAccountUnitOfWork,
    CompanyAccountUnitOfWork,
    AccountUnitOfWork
)
from src.auth.services import get_current_active_user
from src.core.unit_of_work import AbstractUnitOfWork

account_router = fastapi.routing.APIRouter(
    prefix='/accounts'
)


@account_router.get("/me/", response_model=Account)
async def read_users_me(
        current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user


@account_router.post("/user/", response_model=Account, tags=['User'])
async def create_user(
        form_data: UserRegistrationSchema,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(AccountUnitOfWork)
        ],
        user_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(UserAccountUnitOfWork)
        ],
):
    return await services.register_account(
        account_uow=account_uow,
        child_account_uow=user_account_uow,
        role=AccountRole.USER,
        **form_data.dict(),
    )


@account_router.delete(
    '/{id}',
    response_model=AccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Account']
)
async def delete_account(
        id: int,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(AccountUnitOfWork)
        ],
):
    try:
        return await services.mark_account_as_inactive(id=id, account_uow=account_uow)
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.put(
    '/user/{id}',
    response_model=UserAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['User']
)
async def update_user_account(
        id: int,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(UserAccountUnitOfWork)
        ],
        account: UserAccountSchema

):
    try:
        return await account_uow.update(account_id=id, update_object=account)
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.get(
    '/user/{id}',
    response_model=UserAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['User']
)
async def get_user_account(
        id: int,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(UserAccountUnitOfWork)
        ],
):
    try:
        user_account = await account_uow.get(account_id=id)
        return user_account
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.post("/company/", response_model=Account, tags=['Company'])
async def create_company(
        form_data: CompanyRegistrationSchema,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(AccountUnitOfWork)
        ],
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(CompanyAccountUnitOfWork)
        ],
):
    try:
        return await services.register_account(
            role=AccountRole.COMPANY,
            account_uow=account_uow,
            child_account_uow=company_account_uow,
            **form_data.dict()
        )
    except CompanyWithNameAlreadyExistsException as e:
        return JSONResponse(status_code=400, content={'detail': e.message})


@account_router.get(
    '/company/{id}',
    response_model=CompanyAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Company']
)
async def get_company_account(
        id: int,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(CompanyAccountUnitOfWork)
        ],
):
    try:
        return await company_account_uow.get(account_id=id)
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.put(
    '/company/{id}',
    response_model=CompanyAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Company']
)
async def update_company_account(
        id: int,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(CompanyAccountUnitOfWork)
        ],
        company_account: CompanyAccountSchema
):
    try:
        return await company_account_uow.update(account_id=id, update_object=company_account)
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})
    except CompanyWithNameAlreadyExistsException as e:
        return JSONResponse(status_code=400, content={'detail': e.message})
