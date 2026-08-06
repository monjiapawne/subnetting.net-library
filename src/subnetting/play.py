from typing import Any

from bs4 import BeautifulSoup

from .base import Endpoint
from .client import Client
from .errors import ParseError
from .models import Match, Round


class PlayAPI(Endpoint):
    def __init__(self, client: Client):
        super().__init__(client)
        self.round: Round | None = None
        self.match: Match | None = None

    def __iter__(self):
        """Loads the game page, updating the round and match attributes"""
        while True:
            resp = self._client.get("Subnetting")
            soup = BeautifulSoup(resp.text, "html.parser")
            self.round = parse_round(soup)
            self.match = parse_match(soup)

            if self.match.time_remaining <= 0:
                return

            yield self.round

    def __enter__(self):
        """Start the subnetting game"""
        self.start()
        return self

    def __exit__(self, _exc_type: Any, _exc_value: Any, _traceback: Any):
        """end game when implemented"""

    def start(self):
        self._client.post_form("Start")

    def submit(self, answers: list) -> bool:
        """Submit submits the answers provided.

        Returns true if correct, false if incorrect.
        """
        # Submit the answers
        b = "ctl00$MainContent$"
        data = {
            b + "hdnTimeRemaining": self.match.time_remaining,
            b + "txtFirstString": answers[0],
        }
        if len(answers) == 2:
            data[b + "txtSecondString"] = answers[1]
        resp = self._client.post_form("Subnetting", data, "ctl00$MainContent$btnSubmit")

        # Check the answer from the response
        soup = BeautifulSoup(resp.text, "html.parser")
        result = soup.find("span", {"id": "MainContent_label"})
        return result and result.text.strip().lower() == "correct"

    def summary(self) -> list[tuple[str, str]]:
        soup = BeautifulSoup(self._client.get("Summary").text, "html.parser")
        summary = soup.find("span", {"id": "MainContent_lblSummary"})
        if not summary.text:
            raise ParseError("MainContent_lblSummary")

        results = []
        for r in summary.get_text(strip=True, separator="\n").splitlines():
            f = r.split(":")
            if len(f) != 2:
                raise ParseError("Two fields in MainContent_lblSummary")
            r, v = f
            results.append((r.strip().lower(), int(v.strip())))

        return results


def parse_round(soup: BeautifulSoup) -> Round:
    # Find the question
    q = soup.find("span", id="MainContent_QuestionArea")
    question = " ".join(q.text.split()) if q else "no question area in page"

    # Try to get prompts (multi answer questions only)
    prompts = [t.rstrip(":") for s in soup.select("#MainContent_lblOne, #MainContent_lblTwo") if (t := s.text.strip())]

    return Round(question, prompts or ["Answer"])


def parse_match(soup: BeautifulSoup) -> Match:
    tag = soup.find("span", {"id": "MainContent_lblRunningTotal"})
    score = tag.text.strip() if tag else "0/0 Unknown"

    time_remaining = 0
    if countdown := soup.find("input", id="hdnTimeRemaining"):
        v = countdown.get("value")
        if isinstance(v, str):
            time_remaining = float(v)

    return Match(score, time_remaining)
