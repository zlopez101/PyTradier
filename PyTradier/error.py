class RequiredError(Exception):
    pass


class OrderError(Exception):
    pass


class MultiLegKeyWordError(Exception):
    "This class is raised when the dictionar passed to multileg method doesn't have proper keys or values"
    pass


class WatchListError(Exception):
    pass
