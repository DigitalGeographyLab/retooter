#!/usr/bin/env python3


"""Repost Mastodon posts that mention a user."""


from . import Retooter, RetooterError


def main():
    try:
        retooter = Retooter()
        retooter.retoot()

    except RetooterError as exception:
        print(exception.args[0])
        exit(27)


if __name__ == "__main__":
    main()
