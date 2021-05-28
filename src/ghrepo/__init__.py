"""
Parse GitHub repository URLs & specifiers

Visit <https://github.com/jwodder/ghrepo> for more information.
"""

__version__ = "0.1.0.dev1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "ghrepo@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/ghrepo"

from os import PathLike
import re
import subprocess
from typing import Callable, NamedTuple, Optional, Union

AnyPath = Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]

#: Regular expression for a valid GitHub username or organization name.  As of
#: 2017-07-23, trying to sign up to GitHub with an invalid username or create
#: an organization with an invalid name gives the message "Username may only
#: contain alphanumeric characters or single hyphens, and cannot begin or end
#: with a hyphen".  Additionally, trying to create a user named "none" (case
#: insensitive) gives the message "Username name 'none' is a reserved word."
#:
#: Unfortunately, there are a number of users who made accounts before the
#: current name restrictions were put in place, and so this regex also needs to
#: accept names that contain underscores, contain multiple consecutive hyphens,
#: begin with a hyphen, and/or end with a hyphen.
GH_USER_RGX = r"(?![Nn][Oo][Nn][Ee]($|[^-A-Za-z0-9]))[-_A-Za-z0-9]+"

#: Regular expression for a valid GitHub repository name.  Testing as of
#: 2017-05-21 indicates that repository names can be composed of alphanumeric
#: ASCII characters, hyphens, periods, and/or underscores, with the names ``.``
#: and ``..`` being reserved and names ending with ``.git`` forbidden.
GH_REPO_RGX = r"(?:\.?[-A-Za-z0-9_][-A-Za-z0-9_.]*|\.\.[-A-Za-z0-9_.]+)(?<!\.git)"

OWNER_REPO_RGX = re.compile(fr"(?:(?P<owner>{GH_USER_RGX})/)?(?P<name>{GH_REPO_RGX})")

GITHUB_REPO_RGX = re.compile(
    fr"""
    (?:
        (?:https?://)?(?:(?:www\.)?github\.com/|api\.github\.com/repos/)
        |git(?:://github\.com/|@github\.com:)
    )
    (?P<owner>{GH_USER_RGX})/(?P<name>{GH_REPO_RGX})(?:\.git)?/?
""",
    flags=re.X,
)


class GHRepo(NamedTuple):
    owner: str
    name: str

    def __str__(self) -> str:
        return self.fullname

    @property
    def fullname(self) -> str:
        return f"{self.owner}/{self.name}"

    @classmethod
    def parse(
        cls,
        spec: str,
        default_owner: Optional[Union[str, Callable[[], str]]] = None,
    ) -> "GHRepo":
        m = OWNER_REPO_RGX.fullmatch(spec)
        if m:
            owner = m["owner"]
            if owner is None:
                # <https://github.com/python/typeshed/issues/5546>
                if default_owner is None:  # type: ignore[unreachable]
                    raise ValueError(f"No owner given in {spec!r}")
                elif callable(default_owner):
                    owner = default_owner()
                else:
                    owner = default_owner
            name = m["name"]
            assert name is not None
            return cls(owner=owner, name=name)
        else:
            return cls.parse_url(spec)

    @classmethod
    def parse_url(cls, url: str) -> "GHRepo":
        # cf. the giturlparse library
        m = GITHUB_REPO_RGX.fullmatch(url)
        if m:
            return cls(owner=m["owner"], name=m["name"])
        else:
            raise ValueError(f"Invalid GitHub URL: {url!r}")


def get_local_repo(dirpath: Optional[AnyPath] = None, remote: str = "origin") -> GHRepo:
    r = subprocess.run(
        ["git", "remote", "get-url", remote],
        cwd=dirpath,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        check=True,
    )
    return GHRepo.parse_url(r.stdout.strip())
