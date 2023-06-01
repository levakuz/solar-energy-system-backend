class UserDoesNotExistsException(Exception):
    message = "User does not exist"

    def __str__(self):
        return UserDoesNotExistsException.message


class InactiveUserException(Exception):
    message = "Inactive user"

    def __str__(self):
        return InactiveUserException.message


class AccountWithEmailAlreadyExistsException(Exception):
    message = "Account with provided email already exists"

    def __str__(self):
        return AccountWithEmailAlreadyExistsException.message


class CompanyWithNameAlreadyExistsException(Exception):
    message = "Company with provided name already exists"

    def __str__(self):
        return CompanyWithNameAlreadyExistsException.message
