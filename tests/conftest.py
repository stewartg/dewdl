import pytest


@pytest.fixture
def _unstub():
    """Ensures proper unstubbing of mocks after each test."""
    from mockito import unstub

    yield
    unstub()
