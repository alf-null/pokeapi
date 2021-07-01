from marshmallow import Schema, fields

# Defines schema for validation

class MovesInCommonSchema(Schema):
    '''Implements schema validation for moves POST'''
    lan = fields.String(required=True, default='en')
    pokemons = fields.List(fields.String(), required=True)
    limit = fields.Number(default=20)