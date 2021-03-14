class RequiredError(Exception):
    pass


class OrderError(Exception):
    pass


class MultiLegKeyWordError(Exception):
    "This class is raised when the dictionar passed to multileg method doesn't have proper keys or values"
    pass


class WatchListError(Exception):
    pass


class RequestError(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
