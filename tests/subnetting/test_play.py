from test_game import FakeClient

from subnetting.game import Game


def test_summary():
    get_text = (
        '<span id="MainContent_lblSummary" class="bigger">Total Questions: 1<br /> '
        + "Number Correct: 1<br />Number Incorrect: 0<br />TOTAL SCORE: 1<br /></span><br />"
    )

    g = Game(FakeClient(get_text=get_text))

    assert g.play.summary() == [
        ("total questions", 1),
        ("number correct", 1),
        ("number incorrect", 0),
        ("total score", 1),
    ]
