class DeviceDoesNotExistsException(Exception):
    message = "Device does not exist"

    def __str__(self):
        return DeviceDoesNotExistsException.message
