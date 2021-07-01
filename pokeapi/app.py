from os import environ

from flask import Flask, Blueprint
from flask_restplus import Api

from .api import advantage_ns as AdvantageType
from .api import moves_ns as MovesInCommon

v1_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
app = Flask(__name__)
app.config["RESTPLUS_MASK_SWAGGER"] = False

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

if __name__ == "__main__":
    debug = environ.get("flask_debug", True)
    app.run(debug=debug)
