import json
from pathlib import Path
import subprocess
from _pytest.fixtures import FixtureRequest
import pytest
from ghrepo import GHRepo

THIS_DIR = str(Path(__file__).parent)


def test_command(request: FixtureRequest) -> None:
    local_repo = request.config.getoption("--local-repo")
    if local_repo is None:
        pytest.skip("--local-repo not set")
    output = subprocess.check_output(["ghrepo", THIS_DIR], universal_newlines=True)
    assert output.strip() == local_repo


def test_command_json(request: FixtureRequest) -> None:
    local_repo = request.config.getoption("--local-repo")
    if local_repo is None:
        pytest.skip("--local-repo not set")
    owner, _, name = local_repo.partition("/")
    r = GHRepo(owner, name)
    output = subprocess.check_output(
        ["ghrepo", "--json", THIS_DIR], universal_newlines=True
    )
    assert json.loads(output) == {
        "owner": owner,
        "name": name,
        "fullname": local_repo,
        "api_url": r.api_url,
        "clone_url": r.clone_url,
        "git_url": r.git_url,
        "html_url": r.html_url,
        "ssh_url": r.ssh_url,
    }
