from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.accounts.domain import Account, UserAccount
from src.accounts.exceptions import (
    AccountDoesNotExistsException,
    CompanyWithNameAlreadyExistsException
)
from src.accounts.schemas import (
    AccountSchema,
    UserAccountSchema,
    CompanyAccountSchema, UserAccountTypeSchema, CompanyAccountUpdateSchema
)
from src.accounts.services import AccountServices
from src.accounts.unit_of_work import (
    UserAccountUnitOfWork,
    CompanyAccountUnitOfWork,
    AccountUnitOfWork
)
from src.auth.services import get_current_active_user
from src.core.pagination import Paginator
from src.core.schemas import PaginationRequestSchema, PaginationSchema
from src.core.unit_of_work import AbstractUnitOfWork

account_router = fastapi.routing.APIRouter(
    prefix='/accounts'
)


@account_router.get("/me", response_model=Account)
async def read_users_me(
        current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user


@account_router.delete(
    '/{id}',
    response_model=AccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Accounts']
)
async def delete_account(
        id: int,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(AccountUnitOfWork)
        ],
):
    try:
        return await AccountServices.mark_account_as_inactive(id=id, account_uow=account_uow)
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.put(
    '/users/{id}',
    response_model=UserAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Users']
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
    '/users/{id}',
    response_model=UserAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Users']
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


@account_router.put(
    '/users/{id}/type',
    response_model=UserAccount,
    dependencies=[Depends(get_current_active_user)],
    tags=['Users']
)
async def get_user_account(
        id: int,
        account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(UserAccountUnitOfWork)
        ],
        form_data: UserAccountTypeSchema
):
    try:
        user_account = await account_uow.update(account_id=id, update_object=form_data)
        return user_account
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.get(
    '/companies',
    response_model=PaginationSchema[CompanyAccountSchema],
    dependencies=[Depends(get_current_active_user)],
    tags=['Companies']
)
async def get_list_company_accounts(
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(CompanyAccountUnitOfWork)
        ],
        pagination: Annotated[PaginationRequestSchema, Depends(PaginationRequestSchema)],
):
    companies = await company_account_uow.list(**pagination.dict())
    count = await company_account_uow.count()
    paginator = Paginator[Account](models_list=companies, count=count, **pagination.dict())
    return await paginator.get_response()


@account_router.get(
    '/companies/{id}',
    response_model=CompanyAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Companies']
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
    '/companies/{id}',
    response_model=CompanyAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Companies']
)
async def update_company_account(
        id: int,
        company_account_uow: Annotated[
            AbstractUnitOfWork,
            Depends(CompanyAccountUnitOfWork)
        ],
        company_account: CompanyAccountUpdateSchema
):
    try:
        return await company_account_uow.update(account_id=id, update_object=company_account)
    except AccountDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})
    except CompanyWithNameAlreadyExistsException as e:
        return JSONResponse(status_code=400, content={'detail': e.message})
