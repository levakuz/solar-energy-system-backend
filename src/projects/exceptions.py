class ProjectDoesNotExistsException(Exception):
    message = "Project does not exist"

    def __str__(self):
        return ProjectDoesNotExistsException.message


class ProjectLimitForAccountExceededException(Exception):
    message = "Number of projects exceeded for this type of account"

    def __str__(self):
        return ProjectLimitForAccountExceededException.message
