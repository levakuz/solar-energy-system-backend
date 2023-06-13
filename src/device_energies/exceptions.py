class DeviceEnergyDoesNotExistsException(Exception):
    message = "Device energy does not exist"

    def __str__(self):
        return DeviceEnergyDoesNotExistsException.message
