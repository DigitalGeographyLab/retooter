#!/usr/bin/env python3


"""Exceptions used in Retooter."""


__all__ = [
    "RetooterError",
    "RetooterInvalidApiBaseUrl",
    "RetooterInvalidOrMissingConfiguration",
    "RetooterNoAccountNameDefined",
    "RetooterNoAllowedAccountsDefined",
    "RetooterNotAuthenticated",
]


class RetooterError(RuntimeError):
    """Base class for errors happening here."""


class RetooterInvalidOrMissingConfiguration(RetooterError):
    """Generic error for missing configuration."""


class RetooterInvalidApiBaseUrl(RetooterInvalidOrMissingConfiguration):
    """Raised if the supplied API base URL is invalid."""


class RetooterNoAccountNameDefined(RetooterInvalidOrMissingConfiguration):
    """Raised if not account name defined."""


class RetooterNoAllowedAccountsDefined(RetooterInvalidOrMissingConfiguration):
    """Raised if allowed accounts are not defined."""


class RetooterNotAuthenticated(RetooterError):
    """Raised if authentication not sufficient."""
