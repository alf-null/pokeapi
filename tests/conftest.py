import pytest

from flask import Blueprint, Flask
from flask_restplus import Api

from pokeapi.api import advantage_ns as AdvantageType
from pokeapi.api import moves_ns as MovesInCommon


@pytest.fixture
def app():
    v1_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    app = Flask(__name__)

    api = Api(
        v1_blueprint,
        version="1.0",
        title="Poke-API",
        description="Search for pokemon type weakness and common moves",
    )

    # Add appi methods namespaces
    api.add_namespace(AdvantageType)
    api.add_namespace(MovesInCommon)

    app.register_blueprint(v1_blueprint)

    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
