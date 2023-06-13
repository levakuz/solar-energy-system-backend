class ReportDoesNotExistsException(Exception):
    message = "Report does not exist"

    def __str__(self):
        return ReportDoesNotExistsException.message
