class RequiredError(Exception):
    pass


class OrderError(Exception):
    """This class is raised when an order is submitted that does not have the proper formatting
    """

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


class AuthError(Exception):
    """Class for notifying user that some endpoints are for brokerage accounts only, must use live credentials
    """

    pass
