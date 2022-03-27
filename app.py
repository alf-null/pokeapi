import logging
from os import environ

from flask import Blueprint, Flask
from flask_restplus import Api

from pokeapi.api import advantage_ns as AdvantageType
from pokeapi.api import moves_ns as MovesInCommon


# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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
    debug = environ.get("flask_debug", False)
    logger.info(f"Server started flask_debug={debug}")

    if debug:
        app.run(debug=debug)
    else:
        from waitress import serve
        serve(app, host="127.0.0.1", port=5000)
