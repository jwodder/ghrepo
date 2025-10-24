from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
from conftest import TmpRepo
import pytest
from pytest_mock import MockerFixture
from ghrepo.__main__ import main


def test_command(
    capsys: pytest.CaptureFixture[str],
    tmp_repo: TmpRepo,
    mocker: MockerFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_repo.path)
    monkeypatch.setattr(sys, "argv", ["ghrepo"])
    spy = mocker.spy(subprocess, "run")
    assert main() == 0
    spy.assert_called_once_with(
        ["git", "remote", "get-url", "--", "origin"],
        cwd=None,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out.strip() == str(tmp_repo.remotes["origin"])
    assert err == ""


def test_command_json_dir(
    capsys: pytest.CaptureFixture[str], tmp_repo: TmpRepo, mocker: MockerFixture
) -> None:
    r = tmp_repo.remotes["origin"]
    spy = mocker.spy(subprocess, "run")
    assert main(["--json", str(tmp_repo.path)]) == 0
    spy.assert_called_once_with(
        ["git", "remote", "get-url", "--", "origin"],
        cwd=str(tmp_repo.path),
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert json.loads(out) == {
        "owner": r.owner,
        "name": r.name,
        "fullname": str(r),
        "api_url": r.api_url,
        "clone_url": r.clone_url,
        "git_url": r.git_url,
        "html_url": r.html_url,
        "ssh_url": r.ssh_url,
    }
    assert err == ""


@pytest.mark.parametrize("opts", [[], ["--json"]])
def test_command_non_repo(
    opts: list[str], capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    assert main(opts + [str(tmp_path)]) != 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""


@pytest.mark.parametrize("opts", [[], ["--json"]])
def test_command_bad_url(
    opts: list[str], capsys: pytest.CaptureFixture[str], mocker: MockerFixture
) -> None:
    m = mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "remote", "get-url", "--", "origin"],
            returncode=0,
            stdout="git@gist.github.com:cee837802578a4fc8854df60529af98c.git\n",
            stderr=None,
        ),
    )
    assert main(opts) == 1
    m.assert_called_once_with(
        ["git", "remote", "get-url", "--", "origin"],
        cwd=None,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out == ""
    assert err == (
        "ghrepo: Invalid GitHub URL:"
        " 'git@gist.github.com:cee837802578a4fc8854df60529af98c.git'\n"
    )


def test_command_remote(
    capsys: pytest.CaptureFixture[str], mocker: MockerFixture
) -> None:
    m = mocker.patch(
        "subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "remote", "get-url", "--", "upstream"],
            returncode=0,
            stdout="git@github.com:jwodder/daemail.git\n",
            stderr=None,
        ),
    )
    assert main(["--remote", "upstream"]) == 0
    m.assert_called_once_with(
        ["git", "remote", "get-url", "--", "upstream"],
        cwd=None,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out == "jwodder/daemail\n"
    assert err == ""


def test_command_no_such_remote(
    capsys: pytest.CaptureFixture[str], mocker: MockerFixture
) -> None:
    m = mocker.patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            cmd=["git", "remote", "get-url", "--", "upstream"],
            returncode=2,
            output="",
            stderr=None,
        ),
    )
    assert main(["--remote", "upstream"]) == 2
    m.assert_called_once_with(
        ["git", "remote", "get-url", "--", "upstream"],
        cwd=None,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
