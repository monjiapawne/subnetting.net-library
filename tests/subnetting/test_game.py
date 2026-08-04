from subnetting.client import Response


class FakeClient:
    def __init__(self, get_text: str = "", get_status_code: int = 200, post_text: str = "", post_status_code: int = 200):
        self.get_resp = {
            "text": get_text,
            "status_code": get_status_code,
        }
        self.post_resp = (
            {
                "text": post_text,
                "status_code": post_status_code,
            },
        )

    def get(self, path: str) -> Response:
        return Response(**self.get_resp)

    def post_form(self, path: str, fields: dict | None = None, event_target: str = "") -> Response:
        return Response(**self.post_resp)

    def close(self) -> None: ...
