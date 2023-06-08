class LocationDoesNotExistsException(Exception):
    message = "Location does not exist"

    def __str__(self):
        return LocationDoesNotExistsException.message
