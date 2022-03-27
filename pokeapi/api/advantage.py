import json
import os
from os import path
from sys import stderr
from typing import Any, Dict

import requests
from flask import jsonify, make_response, Response
from flask_restplus.namespace import RequestParser

from ..model.advantage import AdvantageTypes
from ..schema.advantage import ReqAdvantageTypesSchema, ResAdvantageTypesSchema

arg_parse = RequestParser()
arg_parse.add_argument(
    name="first_type",
    required=True,
    location="form",
    help="Contains second pokemon move type",
)
arg_parse.add_argument(
    name="second_type",
    required=True,
    location="form",
    help="Contains first pokemon move type",
)


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


resource_path = "../resources"
dirname = os.path.dirname(__file__)


def verify_types(data_model: AdvantageTypes) -> bool:
    ret_value = True
    resgisted_types = f"{resource_path}/resgistered_types.json"
    filename = os.path.join(dirname, resgisted_types)

    if path.exists(filename):
        with open(filename) as types_json:
            types_list = json.load(types_json)
            for type_item in types_list["results"]:
                if (
                    data_model.first_type not in type_item["name"]
                    or data_model.second_type not in type_item["name"]
                ):
                    ret_value = True
    else:
        logger.error("Missing type list from resources folder")
        ret_value = False
    return ret_value


def verify_type_properties(data_model: AdvantageTypes) -> ResAdvantageTypesSchema:
    response = {}
    resgisted_types = f"{resource_path}/type_{data_model.first_type}.json"
    filename = os.path.join(dirname, resgisted_types)

    with open(filename) as type_list:
        type_list = json.load(type_list)

        # Search if the first attack type can deal double damage
        for attack_type in type_list["damage_relations"]["double_damage_to"]:
            if data_model.second_type == attack_type["name"]:
                response["double_damage_to"] = True
                break
        if "double_damage_to" not in response:
            response["double_damage_to"] = False

        # Search if the second attack type can half damage
        for attack_type in type_list["damage_relations"]["half_damage_from"]:
            if data_model.second_type == attack_type["name"]:
                response["half_damage_from"] = True
                break
        if "half_damage_from" not in response:
            response["half_damage_from"] = False

        # Search if the second attack type can half damage
        for attack_type in type_list["damage_relations"]["no_damage_from"]:
            if data_model.second_type == attack_type["name"]:
                response["no_damage_from"] = True
                break
        if "no_damage_from" not in response:
            response["no_damage_from"] = False
    return ResAdvantageTypesSchema().dump(response)


def Post(args: Dict) -> Any:
    """Implements logic for assuming damage dealing advantage"""
    logger.info(f"Advantage type post: {args}")
    response = None
    schema = ReqAdvantageTypesSchema().load(args)
    data_model = AdvantageTypes(**schema)

    if verify_types(data_model):
        advantage_file = f"{resource_path}/type_{data_model.first_type}.json"
        advantage_fp = os.path.join(dirname, advantage_file)

        if path.exists(advantage_fp):
            response = verify_type_properties(data_model)
        else:
            resgisted_types = f"{resource_path}/resgistered_types.json"
            filename = os.path.join(dirname, resgisted_types)
            with open(filename) as types_json:
                types_list = json.load(types_json)
                for type_item in types_list["results"]:
                    if data_model.first_type == type_item["name"]:
                        with requests.get(type_item["url"]) as req:
                            with open(advantage_fp, "wb") as new_json:
                                new_json.write(req.content)
            if path.exists(advantage_fp):
                response = verify_type_properties(data_model)
    else:
        response = make_response(jsonify(message="type not found"), 404)
    if not response:
        response = make_response(jsonify(message="type not found"), 404)
    logger.info(f"Served response: {response}")
    return response if isinstance(response, Response) else jsonify(response)
