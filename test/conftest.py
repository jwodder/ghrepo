from pathlib import Path
import shutil
import subprocess
from typing import Dict, NamedTuple
import pytest
from ghrepo import GHRepo


class TmpRepo(NamedTuple):
    path: Path
    branch: str
    remotes: Dict[str, GHRepo]
    upstreams: Dict[str, GHRepo]


@pytest.fixture(scope="session")
def tmp_repo(tmp_path_factory: pytest.TempPathFactory) -> TmpRepo:
    if shutil.which("git") is None:
        pytest.skip("Git not installed")
    tmp_path = tmp_path_factory.mktemp("tmp_repo")
    BRANCH = "trunk"
    REMOTES = {
        "origin": GHRepo("octocat", "repository"),
        "upstream": GHRepo("foobar", "repo"),
    }
    subprocess.run(
        ["git", "-c", f"init.defaultBranch={BRANCH}", "init"],
        check=True,
        cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "remote", "add", "origin", REMOTES["origin"].ssh_url],
        check=True,
        cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "remote", "add", "upstream", REMOTES["upstream"].clone_url],
        check=True,
        cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "config", "branch.draft.remote", "upstream"],
        check=True,
        cwd=str(tmp_path),
    )
    return TmpRepo(tmp_path, BRANCH, REMOTES, {"draft": REMOTES["upstream"]})
