from bs4 import BeautifulSoup

from subnetting.models import Match, Round


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
