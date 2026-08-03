from .client import Client


class Endpoint:
    def __init__(self, client: Client):
        self._client = client
