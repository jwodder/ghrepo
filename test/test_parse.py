import pytest
from ghrepo import GHRepo

REPO_URLS = [
    (
        "git://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git://github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git@github.com:jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git@github.com:jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://api.github.com/repos/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/none.git",
        GHRepo("jwodder", "none"),
    ),
]

BAD_REPOS = [
    "https://github.com/none/headerparser.git",
    "none/repo",
    "jwodder/headerparser.git",
    "jwodder/",
    "https://api.github.com/repos/jwodder/headerparser.git",
    "https://api.github.com/repos/jwodder/headerparser.git/",
    "https://api.github.com/repos/jwodder/headerparser/",
]


@pytest.mark.parametrize(
    "spec,repo",
    REPO_URLS
    + [
        ("jwodder/headerparser", GHRepo("jwodder", "headerparser")),
        ("headerparser", GHRepo("jwodder", "headerparser")),
        ("jwodder/none", GHRepo("jwodder", "none")),
        ("none", GHRepo("jwodder", "none")),
        ("nonely/headerparser", GHRepo("nonely", "headerparser")),
        ("none-none/headerparser", GHRepo("none-none", "headerparser")),
        ("nonenone/headerparser", GHRepo("nonenone", "headerparser")),
    ],
)
def test_parse(spec: str, repo: GHRepo) -> None:
    assert GHRepo.parse(spec, default_owner="jwodder") == repo


@pytest.mark.parametrize("spec", BAD_REPOS)
def test_parse_bad_spec(spec: str) -> None:
    with pytest.raises(ValueError):
        GHRepo.parse(spec)


@pytest.mark.parametrize("url,repo", REPO_URLS)
def test_parse_url(url: str, repo: GHRepo) -> None:
    assert GHRepo.parse_url(url) == repo


@pytest.mark.parametrize("url", BAD_REPOS)
def test_parse_bad_url(url: str) -> None:
    with pytest.raises(ValueError):
        GHRepo.parse_url(url)
