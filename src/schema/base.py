from marshmallow import fields


class LowerCaseString(fields.String):
    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'lower'):
            value = value.lower()
        return super()._deserialize(value, *args, **kwargs)
