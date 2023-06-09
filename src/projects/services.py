from datetime import datetime, timedelta

from src.accounts.domain import Account, UserAccount
from src.accounts.models import UserAccountType
from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_types.domain import DeviceType
from src.devices.domain import Device
from src.location_weather.domain import LocationWeather
from src.locations.domain import Location
from src.projects.domain import Project
from src.projects.exceptions import ProjectDoesNotExistsException, ProjectLimitForAccountExceededException
from src.projects.schemas import ProjectCreateUpdateSchema
from src.reports.domain import Report
from src.reports.services import ReportServices


class ProjectServices:

    @classmethod
    async def schedule_report_creation_for_30_days(
            cls,
            project: Project,
            current_user: Account,
            report_uow: AbstractUnitOfWork[Report],
            location_uow: AbstractUnitOfWork[Location],
            location_weather_uow: AbstractUnitOfWork[LocationWeather],
            device_uow: AbstractUnitOfWork[Device],
            device_type_uow: AbstractUnitOfWork[DeviceType],
            device_energies_uow: AbstractUnitOfWork[DeviceEnergy],
            project_uow: AbstractUnitOfWork[Project]
    ):
        date_from = datetime.now()
        date_from = date_from.replace(minute=0, second=0, microsecond=0)
        date_to = date_from + timedelta(days=30)
        await ReportServices.schedule_report_creation(
            date_from=date_from,
            date_to=date_to,
            report_uow=report_uow,
            project=project,
            current_user=current_user,
            location_uow=location_uow,
            location_weather_uow=location_weather_uow,
            device_uow=device_uow,
            device_type_uow=device_type_uow,
            device_energies_uow=device_energies_uow,
            project_uow=project_uow
        )

    @classmethod
    async def try_to_create_project(
            cls,
            project_uow: AbstractUnitOfWork[Project],
            user_account_uow: AbstractUnitOfWork[UserAccount],
            project: ProjectCreateUpdateSchema,
            current_user: Account,
    ) -> Project:
        user_account = await user_account_uow.get(account_id=current_user.id)
        if user_account.type == UserAccountType.free:
            user_projects = await project_uow.list(account_id=current_user.id)
            if len(user_projects) > 0:
                raise ProjectLimitForAccountExceededException
        return await project_uow.add(**project.dict())

