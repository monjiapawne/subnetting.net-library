import re
from typing import NamedTuple


class Token(NamedTuple):
    value: str
    ip: bool = False
    digit: bool = False
    mask: bool = False


def _lex(raw: str) -> list[Token]:
    ips = re.findall(r"[0-9]+(?:\.[0-9]+){3}", raw)
    ip_subnet = re.findall(r"[0-9]+(?:\.[0-9]+){3}/[0-9]{1,2}", raw)
    cidr = re.findall(r"\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}", raw)

    tokens: list[Token] = []

    for word in raw.split(" "):
        if word in ip_subnet:
            ip, mask = word.split("/")
            tokens.append(Token(value=ip, ip=True))
            tokens.append(Token(value="/" + mask, mask=True))
        elif word in cidr:
            tokens.append(Token(value="/" + word, mask=True))
        elif word in ips:
            tokens.append(Token(value=word, ip=True))
        elif word.isdigit():
            tokens.append(Token(value=word, digit=True))
        else:
            tokens.append(Token(value=word))

    return tokens


_ESC = "\033"
_GR = _ESC + "[32m"
_YW = _ESC + "[31m"
_RESET = _ESC + "[0m"


def highlight(raw: str) -> str:
    s: list[str] = []
    prev_token: Token | None = None
    for t in _lex(raw.rstrip(":")):
        if t.ip:
            # if two ips in a row, it's a mask
            if prev_token and prev_token.ip:
                s.append(_YW + t.value + _RESET)
            else:
                s.append(_GR + t.value + _RESET)
        elif t.mask:
            s.append(_YW + t.value + _RESET)
        elif t.digit:
            s.append(_GR + t.value + _RESET)
        else:
            s.append(t.value)
        prev_token = t

    return " ".join(s) + ":"


def dict_table(dict: dict[str, str]) -> str:
    padding = 5
    max_key_len = max(len(k) for k in dict.keys()) + padding
    return "\n".join([f"{k:<{max_key_len}}{v}" for k, v in dict.items()])


def named_tuple_table(obj: list[any]) -> str:
    if not obj:
        return ""

    if hasattr(obj[0], "_fields"):  # Works for NamedTuples
        headers = list(obj[0]._fields)

    res = ["\t".join(headers)]

    for item in obj:
        row_vals = [str(getattr(item, field, "")) for field in headers]
        res.append("\t".join(row_vals))

    return "\n".join(res)
