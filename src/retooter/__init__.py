#!/usr/bin/env python3


"""Repost Mastodon posts that mention a user."""


__version__ = "0.0.1"


__all__ = [
    "__version__",
    "Retooter",
    "RetooterError",
    "RetooterInvalidApiBaseUrl",
    "RetooterNoAccountNameDefined",
    "RetooterNoAllowedAccountsDefined",
    "RetooterNotAuthenticated",
    "RetooterInvalidOrMissingConfiguration",
]


from .errors import (
    RetooterError,
    RetooterInvalidApiBaseUrl,
    RetooterNoAccountNameDefined,
    RetooterNoAllowedAccountsDefined,
    RetooterNotAuthenticated,
    RetooterInvalidOrMissingConfiguration,
)
from .retooter import Retooter
