from typing import NamedTuple, Protocol, cast
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class Response(NamedTuple):
    text: str
    status_code: int


class Client(Protocol):
    """Interface for subnetting game client"""

    def get(self, path: str) -> Response: ...
    def post_form(self, path: str, fields: dict | None = None, event_target: str = "") -> Response: ...
    def close(self) -> None: ...


class AspClient:
    """AspClient connects to www.subnetting.net's asp.net website"""

    _URL_BASE = "https://www.subnetting.net"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()
        self._asp_state: dict[str, str] = {}
        self._authenticated: bool = False

    def _parse_asp_state(self, html: str) -> None:
        """Reads and stores the asp fields from the html"""
        soup = BeautifulSoup(html, "html.parser")
        for key in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"):
            if element := soup.find("input", {"name": key}):
                self._asp_state[key] = cast(str, element["value"])

    def _request(self, method: str, path: str, data: dict | None = None) -> Response:
        """Generic http request

        Appends ".aspx" to the path
        """
        resp = self._session.request(method, urljoin(self._URL_BASE, path + ".aspx"), data=data)
        resp.raise_for_status()
        self._parse_asp_state(resp.text)
        return Response(resp.text, resp.status_code)

    def get(self, path: str) -> Response:
        return self._request("GET", path)

    def post_form(self, path: str, fields: dict | None = None, event_target: str = "") -> Response:
        data = {
            "__EVENTTARGET": event_target,
            "__EVENTARGUMENT": "",
            **self._asp_state,
            **(fields or {}),
        }
        return self._request("POST", path, data)

    def close(self) -> None:
        self._session.close()
