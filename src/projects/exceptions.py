class ProjectDoesNotExistsException(Exception):
    message = "Project does not exist"

    def __str__(self):
        return ProjectDoesNotExistsException.message
