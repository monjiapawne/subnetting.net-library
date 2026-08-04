from bs4 import BeautifulSoup
from test_game import FakeClient

from subnetting.game import Game
from subnetting.models import Match
from subnetting.play import parse_match, parse_round


def test_summary():
    get_resp = (
        '<span id="MainContent_lblSummary" class="bigger">Total Questions: 1<br /> '
        + "Number Correct: 1<br />Number Incorrect: 0<br />TOTAL SCORE: 1<br /></span><br />"
    )

    g = Game(FakeClient(get_resp=get_resp))

    assert g.play.summary() == [
        ("total questions", 1),
        ("number correct", 1),
        ("number incorrect", 0),
        ("total score", 1),
    ]


def test_submit_correct():
    g = Game(FakeClient(post_resp='<span id="MainContent_label">Correct</span>'))
    g.play.match = Match("1/1", 1.1)
    assert g.play.submit(["test"])


def test_submit_incorrect():
    g = Game(FakeClient(post_resp='<span id="MainContent_label"></span>'))
    g.play.match = Match("1/1", 1.1)
    assert not g.play.submit(["test"])


def test_parse_round_two_questions():
    soup = BeautifulSoup(
        '<span id="MainContent_QuestionArea">question 1</span>'
        + '<span id="MainContent_lblOne">answer prompt 1</span>'
        + '<span id="MainContent_lblTwo">answer prompt 2</span>',
        "html.parser",
    )

    round = parse_round(soup)

    assert round.question == "question 1"
    assert len(round.prompts) == 2
    assert round.prompts[0] == "answer prompt 1"
    assert round.prompts[1] == "answer prompt 2"


def test_parse_round_one_questions():
    soup = BeautifulSoup(
        '<span id="MainContent_QuestionArea">question 1</span>' + '<span id="MainContent_lblOne"></span>',
        "html.parser",
    )

    round = parse_round(soup)

    assert round.question == "question 1"
    assert len(round.prompts) == 1
    assert round.prompts[0] == "Answer"


def test_parse_match():
    soup = BeautifulSoup(
        '<span id="MainContent_lblRunningTotal">0/1 Correct</span> '
        + '<input id="hdnTimeRemaining" name="ctl00$MainContent$hdnTimeRemaining" type="hidden" value="299.6"/>',
        "html.parser",
    )

    round = parse_match(soup)

    assert round.time_remaining == 299.6
    assert round.score == "0/1 Correct"
