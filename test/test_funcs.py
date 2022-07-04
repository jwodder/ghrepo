from pathlib import Path
from conftest import TmpRepo
import pytest
from ghrepo import get_current_branch, get_local_repo, is_git_repo


def test_is_git_repo(monkeypatch: pytest.MonkeyPatch, tmp_repo: TmpRepo) -> None:
    assert is_git_repo(tmp_repo.path)
    monkeypatch.chdir(tmp_repo.path)
    assert is_git_repo()


def test_is_not_git_repo(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    assert not is_git_repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert not is_git_repo()


def test_get_current_branch(monkeypatch: pytest.MonkeyPatch, tmp_repo: TmpRepo) -> None:
    assert get_current_branch(tmp_repo.path) == tmp_repo.branch
    monkeypatch.chdir(tmp_repo.path)
    assert get_current_branch() == tmp_repo.branch


def test_get_local_repo(monkeypatch: pytest.MonkeyPatch, tmp_repo: TmpRepo) -> None:
    assert get_local_repo(tmp_repo.path) == tmp_repo.remotes["origin"]
    assert (
        get_local_repo(tmp_repo.path, remote="upstream") == tmp_repo.remotes["upstream"]
    )
    monkeypatch.chdir(tmp_repo.path)
    assert get_local_repo() == tmp_repo.remotes["origin"]
    assert get_local_repo(remote="upstream") == tmp_repo.remotes["upstream"]
