import base64
import uuid
from datetime import datetime, timedelta
from typing import List

import matplotlib.pyplot as plt
from pytz import utc

from src.core.unit_of_work import AbstractUnitOfWork
from src.device_energies.domain import DeviceEnergy
from src.device_energies.exceptions import DeviceEnergyDoesNotExistsException
from src.device_energies.services import calculate_device_energy_based_on_location_weather
from src.device_types.domain import DeviceType
from src.devices.domain import Device
from src.location_weather.domain import LocationWeather
from src.location_weather.services import get_weather_for_date
from src.locations.domain import Location
from src.projects.domain import Project
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
            report_uow: AbstractUnitOfWork[Report],
            project_uow: AbstractUnitOfWork[Project],

    ) -> Report:
        # 1) Get all project devices

        devices = await device_uow.list(project=project_id)
        project = await project_uow.get(id=project_id)
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
                        location_weather = weather_for_location_from_api.get(date.isoformat(), None)
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
        chart_path = f'./src/staticfiles/report_charts/{project.name}_{uuid.uuid4()}.png'
        await cls.create_plot_for_report(
            dates=list(project_energy.keys()),
            energy_values=list(project_energy.values()),
            file_path=chart_path
        )
        return await report_uow.add(
            **ReportGenerateSchema(
                project_id=project_id,
                date_from=date_from,
                date_to=date_to,
                value=total_energy,
                plot_path=chart_path
            ).dict()
        )

    @classmethod
    async def generate_report_template(
            cls,
            image_path: str,
            project_name: str,
            report: Report
    ):

        # Read the temporary file as bytes
        with open(image_path, "rb") as file:
            img_data = file.read()

        # Encode the image data using base64
        encoded_image = base64.b64encode(img_data).decode("utf-8")

        # Format the HTML report
        report = f"""\
        <html>
        <head>
            <style>
                table, th, td {{ border: 1px solid black; border-collapse: collapse; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>{project_name} Electricity Production Report</h2>
            <p>This is to inform you about the electricity production of {project_name} 
            from {report.date_from} to {report.date_to}.</p>
            <p><strong>Electricity Production:</strong> {report.value} kWh</p>
            <p>Below is the graph showing the daily production of electricity:</p>
            <img src="data:image/png;base64,{encoded_image}" alt="Daily Production Graph" style="display: block; margin-left: auto; margin-right: auto/>;
        </body> 
        </html> 
        """

    @classmethod
    async def create_plot_for_report(
            cls,
            dates: List[datetime],
            energy_values: List[int],
            file_path: str
    ):
        # Generate the graph
        plt.figure(figsize=(16, 9))
        plt.plot(dates, energy_values)
        plt.grid(axis='both', alpha=.3)

        plt.xlabel("Date", fontsize=16)
        plt.ylabel("Daily Production (kWh)", fontsize=16)
        plt.title("Daily Production of Electricity", fontsize=16)
        x_ticks = list({datetime(i.year, i.month, i.day) for i in dates})
        x_labels = [i.strftime("%d/%m/%Y") for i in x_ticks]
        plt.xticks(fontsize=16, labels=x_labels, ticks=x_ticks, rotation=60)
        plt.yticks(fontsize=16)

        plt.tight_layout()


        # Save the graph as a temporary file
        tmp_file = file_path  # Replace with a suitable temporary file path
        plt.savefig(tmp_file)
        plt.close()
