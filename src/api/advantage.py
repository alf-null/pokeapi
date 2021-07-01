import json
import requests
import os 
from sys import stderr
from os import path
from typing import Any, Dict


from flask import jsonify
import requests
from schema.advantage import AdvantageTypesSchema
from model.advantage import AdvantageTypes

from flask_restplus.namespace import RequestParser

arg_parse = RequestParser()
arg_parse.add_argument(
    name="first_type",
    required=True, 
    location='json',
    help='''Contains first and second pokemon types respectively'''
)
arg_parse.add_argument(
    name="second_type",
    required=True, 
    location='json',
    help='''Contains first and second pokemon types respectively'''
)

def verify_types(data_model: AdvantageTypes) -> bool:
    ret_value = True
    resgisted_types = '../resources/resgistered_types.json'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, resgisted_types)

    if path.exists(filename):
        with open(filename) as types_json:
            types_list = json.load(types_json)
            for type_item in types_list['results']:
                if data_model.first_type not in type_item['name'] or data_model.second_type not in type_item['name']:
                    print(type_item['name'])
                    ret_value = True
    else:
        print("Missing type list from resources", file=stderr)
        ret_value = False
    return ret_value


def verify_type_properties(data_model: AdvantageTypes) -> Dict:
    response = {}
    resgisted_types = f'../resources/type_{data_model.first_type}.json'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, resgisted_types)

    with open(filename) as type_list:
        type_list = json.load(type_list)

        # Search if the first attack type can deal double damage
        for attack_type in type_list['damage_relations']['double_damage_to']:
            if data_model.second_type == attack_type['name']:
                response['double_damage_to'] =  True
                break
        if 'double_damage_to' not in response:
            response['double_damage_to'] = False

        # Search if the second attack type can half damage
        for attack_type in type_list['damage_relations']["half_damage_from"]:
            if data_model.second_type == attack_type['name']:
                response['half_damage_from'] = True
                break
        if 'half_damage_from' not in response:
            response['half_damage_from'] = False

        # Search if the second attack type can half damage
        for attack_type in type_list['damage_relations']['no_damage_from']:
            if data_model.second_type == attack_type['name']:
                response['no_damage_from'] = True
                break
        if 'no_damage_from' not in response:
            response['no_damage_from'] = False
    return response

def Post(args: Dict) ->Any:
    """Implements logic for assuming damage dealing advantage"""
    response = None
    schema = AdvantageTypesSchema().load(args)
    data_model = AdvantageTypes(**schema)
    dirname = os.path.dirname(__file__)
    
    if verify_types(data_model):
        advantage_file = f'../resources/type_{data_model.first_type}.json'
        advantage_fp = os.path.join(dirname, advantage_file)

        if path.exists(advantage_fp):
            response = verify_type_properties(data_model)
        else: 
            resgisted_types = '../resources/resgistered_types.json'
            filename = os.path.join(dirname, resgisted_types)
            with open(filename) as types_json:
                types_list = json.load(types_json)
                for type_item in types_list['results']:
                    if data_model.first_type == type_item['name']:
                        with requests.get(type_item['url']) as req:
                            with open(advantage_fp, 'wb') as new_json:
                                new_json.write(req.content)
            response = verify_type_properties(data_model)
        response['status_code'] = 200
    return jsonify(response)