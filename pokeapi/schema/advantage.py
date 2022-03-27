from marshmallow import Schema, fields, pre_load

# Defines schema for validation


class ReqAdvantageTypesSchema(Schema):
    """Expected req schema validations for advantages POST"""

    first_type = fields.String(required=True)
    second_type = fields.String(required=True)

    @pre_load
    def to_lowercase(self, in_data, **kwargs):
        """Switch any uppercase to lowercase"""
        in_data["first_type"] = in_data["first_type"].lower()
        in_data["second_type"] = in_data["second_type"].lower()
        return in_data


class ResAdvantageTypesSchema(Schema):
    """Expected res schema validations for advantages POST"""
    double_damage_to = fields.Boolean(required=True)
    half_damage_from = fields.Boolean(required=True)
    no_damage_from = fields.Boolean(required=True)
