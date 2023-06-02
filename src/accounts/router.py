from typing import Annotated

import fastapi
from fastapi import Depends
from starlette.responses import JSONResponse

from src.accounts import services
from src.accounts.domain import Account, UserAccount, CompanyAccount
from src.accounts.exceptions import UserDoesNotExistsException
from src.accounts.schemas import UserRegistrationSchema, AccountSchema, UserAccountSchema, CompanyRegistrationSchema, \
    CompanyAccountSchema
from src.accounts.services import register_account
from src.auth.services import get_current_active_user
from src.core.repository import AbstractRepository, TortoiseRepository
from src.core.repository_factory import RepositoryFactory

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
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=Account,
                type_repository=TortoiseRepository
            ))
        ],
        user_account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=UserAccount,
                type_repository=TortoiseRepository
            ))
        ]
):
    return await register_account(
        form_data.email,
        form_data.password,
        account_repository,
        user_account_repository,
        first_name=form_data.first_name,
        last_name=form_data.last_name
    )


@account_router.delete(
    '/{id}',
    response_model=AccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Account']
)
async def delete_account(
        id: int,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=Account,
                type_repository=TortoiseRepository
            ))
        ],

):
    try:
        return await services.delete_account(id=id, account_repository=account_repository)
    except UserDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.put(
    '/user/{id}',
    response_model=UserAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['User']
)
async def update_user_account(
        id: int,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=UserAccount,
                type_repository=TortoiseRepository
            ))
        ],
        account: UserAccountSchema

):
    try:
        return await account_repository.update(account_id=id, update_object=account)
    except UserDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.get(
    '/user/{id}',
    response_model=UserAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['User']
)
async def get_user_account(
        id: int,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=UserAccount,
                type_repository=TortoiseRepository
            ))
        ],

):
    try:
        user_account = await account_repository.get(account_id=id)
        return user_account
    except UserDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.post("/company/", response_model=Account, tags=['Company'])
async def create_company(
        form_data: CompanyRegistrationSchema,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=Account,
                type_repository=TortoiseRepository
            ))
        ],
        company_account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=CompanyAccount,
                type_repository=TortoiseRepository
            ))
        ]
):
    return await register_account(
        form_data.email,
        form_data.password,
        account_repository,
        company_account_repository,
        name=form_data.name
    )


@account_router.get(
    '/company/{id}',
    response_model=CompanyAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Company']
)
async def get_company_account(
        id: int,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=CompanyAccount,
                type_repository=TortoiseRepository
            ))
        ],

):
    try:
        return await account_repository.get(account_id=id)
    except UserDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})


@account_router.put(
    '/company/{id}',
    response_model=CompanyAccountSchema,
    dependencies=[Depends(get_current_active_user)],
    tags=['Company']
)
async def get_company_account(
        id: int,
        account_repository: Annotated[
            AbstractRepository,
            Depends(RepositoryFactory(
                domain_model=CompanyAccount,
                type_repository=TortoiseRepository
            ))
        ],
        company_account: CompanyAccountSchema
):
    try:
        return await account_repository.update(account_id=id, update_object=company_account)
    except UserDoesNotExistsException as e:
        return JSONResponse(status_code=404, content={'detail': e.message})
