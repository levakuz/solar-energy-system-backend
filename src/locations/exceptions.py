class LocationDoesNotExistsException(Exception):
    message = "Location does not exist"

    def __str__(self):
        return LocationDoesNotExistsException.message


class GeocodingNotFoundException(Exception):
    message = "Location not found"

    def __str__(self):
        return GeocodingNotFoundException.message
