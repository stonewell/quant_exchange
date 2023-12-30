import json

from flask_smorest import Blueprint
from flask.views import MethodView

from quant_exchange.models import udf

from stock_data_provider.cn_a.vip_dataset import load_stock_data

blp = Blueprint("UDF",
                __name__,
                url_prefix="/udf",
                description="UDF stock api")


@blp.route("/config")
class Config(MethodView):

  @blp.response(200)
  def get(self):
    return {
        # Represents the resolutions for bars supported by your datafeed
        'supported_resolutions': ['5', '1D'],
        # The `exchanges` arguments are used for the `searchSymbols` method if a user selects the exchange
        'exchanges': [
            {
                'value': 'all',
                'name': 'China',
                'desc': 'All China Stocks'
            },
            {
                'value': 'sh',
                'name': 'Shang Hai',
                'desc': 'Shang Hai Exchange'
            },
            {
                'value': 'sz',
                'name': 'Shen Zhen',
                'desc': 'Shen Zhen Exchange'
            },
        ],
        # The `symbols_types` arguments are used for the `searchSymbols` method if a user selects this symbol type
        'symbols_types': [{
            'name': 'Stock',
            'value': 'stock'
        }],
        "supports_group_request":
        False,
        "supports_marks":
        True,
        "supports_search":
        True,
        "supports_timescale_marks":
        False,
    }


@blp.route("/symbols")
class Symbols(MethodView):

  @blp.response(200)
  @blp.arguments(udf.SymbolResolveArgsSchema, location="query")
  def get(self, args):
    print(args)
    return {
        "name": args['s'],
        "exchange-traded": "sh",
        "exchange-listed": "sh",
        "timezone": "Asia/Shanghai",
        "minmov": 1,
        "minmov2": 0,
        "pointvalue": 1,
        "session": "0930-1500",
        "has_intraday": False,
        "visible_plots_set": "ohlcv",
        "description": "Shang Hai Index:" + args['s'] ,
        "type": "stock",
        "supported_resolutions": ["D", "5"],
        "pricescale": 100,
        "ticker": args['s'],
    }


@blp.route("/history")
class History(MethodView):

  @blp.response(200)
  @blp.arguments(udf.HistoryArgsSchema, location="query")
  def get(self, args):
    print(args)

    if args['c'] == 325 or args['c'] > 329:
      return {
          "s": "no_data",
      }

    return {
        "s": "ok",
        "t": [1386493512, 1386493572, 1386493632, 1386493692],
        "c": [42.1, 43.4, 44.3, 42.8],
        "o": [41.0, 42.9, 43.7, 44.5],
        "h": [43.0, 44.1, 44.8, 44.5],
        "l": [40.4, 42.1, 42.8, 42.3],
        "v": [12000, 18500, 24000, 45000]
    }

@blp.route("/search")
class Search(MethodView):

  @blp.response(200, udf.SearchResultSchema(many=True))
  @blp.arguments(udf.SearchArgsSchema, location="query")
  def get(self, args):
    print(args)

    return [
      {
        "d":"stock 1",
        "n":"sh:600001",
        "e":"sh",
        "s":"600001",
        "ti":"600001",
        "t":"stock",
      },
      {
        "d":"stock 2",
        "n":"sh:600002",
        "e":"sh",
        "s":"600002",
        "ti":"600002",
        "t":"stock",
      },
    ]
