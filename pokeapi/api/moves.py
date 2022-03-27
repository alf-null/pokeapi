import json
import os
from typing import Any, Dict

import requests
from flask import jsonify, make_response
from flask_restplus.namespace import RequestParser

from ..model.moves import MovesInCommon
from ..schema.moves import ReqMovesInCommonSchema, ResMovesInCommonSchema

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


arg_parse = RequestParser()
arg_parse.add_argument(
    name="lan",
    default="en",
    location="form",
    help="Set a translation language for the moves, defaul: en",
)
arg_parse.add_argument(
    name="pokemons",
    required=True,
    location="form",
    help="This is a list of pokemos separated by comma each one",
)
arg_parse.add_argument(
    name="limit",
    default="10",
    location="from",
    help="Set a maximum return number for moves, default: 20",
)

pokeapi_base_uri = r"https://pokeapi.co/api/v2"
pokemon_resources = "../resources/pokemons"
dirname = os.path.dirname(__file__)


def get_moves(file: str):
    moves = []
    with open(file) as pokemon_data:
        moves_data = json.load(pokemon_data)["moves"]
        for move in moves_data:
            moves.append(move["move"]["name"])
    return moves


def Post(args: Dict) -> Any:
    """Implement logic for matching moves on many pokemon"""    
    logger.info(f"Moves post: {args}")
    schema = ReqMovesInCommonSchema().load(args)
    data_model = MovesInCommon(**schema)

    pokemon_moves = []
    pokemon_errors = []
    common_moves = []

    for pokemon in data_model.pokemons:
        pokemon_file = os.path.join(
            dirname,
            f"{pokemon_resources}/{pokemon}.json",
        )
        if os.path.exists(pokemon_file):
            moves = get_moves(pokemon_file)
            pokemon_moves.append(moves)
        else:
            with requests.get(f"{pokeapi_base_uri}/pokemon/{pokemon}") as req:
                if not req:
                    logger.warning(f"Pokemon {pokemon} not found")
                    pokemon_errors.append(pokemon)
                    continue
                
                try:
                    with open(pokemon_file, "wb") as new_pokemon_file:
                        new_pokemon_file.write(req.content)
                except OSError:
                    return make_response(jsonify(message="File management error"), 500)
            moves = get_moves(pokemon_file)
            pokemon_moves.append(moves)

    repeated = {}
    for move_set in pokemon_moves:
        for move in move_set:
            if move in repeated:
                repeated[move] += 1
            else:
                repeated[move] = 1

    for key, value in repeated.items():
        if value == len(data_model.pokemons):
            common_moves.append(key)

    if data_model.lan != "en":
        for i in range(len(common_moves)):
            with requests.get(
                f"{pokeapi_base_uri}/move/{common_moves[i]}"
            ) as req:
                for name in req.json()["names"]:
                    if name["language"]["name"] == data_model.lan:
                        common_moves[i] = name["name"]

    logger.info(f"Served response: {common_moves}")
    response = jsonify(ResMovesInCommonSchema().dump({"shared_moves":common_moves, "processing_erros": pokemon_errors}))
    return response if not pokemon_errors else make_response(response, 206)
    
