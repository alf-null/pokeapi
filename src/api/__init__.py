
from flask_restplus import Resource,  Namespace
from .advantage import Post, arg_parse as advantage_arg_parse

advantage_ns = Namespace(
    'advantages',
    description='Endpoint to determine which one have an advantage'
)

@advantage_ns.route('/')
class AdvantageOperation(Resource):
    """Should wrap all the operation related with advantage calculation"""
    @advantage_ns.expect(advantage_arg_parse)
    def post(self):
        args = advantage_arg_parse.parse_args()
        return Post(args)