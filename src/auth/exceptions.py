class InvalidCredentialsException(Exception):
    message = "Invalid credentials were provided"

    def __str__(self):
        return InvalidCredentialsException.message
