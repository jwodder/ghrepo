v0.7.0 (in development)
-----------------------
- Drop support for Python 3.6
- Support Python 3.11
- Properly follow RFC 3986 when parsing username & password fields in
  `www.github.com` URLs
- Correct the accepted format for URLs that start with `ssh://` (They need to
  separate the hostname from the path with a slash rather than a colon)
- Schemes & hostnames in URLs are now parsed case-insensitively

v0.6.0 (2022-07-08)
-------------------
- `get_local_repo()` now raises a dedicated `NoSuchRemoteError` if the given
  remote does not exist
- `get_current_branch()` now raises a dedicated `DetachedHeadError` if the
  repository is in a detached `HEAD` state
- `get_branch_upstream()` now raises a dedicated `NoUpstreamError` if the given
  branch does not have an upstream configured

v0.5.0 (2022-07-06)
-------------------
- Make `get_local_repo()` handle remote names that start with a hyphen
- Add a `get_branch_upstream()` function

v0.4.1 (2022-07-04)
-------------------
- Do not accept repository names that end in "`.git`" with alternate casings

v0.4.0 (2021-11-05)
-------------------
- Support Python 3.10
- Export and document `GH_USER_RGX` and `GH_REPO_RGX`

v0.3.0 (2021-10-03)
-------------------
- `ghrepo` command: If a git invocation fails, exit with the same return code
  as the subprocess
- Error messages from the `ghrepo` command are now prefixed with "ghrepo:"

v0.2.0 (2021-05-29)
-------------------
- `ghrepo` command: Fail more gracefully when the remote URL is invalid

v0.1.0 (2021-05-28)
-------------------
Initial release
