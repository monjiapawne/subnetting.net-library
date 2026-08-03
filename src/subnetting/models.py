from dataclasses import dataclass


@dataclass
class Match:
    score: str
    time_remaining: float

    def __str__(self) -> str:
        return f"{self.score} | {self.time_remaining:.0f}s"


@dataclass
class Round:
    question: str
    prompts: list[str]
