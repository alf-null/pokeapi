from marshmallow import Schema, fields

# Defines schema validation

class AdvantageTypesSchema(Schema):
    '''Implements schema validations for advantage_types GET'''
    first_type = fields.String(required=True)
    second_type = fields.String(required=True)
