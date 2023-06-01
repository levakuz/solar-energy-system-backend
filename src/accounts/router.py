from typing import Annotated

import fastapi
from fastapi import Depends

from src.accounts.domain import Account, CompanyAccount, UserAccount
from src.accounts.schemas import CompanyRegistrationSchema, UserRegistrationSchema
from src.accounts.services import register_account
from src.auth.schemas import LoginData, Token
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


@account_router.post("/register/user", response_model=Account)
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


@account_router.post("/register/company", response_model=Account)
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