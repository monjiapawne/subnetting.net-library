import unicodedata
from datetime import datetime
from typing import NamedTuple

from bs4 import BeautifulSoup

from .auth import requires_login
from .base import Endpoint


class HistoryEntry(NamedTuple):
    score: str
    questions: str
    correct: str
    date: datetime


class AccountAPI(Endpoint):
    @requires_login
    def stats(self) -> dict[str, str]:
        """Pull account stats, returns a dictionary of field:value"""
        r = self._client.get("Account/Profile")
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", class_="tabformat")

        stats: dict[str, str] = {}
        for row in table.find_all("tr"):
            tds = [tds.text for tds in row.find_all("td", limit=2)]
            if len(tds) != 2:
                # skip malformed
                continue
            k, v = tds
            stats[k] = v

        return stats

    @requires_login
    def history(self) -> list[HistoryEntry]:
        # TODO: still being parsed wrong
        r = self._client.get("Account/Profile")
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", id="BottomContent_gvHistory")

        headings = [th.text.lower() for th in table.find("tr") if th.text.strip()]

        history: list[HistoryEntry] = list()
        for tr in table.find_all("tr")[1:]:
            # need safety
            cells = [unicodedata.normalize("NFKC", td.text).strip() for td in tr.find_all("td")]

            # 11/26/2024 01:58:04
            raw_date = cells[headings.index("date/time (utc)")]
            if raw_date:
                date = datetime.strptime(raw_date.strip(), "%m/%d/%Y %H:%M:%S")

            history.append(
                HistoryEntry(
                    score=tr.text[headings.index("score")],
                    questions=tr.text[headings.index("questions")],
                    correct=tr.text[headings.index("correct")],
                    date=date,
                )
            )

        return history
