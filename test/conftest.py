import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--local-repo")


@pytest.fixture
def local_repo(request: pytest.FixtureRequest) -> str:
    lr = request.config.getoption("--local-repo")
    if lr is None:
        pytest.skip("--local-repo not set")
    assert isinstance(lr, str)
    return lr
