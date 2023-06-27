class ReportDoesNotExistsException(Exception):
    message = "Report does not exist"

    def __str__(self):
        return ReportDoesNotExistsException.message


class GenerateReportForInactiveProjectException(Exception):
    message = "Cannot generate report for inactive project"

    def __str__(self):
        return GenerateReportForInactiveProjectException.message


class GenerateReportNotWithinYearException(Exception):
    message = "Cannot generate report for date range more than a year"

    def __str__(self):
        return GenerateReportNotWithinYearException.message
