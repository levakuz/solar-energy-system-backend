import uuid
from typing import Annotated, NoReturn, List

from fastapi import Depends
from pydantic import BaseModel
from tortoise.exceptions import DoesNotExist

from src.core.repository import TortoiseRepository, AbstractRepository
from src.core.repository_factory import RepositoryFactory
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_types.domain import DeviceType
from src.device_types.exceptions import DeviceTypeDoesNotExistsException


class DeviceTypeUnitOfWork(AbstractUnitOfWork[DeviceType]):
    def __init__(
            self,
            device_type_repository: Annotated[
                AbstractRepository,
                Depends(RepositoryFactory(
                    domain_model=DeviceType,
                    type_repository=TortoiseRepository
                ))
            ],
    ):
        self._device_type_repository = device_type_repository

    async def get(self, *args, **kwargs) -> DeviceType:
        try:
            return await self._device_type_repository.get(*args, **kwargs)
        except DoesNotExist as e:
            raise DeviceTypeDoesNotExistsException

    async def update(self, update_object: BaseModel, **kwargs) -> DeviceType:
        try:
            await self._device_type_repository.update(update_object=update_object, **kwargs)
            return await self._device_type_repository.get(**kwargs)
        except DoesNotExist as e:
            raise DeviceTypeDoesNotExistsException

    async def add(self, *args, **kwargs) -> DeviceType:
        photo = kwargs.pop('photo')  # type: UploadFile
        file_name = f'{kwargs.get("name")}_{uuid.uuid4()}.png'
        with open(f'./src/staticfiles/device_types_photos/{file_name}', 'wb') as file:
            data = await photo.read()
            file.write(data)
        kwargs['photo'] = file_name
        return await self._device_type_repository.add(*args, **kwargs)

    async def delete(self, *args, **kwargs) -> NoReturn:
        try:
            await self._device_type_repository.delete(*args, **kwargs)
        except DoesNotExist as e:
            raise DeviceTypeDoesNotExistsException

    async def list(self, *args, **kwargs) -> List[DeviceType]:
        return await self._device_type_repository.list(*args, **kwargs)

    async def count(self, *args, **kwargs) -> int:
        return await self._device_type_repository.count(*args, **kwargs)
