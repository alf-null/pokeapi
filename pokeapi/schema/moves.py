from marshmallow import Schema, fields, pre_load

# Defines schema for validation


class MovesInCommonSchema(Schema):
    """Implements schema validation for moves POST"""

    lan = fields.String(required=True, default="en")
    pokemons = fields.List(fields.String(), required=True)
    limit = fields.Integer(default=10)

    @pre_load
    def clean_pokemons(self, in_data, **kwargs):
        """Change formant, from comma separated to python list"""
        in_data["pokemons"] = in_data["pokemons"].replace(" ", "").split(",")
        return in_data
