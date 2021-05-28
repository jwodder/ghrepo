"""
Parse GitHub repository URLs & specifiers

Visit <https://github.com/jwodder/ghrepo> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'ghrepo@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/ghrepo'

from   os     import PathLike
import re
import subprocess
from   typing import Callable, NamedTuple, Optional, Union

AnyPath = Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]

GH_USER_RGX = r'(?![Nn][Oo][Nn][Ee]($|[^-A-Za-z0-9]))[-_A-Za-z0-9]+'
GH_REPO_RGX = r'(?:\.?[-A-Za-z0-9_][-A-Za-z0-9_.]*|\.\.[-A-Za-z0-9_.]+)'\
              r'(?<!\.git)'

OWNER_REPO_RGX = re.compile(
    fr'(?:(?P<owner>{GH_USER_RGX})/)?(?P<name>{GH_REPO_RGX})'
)

GITHUB_REMOTE_RGX = re.compile(fr'''
    (?:
        (?:https?://)?(?:www\.)?github\.com/
        |git(?:://github\.com/|@github\.com:)
    )
    (?P<owner>{GH_USER_RGX})/(?P<name>{GH_REPO_RGX})(?:\.git)?/?
''', flags=re.X)

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
                if default_owner is None:
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
        m = GITHUB_REMOTE_RGX.fullmatch(url)
        if m:
            return cls(owner=m["owner"], name=m["name"])
        else:
            raise ValueError(f"Invalid GitHub URL: {url!r}")

    @classmethod
    def get_local(cls, chdir: Optional[AnyPath] = None, remote: str = "origin")\
            -> "GHRepo":
        r = subprocess.run(
            ["git", "remote", "get-url", remote],
            cwd=chdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        if r.returncode == 0:
            return cls.parse_url(r.stdout.strip())
        else:
            raise RuntimeError(
                f"Could not determine remote URL: 'git remote get-url {remote}'"
                f" exited with {r.returncode}:\n{r.stderr}"
            )
