from subnetting import AspClient, Game, SubnettingError

from .config import credentials, session_
from .helpers import ask
from .render import highlight

# TODO: auth: cache login
# TODO: play: __exit__()


def main():
    _ = session_()
    with Game(AspClient()) as game:
        game.auth.login(*credentials())
        # raise SystemExit()
        # print(dict_table(game.account.stats()))
        # print(named_tuple_table(game.account.history()))

        with game.play as match:
            for round in match:
                print(game.match)
                print(highlight(round.question))

                correct = game.play.submit(ask(round.prompts))
                if correct:
                    print("Correct!")
                else:
                    print("Incorrect!")

                input("[Enter for next question]")
                break

    print("\n".join(f"{r[0]}: {r[1]}" for r in game.results))


def run():
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit()
    except SubnettingError as e:
        raise SystemExit(f"error: {e}")


if __name__ == "__main__":
    run()
