import pytest

from pokeapi.app import app


@pytest.fixture
def test_app():
    app.testing = True
    return app.test_client()
