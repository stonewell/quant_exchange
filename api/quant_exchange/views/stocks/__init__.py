from flask_smorest import Blueprint
from flask.views import MethodView
from quant_exchange.models import stock


blp = Blueprint("Stocks", __name__, url_prefix="/stocks", description="Operations on stocks")

@blp.route("/")
class Stocks(MethodView):
    @blp.arguments(stock.StockQueryArgsSchema, location="query")
    @blp.response(200, stock.StockSchema(many=True))
    def get(self, args):
        """List Stocks"""
        print(args)

        return []
