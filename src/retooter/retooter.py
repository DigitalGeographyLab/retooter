#!/usr/bin/env python3


"""Repost Mastodon posts that mention a user."""


import functools
import os
import pathlib
import warnings

import mastodon


__all__ = ["Retooter", "RetooterError"]


# variable and secret names
ACCESS_TOKEN = "ACCESS_TOKEN"
ACCOUNT_NAME = "RETOOTER_ACCOUNT_NAME"
ALLOWED_ACCOUNTS = "RETOOTER_ALLOWED_ACCOUNTS"
API_BASE_URL = "RETOOTER_API_BASE_URL"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
DRY_RUN = "RETOOTER_DRY_RUN"


SINCE_ID_CACHE_FILE = pathlib.Path("since_id")


class RetooterError(RuntimeError):
    "Base class for errors happening here." ""


class RetooterNoAccountNameDefined(RetooterError):
    """Raised if not accout name defined."""


class RetooterNotAuthenticated(RetooterError):
    """Raised if authentication not sufficient."""


class Retooter:
    """Repost Mastodon posts that mention a user."""

    APPLICATION_NAME = "Retooter"

    DRY_RUN = bool(
        DRY_RUN in os.environ
        and os.environ[DRY_RUN].lower() in ("true", "t", "yes", "y")
    )

    def __init__(self):
        """Repost Mastodon posts that mention a user."""
        try:
            self.authenticate()
        except RetooterNoAccountNameDefined as exception:
            raise RetooterError(f"Make sure {ACCOUNT_NAME} is defined.") from exception

    def authenticate(self):
        """
        Reads env vars and tries to authenticate against the API.

        Returns
        =======
        tuple(str, str, str) : client_id, client_secret, access_token
        """
        try:
            try:
                self.mastodon = mastodon.Mastodon(
                    access_token=os.environ["ACCESS_TOKEN"],
                    api_base_url=self.api_base_url,
                    client_id=os.environ["CLIENT_ID"],
                    client_secret=os.environ["CLIENT_SECRET"],
                )
            except KeyError as exception:
                raise RetooterNotAuthenticated from exception

            try:
                self.mastodon.app_verify_credentials()
            except mastodon.errors.MastodonUnauthorizedError as exception:
                raise RetooterNotAuthenticated from exception

        except RetooterNotAuthenticated:
            if "GITHUB_ACTIONS" in os.environ:
                raise RetooterError(
                    "No sufficient authentication found, please follow the "
                    "instructions in README.md to obtain CLIENT_ID, "
                    "CLIENT_SECRET, and ACCESS_TOKEN"
                )
            else:
                print(
                    "No sufficient authentication found, requesting a new "
                    "access token from the API."
                )
                client_id, client_secret = mastodon.Mastodon.create_app(
                    self.APPLICATION_NAME,
                    api_base_url=self.api_base_url,
                )
                self.mastodon = mastodon.Mastodon(
                    api_base_url=self.api_base_url,
                    client_id=client_id,
                    client_secret=client_secret,
                )
                auth_url = self.mastodon.auth_request_url()
                auth_code = input(
                    f"Visit {auth_url}, authenticate with your credentials, "
                    "and copy-and-paste the returned authentication code here:"
                )
                access_token = self.mastodon.log_in(code=auth_code)

                print(
                    "You find the new secrets below, please follow the "
                    "instructions in README.md to define them in your GitHub "
                    "actions environment."
                )
                print(
                    "\n"
                    f"{CLIENT_ID}: {client_id}\n"
                    f"{CLIENT_SECRET}: {client_secret}\n"
                    f"{ACCESS_TOKEN}: {access_token}\n"
                )
                exit(0)

    @functools.cached_property
    def account_name(self):
        try:
            account_name = os.environ[ACCOUNT_NAME]
        except KeyError as exception:
            raise RetooterNoAccountNameDefined from exception
        return account_name

    @functools.cached_property
    def allowed_accounts(self):
        try:
            allowed_accounts = os.environ[ALLOWED_ACCOUNTS].splitlines()
        except KeyError:
            warnings.warn(f"No {ALLOWED_ACCOUNTS} found, check configuration")
            allowed_accounts = []
        return allowed_accounts

    @functools.cached_property
    def api_base_url(self):
        if API_BASE_URL in os.environ and os.environ[API_BASE_URL]:
            api_base_url = os.environ[API_BASE_URL]
        else:
            api_base_url = f"https://{self.account_name.split('@')[-1]}"
        return api_base_url

    def retoot(self):
        """Repost Mastodon posts that mention a user."""
        for mention in self.mentions:
            retooters = [
                retooter["acct"]
                for retooter in self.mastodon.status_reblogged_by(
                    mention["status"]["id"]
                )
            ]
            if (
                self.account_name not in retooters
                and self.account_name.split('@')[0] not in retooters
            ):
                if self.DRY_RUN:
                    print(
                        f"{DRY_RUN} is set, not actually re-posting. \n"
                        f"Would now repost {mention['status']['id']} "
                        f"by {mention['status']['account']['acct']}."
                    )
                else:
                    print(
                        f"Reposting {mention['status']['id']} "
                        f"by {mention['status']['account']['acct']}."
                    )
                    self.mastodon.status_reblog(mention["status"]["id"])
                    self.since_id = mention["status"]["id"]

    @property
    def mentions(self):
        """Posts the account has been mentioned (after self.since_id)."""
        mentions = self.mastodon.notifications(
            mentions_only=True,
            since_id=self.since_id,
        )
        for mention in mentions:
            if mention["status"]["account"]["acct"] in self.allowed_accounts:
                yield mention

    @property
    def since_id(self):
        """Try to read a cached since_id."""
        try:
            since_id = self._since_id
        except AttributeError:
            try:
                since_id = int(SINCE_ID_CACHE_FILE.read_text())
                self._since_id = since_id
            except (FileNotFoundError, ValueError):
                since_id = None
        return since_id

    @since_id.setter
    def since_id(self, since_id):
        if since_id is not None:
            self._since_id = since_id
            SINCE_ID_CACHE_FILE.write_text(str(since_id))
