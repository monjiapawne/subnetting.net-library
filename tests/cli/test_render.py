from subnetting.cli.render import Token, _lex


def test_lex_full_string():
    tokens = _lex("example question 1.1.1.1")
    assert len(tokens) == 3
    assert tokens == [
        Token(value="example"),
        Token(value="question"),
        Token(value="1.1.1.1", ip=True),
    ]


def test_lex_ip():
    assert _lex("1.1.1.1") == [Token(value="1.1.1.1", ip=True)]


def test_lex_subnet_ip():
    tokens = _lex("192.168.2.0/24")
    assert tokens == [
        Token(value="192.168.2.0", ip=True),
        Token(value="/24", mask=True),
    ]


def test_lex_digit():
    assert _lex("digit 10199") == [
        Token(value="digit"),
        Token(value="10199", digit=True),
    ]
