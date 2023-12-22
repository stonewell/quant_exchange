import json

from flask_smorest import Blueprint
from flask.views import MethodView

from quant_exchange.models import stock

from stock_data_provider.cn_a.vip_dataset import load_stock_data


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
    @blp.response(200, stock.StockDataSchema(many=True))
    @blp.arguments(stock.StockQueryArgsSchema, location="query")
    def get(self, data_range, stock_id):
        d = load_stock_data(stock_id, False)
        data = d[0].data_frame.reset_index()
        value = data.to_dict(orient="records")

        return value

@blp.route("/<stock_id>/mins")
class StockDataMinutes(MethodView):
    @blp.response(200, stock.StockDataSchema(many=True))
    @blp.arguments(stock.StockQueryArgsSchema, location="query")
    def get(self, data_range, stock_id):
        return None
