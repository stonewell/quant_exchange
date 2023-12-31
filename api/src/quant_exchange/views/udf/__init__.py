import json
import datetime

import pandas as pd
from flask_smorest import Blueprint
from flask.views import MethodView

from quant_exchange.models import udf

from stock_data_provider.cn_a import load_stock_data, load_stock_info

blp = Blueprint("UDF",
                __name__,
                url_prefix="/udf",
                description="UDF stock api")

config = {
    # Represents the resolutions for bars supported by your datafeed
    'supported_resolutions': ['5', '1D'],
    # The `exchanges` arguments are used for the `searchSymbols` method if a user selects the exchange
    'exchanges': [
        {
            'value': 'all',
            'name': '中国A股',
            'desc': 'All China Stocks'
        },
        {
            'value': 'sh',
            'name': '上证',
            'desc': 'Shang Hai Exchange'
        },
        {
            'value': 'sz',
            'name': '深证',
            'desc': 'Shen Zhen Exchange'
        },
        {
            'value': 'of',
            'name': 'ETF',
            'desc': ''
        },
    ],
    # The `symbols_types` arguments are used for the `searchSymbols` method if a user selects this symbol type
    'symbols_types': [
        {
            'name': '股票',
            'value': 'stock',
        },
        {
            'name': '指数',
            'value': 'index',
        },
        {
            'name': '其他',
            'value': 'other',
        },
        {
            'name': '可转债',
            'value': 'bond',
        },
        {
            'name': 'ETF',
            'value': 'etf',
        },
    ],
    "supports_group_request":
    False,
    "supports_marks":
    True,
    "supports_search":
    True,
    "supports_timescale_marks":
    False,
}


@blp.route("/config")
class Config(MethodView):

  @blp.response(200)
  def get(self):
    return config


@blp.route("/symbols")
class Symbols(MethodView):

  @blp.response(200)
  @blp.arguments(udf.SymbolResolveArgsSchema, location="query")
  def get(self, args):
    print(args)

    df = load_stock_info()
    row = df.loc[df['symbol'] == args['s']].iloc[0]
    print(row)

    return {
        "name": row['code_name'],
        "exchange-traded": row['exchange'],
        "exchange-listed": row['exchange'],
        "timezone": "Asia/Shanghai",
        "minmov": 1,
        "minmov2": 0,
        "pointvalue": 1,
        "session": "0930-1500",
        "has_intraday": False,
        "visible_plots_set": "ohlcv",
        "description": row['code_name'],
        "type": config['symbols_types'][row['type'] - 1]['value'],
        "supported_resolutions": ["D", "5"],
        "pricescale": 100,
        "ticker": row['symbol'],
    }


@blp.route("/history")
class History(MethodView):

  @blp.response(200)
  @blp.arguments(udf.HistoryArgsSchema, location="query")
  def get(self, args):
    if not 's' in args or args['s'] == '':
      return {
        "s": "no_data",
      }

    f = pd.Timestamp.fromtimestamp(args['f'], 'UTC').tz_localize(None).round('D')
    t = pd.Timestamp.fromtimestamp(args['t'], 'UTC').tz_localize(None).round('D')
    c = int(args['c']) if 'c' in args else -1

    print(args, f, t, c)

    df = load_stock_info()
    row = df.loc[df['symbol'] == args['s']].iloc[0]

    price_adj = 1

    if config['symbols_types'][row['type'] - 1]['value'] == 'index':
      price_adj = 100

    d = load_stock_data(args['s'], False)
    data = d[0].data_frame.reset_index()

    if data.empty or t < data.iloc[0]['day']:
      return {
          "s": "no_data",
      }

    if c > 0:
      data = data.loc[
        (data['day'] <= t)
      ]
      data = data[-c:]
    else:
      data = data.loc[
        (data['day'] >= f)
        & (data['day'] <= t)
      ]

    if data.empty:
      return {
          "s": "no_data",
      }

    result = {
        "s": "ok",
        "t": [day.tz_localize('UTC').round('D').timestamp() for day in data['day'].to_list()],
        "c": [d * price_adj for d in data['close'].to_list()],
        "o": [d * price_adj for d in data['open'].to_list()],
        "h": [d * price_adj for d in data['high'].to_list()],
        "l": [d * price_adj for d in data['low'].to_list()],
        "v": data['volume'].to_list()
    }

    return result


def find_symbol_type(t):
  symbol_types = config['symbols_types']

  for idx in range(len(symbol_types)):
    st = symbol_types[idx]
    if st['value'] == t:
      return idx + 1
  return -1


@blp.route("/search")
class Search(MethodView):

  @blp.response(200, udf.SearchResultSchema(many=True))
  @blp.arguments(udf.SearchArgsSchema, location="query")
  def get(self, args):
    print(args)

    types = range(1, 6)

    if args['t'] != '':
      types = [find_symbol_type(args['t'])]

    exchanges = [x['value'] for x in config['exchanges']]

    if not args['e'] in ['', 'all']:
      exchanges = [args['e']]

    df = load_stock_info()
    rows = df.loc[df['symbol'].str.startswith(args['q'], na=False)
                  & df['type'].isin(types)
                  & df['exchange'].isin(exchanges)].head(int(args['l']))
    print(rows)

    result = []
    for idx, row in rows.iterrows():
      result.append({
          "d": row['code_name'],
          "n": row['exchange'] + ':' + row['symbol'],
          "e": row['exchange'],
          "s": row['symbol'],
          "ti": row['symbol'],
          "t": config['symbols_types'][row['type'] - 1]['value'],
      })
    return result
