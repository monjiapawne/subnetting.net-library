import functools

from bs4 import BeautifulSoup

from .base import Endpoint
from .errors import LoginRequired, OperationFailed


def requires_login(method):  # noqa: ANN001, ANN201
    """Single method decorator, checks if client is authenticated, raises LoginRequired if not

    The reason we don't just calling login is to avoid storing login credentials in memory, rather force
    a natural relogin.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        if not self._client._authenticated:
            raise LoginRequired(method.__name__)
        return method(self, *args, **kwargs)

    return wrapper


class AuthAPI(Endpoint):
    def login(self, username: str, password: str) -> None:
        # 1) Get state
        self._client.get("Account/Login")

        # 2) Login
        b = "ctl00$MainContent$LoginUser$"
        self._client.post_form(
            "Account/Login",
            {
                b + "UserName": username,
                b + "Password": password,
                b + "LoginButton": "Log In",
            },
        )

        if not self._logged_in():
            raise OperationFailed

    def _logged_in(self) -> bool:
        r = self._client.get("Account/Profile")
        soup = BeautifulSoup(r.text, "html.parser")

        logged_in = bool(soup.find("a", string="View/Edit Account Information"))
        self._client._authenticated = logged_in

        return logged_in

    @requires_login
    def logout(self):
        """Logout of account"""
        # For whatever reason the empty VIEWSTATEENCRYPTED is required to accept the logut
        self._client.post_form("/Account/Profile", {"__VIEWSTATEENCRYPTED": ""}, "ctl00$lv1$HeadLoginStatus$ctl00")
        if self._logged_in():
            raise OperationFailed()
