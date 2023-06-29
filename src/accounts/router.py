from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

import src.accounts.services as account_services
from src.accounts.domain import Account, UserAccount
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
    CompanyAccountSchema, UserAccountTypeSchema, CompanyAccountUpdateSchema
)
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


@account_router.get("/me", response_model=AccountSchema, tags=['Accounts'])
async def read_users_me(
        current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user


@account_router.post("/users", response_model=Account, tags=['Users'])
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
    return await account_services.register_account(
        account_uow=account_uow,
        child_account_uow=user_account_uow,
        role=AccountRole.USER,
        **form_data.dict(),
    )


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
        return await account_services.mark_account_as_inactive(id=id, account_uow=account_uow)
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


@account_router.post("/companies", response_model=Account, tags=['Companies'])
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
        return await account_services.register_account(
            role=AccountRole.COMPANY,
            account_uow=account_uow,
            child_account_uow=company_account_uow,
            **form_data.dict()
        )
    except CompanyWithNameAlreadyExistsException as e:
        return JSONResponse(status_code=400, content={'detail': e.message})


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
