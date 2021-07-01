from flask_restplus import Namespace, Resource

from .advantage import Post as AdvantagePost
from .advantage import arg_parse as advantage_arg_parse
from .moves import Post as MovesPost
from .moves import arg_parse as moves_arg_parse

advantage_ns = Namespace(
    "advantages",
    description="Endpoint to determine which one have an advantage",
)

moves_ns = Namespace(
    "moves", description="Verify pokemon moves related transactions"
)


@advantage_ns.route("/")
class AdvantageOperation(Resource):
    """Should wrap all the operation related with advantage calculation"""

    @advantage_ns.expect(advantage_arg_parse)
    def post(self):
        """
        Check for type advantage
        Returns
            {
              "double_damage_to": boolean,
              "half_damage_from": boolean,
              "no_damage_from": boolean,
              "status_code": return_code
            }
        """
        args = advantage_arg_parse.parse_args()
        return AdvantagePost(args)


@moves_ns.route("/")
class MovesOperation(Resource):
    """Should wrap all the operation related with moves in general"""

    @moves_ns.expect(moves_arg_parse)
    def post(self):
        """
        Check for moves in common shared by a pokemon list
        """
        args = moves_arg_parse.parse_args()
        return MovesPost(args)
