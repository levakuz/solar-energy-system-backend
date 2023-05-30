from src.accounts.models import Account as AccountDatabaseModel
from src.accounts.domain import Account as AccountDomainModel
from src.core.repository import TortoiseRepository


class AccountRepository(TortoiseRepository):
    def __init__(self, model=AccountDatabaseModel, domain=AccountDomainModel):
        super().__int__(model=model, domain=domain)

