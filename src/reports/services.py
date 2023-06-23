from datetime import datetime, timedelta

from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.exceptions import DeviceEnergyDoesNotExistsException
from src.device_energies.services import calculate_device_energy_based_on_location_weather
from src.device_types.domain import DeviceType
from src.devices.domain import Device
from src.location_weather.domain import LocationWeather
from src.location_weather.services import get_weather_for_date
from src.locations.domain import Location
from src.reports.domain import Report
from src.reports.schemas import ReportGenerateSchema


class ReportServices:

    @classmethod
    async def generate_report(
            cls,
            date_from: datetime,
            date_to: datetime,
            project_id: int,
            device_uow: AbstractUnitOfWork[Device],
            device_energies_uow: AbstractUnitOfWork[DeviceEnergy],
            location_weather_uow: AbstractUnitOfWork[LocationWeather],
            device_type_uow: AbstractUnitOfWork[DeviceType],
            location_uow: AbstractUnitOfWork[Location],
            report_uow: AbstractUnitOfWork[Report]

    ) -> Report:
        # 1) Get all project devices

        devices = await device_uow.list(project=project_id)

        # 2) Get device locations
        total_energy = 0
        project_energy = {}
        for device in devices:
            date = date_from
            weather_for_location_from_api = {}
            while date <= date_to:
                try:
                    device_energy_at_date = await device_energies_uow.get(device_id=device.id, date=date)
                    device_energy_value = device_energy_at_date.value
                except DeviceEnergyDoesNotExistsException:
                    location = await location_uow.get(id=device.location_id)
                    location_weather = await location_weather_uow.get(location_id=device.location_id, date=date)
                    if not location_weather:
                        if len(weather_for_location_from_api.keys()) == 0:
                            weather_for_location_from_api = await get_weather_for_date(
                                date_from,
                                date_to,
                                location.latitude,
                                location.longitude,
                                location.id
                            )
                        location_weather = weather_for_location_from_api[date.isoformat()]
                    device_energy_value = await calculate_device_energy_based_on_location_weather(
                        device_type=await device_type_uow.get(id=device.device_type_id),
                        location_weather=location_weather
                    )
                    await device_energies_uow.add(
                        value=device_energy_value,
                        device_id=device.id,
                        date=date
                    )
                if date in project_energy.keys():
                    project_energy[date] += device_energy_value
                else:
                    project_energy[date] = device_energy_value
                total_energy += device_energy_value
                date = date + timedelta(hours=1)

        return await report_uow.add(
            **ReportGenerateSchema(
                project_id=project_id,
                date_from=date_from,
                date_to=date_to,
                value=total_energy
            ).dict()
        )
