import json

from flask_smorest import Blueprint
from flask.views import MethodView

from quant_exchange.models import backtest as bt_model
from quant_exchange import context

from stock_data_provider.cn_a import load_stock_data


blp = Blueprint("BackTest",
                __name__,
                url_prefix="/backtest",
                description="backtest Operations")


@blp.route("/run")
class BackTests(MethodView):

  @blp.arguments(bt_model.RunBackTestSchema)
  @blp.response(200)
  def post(self, args):
    print(args)
    return []
