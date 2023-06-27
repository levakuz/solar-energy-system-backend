class DeviceDoesNotExistsException(Exception):
    message = "Device does not exist"

    def __str__(self):
        return DeviceDoesNotExistsException.message


class DeviceLimitForAccountExceededException(Exception):
    message = "Number of devices exceeded for this type of account"

    def __str__(self):
        return DeviceLimitForAccountExceededException.message