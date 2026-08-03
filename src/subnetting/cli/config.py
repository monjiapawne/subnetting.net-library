import os

import requests
import urllib3


def credentials() -> tuple[str, str]:
    try:
        username = os.environ["SNG_USERNAME"]
        password = os.environ["SNG_PASSWORD"]
    except KeyError as e:
        raise SystemExit(f"missing environment variables: {e}") from None
    return username, password


def session_(
    http: str = "http://127.0.0.1:8080",
    https: str = "http://127.0.0.1:8080",
    verify: bool = False,
) -> requests.Session:
    s = requests.Session()
    s.proxies.update(
        {
            "http": http,
            "https": https,
        }
    )
    s.verify = verify
    urllib3.disable_warnings()
    return s
