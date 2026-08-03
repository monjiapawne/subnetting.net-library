class SubnettingError(Exception):
    """Base subnetting error"""


class OperationFailed(SubnettingError):
    """Operation was unsuccessful

    This could be: logging, logging out, etc.
    """


class LoginRequired(SubnettingError):
    def __init__(self, resource_name: str):
        super().__init__(f"login is required for resource: {resource_name}")


class ParseError(SubnettingError):
    def __init__(self, target: str) -> None:
        super().__init__(f"could not find {target} in page")
