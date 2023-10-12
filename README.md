# ‘Retooter’ re-posts Mastodon messages mentioning an account

This is a small Mastodon bot, running on GitHub actions, that re-posts any
‘toots’ by anybody from a list of allowed accounts that mention one configurable
account.

*Retooter* is written in Python and depends on the
[Mastodon.py](https://github.com/halcy/Mastodon.py) package to interact with the
server-side API.


## Configuration

1. [Enable actions for this
   repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
   Limit the actions to ‘Allow [repo-name], and select non-[repo-name], actions
   and reusable workflows’, and check the ‘Allow actions created by GitHub’ box

2. Define some [action
   variables](https://docs.github.com/en/actions/learn-github-actions/variables):
   - `RETOOTER_ACCOUNT_NAME`: set to the account that should retoot when it is
     mentioned. **Omit** the leading `@`, be sure to include the domain name
     (e.g., `digigeolab@mastodon.online`)
   - `RETOOTER_ALLOWED_ACCOUNTS`: a list of accounts, one per line, whose posts
     are re-tooted if they mention `RETOOTER_ACCOUNT_NAME`
   - (optional) `RETOOTER_API_BASE_URL`: if the API base url of the account’s instance
     differs from `https://` + the domain part of the `RETOOTER_ACCOUNT_NAME`
     (e.g., `https://mastodon.online`), define it manually, here
   - (option) `RETOOTER_DRY_RUN`: if this variable is set to `TRUE`, *retooter*
     will not actually re-post any messages, but rather print them to stdout
     (which can be read from the log output of a GitHub action)

3. Create a new set of authentication keys. This is a multi-step process that
   includes running the script *once* locally, or in an interactive environment,
   in which you can copy and paste text from and to the script

   1. Install this project locally, e.g., in a virtual environment

      ```
      pip install git+https://github.com/DigitalGeographyLab/retooter.git
      ```

   2. Locally define the `RETOOTER_ACCOUNT_NAME` (and possibly
      `RETOOTER_API_BASE_URL`( you set above as an environment variable:
      if you use BASH or a similar shell, use `export`:

      ```
      export RETOOTER_ACCOUNT_NAME="digigeolab@mastodon.online"
      export RETOOTER_API_BASE_URL="https://mastodon.online"
      ```

   3. Run the package:

      ```
      python -m retooter
      ```

   4. The script will prompt you to open a web address (on the account‘s
      instance), login and authenticate there, and copy and paste the response
      back to the script.

   5. Then, it will print three variables: `CLIENT_ID`, `CLIENT_SECRET`, and
      `ACCESS_TOKEN`. Copy these and define them as [GitHub action
      secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).
