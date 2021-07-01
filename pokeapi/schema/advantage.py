from marshmallow import Schema, fields, pre_load

# Defines schema for validation


class AdvantageTypesSchema(Schema):
    """Implements schema validations for advantages POST"""

    first_type = fields.String(required=True)
    second_type = fields.String(required=True)

    @pre_load
    def to_lowercase(self, in_data, **kwargs):
        """Switch any uppercase to lowercase"""
        in_data["first_type"] = in_data["first_type"].lower()
        in_data["second_type"] = in_data["second_type"].lower()
        return in_data
