from flask_smorest import Blueprint
from flask.views import MethodView
from quant_exchange.models import stock


blp = Blueprint("Stocks", __name__, url_prefix="/stocks", description="Operations on stocks")

@blp.route("/")
class Stocks(MethodView):
    @blp.arguments(stock.StocksQueryArgsSchema, location="query")
    @blp.response(200, stock.StockSchema(many=True))
    def get(self, args):
        """List Stocks"""
        print(args)

        return []

@blp.route("/<stock_id>")
@blp.route("/<stock_id>/info")
class StockInfo(MethodView):
    @blp.response(200, stock.StockSchema)
    def get(self, stock_id):
        """List Stocks"""
        print('info', stock_id)

        return None

@blp.route("/<stock_id>/daily")
class StockDataDaily(MethodView):
    @blp.response(200, stock.StockSchema)
    @blp.arguments(stock.StockQueryArgsSchema, location="query")
    def get(self, data_range, stock_id):
        """List Stocks"""
        print('daily', data_range, stock_id)

        return None

@blp.route("/<stock_id>/mins")
class StockDataMinutes(MethodView):
    @blp.response(200, stock.StockSchema)
    @blp.arguments(stock.StockQueryArgsSchema, location="query")
    def get(self, data_range, stock_id):
        """List Stocks"""
        print('mins', stock_id, data_range)

        return None
