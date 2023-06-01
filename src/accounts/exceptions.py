class UserDoesNotExistsException(Exception):
    message = "User does not exist"

    def __str__(self):
        return UserDoesNotExistsException.message


class InactiveUserException(Exception):
    message = "Inactive user"

    def __str__(self):
        return InactiveUserException.message