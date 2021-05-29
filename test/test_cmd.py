import json
from pathlib import Path
from _pytest.capture import CaptureFixture
from ghrepo import GHRepo
from ghrepo.__main__ import main

THIS_DIR = str(Path(__file__).parent)


def test_command(capsys: CaptureFixture[str], local_repo: str) -> None:
    main([THIS_DIR])
    output, _ = capsys.readouterr()
    assert output.strip() == local_repo


def test_command_json(capsys: CaptureFixture[str], local_repo: str) -> None:
    owner, _, name = local_repo.partition("/")
    r = GHRepo(owner, name)
    main(["--json", THIS_DIR])
    output, _ = capsys.readouterr()
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
