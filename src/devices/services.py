from typing import NoReturn

from src.accounts.domain import Account, UserAccount
from src.accounts.models import UserAccountType
from src.core.unit_of_work import AbstractUnitOfWork
from src.devices.domain import Device
from src.devices.exceptions import DeviceLimitForAccountExceededException
from src.devices.schemas import DeviceCreateUpdateSchema
from src.locations.domain import Location
from src.locations.services import try_to_delete_location


class DevicesServices:

    @classmethod
    async def try_to_create_device(
            cls,
            device_uow: AbstractUnitOfWork[Device],
            user_account_uow: AbstractUnitOfWork[UserAccount],
            location_uow: AbstractUnitOfWork[Location],
            current_user: Account,
            device: DeviceCreateUpdateSchema,
    ) -> Device:
        user_account = await user_account_uow.get(account_id=current_user.id)
        if user_account.type == UserAccountType.free:
            user_devices = await device_uow.list(project_id=device.project_id)
            if len(user_devices) >= 3:
                await try_to_delete_location(
                    location_uow=location_uow,
                    location_id=device.location_id
                )
                raise DeviceLimitForAccountExceededException
        return await device_uow.add(**device.dict())

    @classmethod
    async def try_to_delete_device(
            cls,
            device_uow: AbstractUnitOfWork[Device],
            location_uow: AbstractUnitOfWork[Location],
            device_id: int,
    ) -> NoReturn:
        device = await device_uow.get(id=device_id)
        await try_to_delete_location(
            location_uow=location_uow,
            location_id=device.location_id
        )
        device = await device_uow.delete(id=device_id)
