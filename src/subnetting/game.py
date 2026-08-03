from .account import AccountAPI
from .auth import AuthAPI
from .client import AspClient, Client
from .play import PlayAPI


class Game:
    def __init__(self, client: Client | None = None):
        self._client = client or AspClient()
        self.account = AccountAPI(self._client)
        self.play = PlayAPI(self._client)
        self.auth = AuthAPI(self._client)
        self.results: list[tuple[str, str]] | None = None

    @property
    def round(self):
        return self.play.round

    @property
    def match(self):
        return self.play.match

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):  # noqa: ANN001
        self.results = self.play.summary()
        self._client.close()
