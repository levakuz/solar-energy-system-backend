class DeviceTypeDoesNotExistsException(Exception):
    message = "Device type does not exist"

    def __str__(self):
        return DeviceTypeDoesNotExistsException.message
