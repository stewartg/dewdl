import pytest

from dewdl._dewdl_configs import DewDLConfigs


@pytest.fixture
def _unstub():
    """Ensures proper unstubbing of mocks after each test."""
    from mockito import unstub

    yield
    unstub()


# @pytest.fixture(scope="session", autouse=True)
# def _configure_udl_env():
#     DewDLConfigs.update_udl_env("test")


@pytest.fixture(autouse=True)
def _configure_udl_env(monkeypatch):
    monkeypatch.setattr(DewDLConfigs, "get_udl_env", lambda: "test")
