import json

from flask_smorest import Blueprint
from flask.views import MethodView

from quant_exchange.models import stock
from quant_exchange import context

from stock_data_provider.cn_a import load_stock_data, load_stock_info


blp = Blueprint("Stocks",
                __name__,
                url_prefix="/stocks",
                description="Operations on stocks")


@blp.route("/")
class Stocks(MethodView):

  @blp.arguments(stock.StocksQueryArgsSchema, location="query")
  @blp.response(200, stock.StockSchema(many=True))
  def get(self, args):
    """List Stocks"""
    print(args)

    return []

def find_symbol(df, stock_id):
    rows = df.loc[(df['symbol'] == stock_id)
                  | ((df['symbol'] == (stock_id[2:]))
                 & (df['exchange'] == (stock_id[:2])))
                  | (df['abbr'] == stock_id)]

    if rows is None or rows.empty:
      return None

    print(rows)

    return rows

@blp.route("/<stock_id>")
@blp.route("/<stock_id>/info")
class StockInfo(MethodView):

  @blp.response(200, stock.StockSchema(many=True))
  def get(self, stock_id):
    """Return Stock Info"""
    print('info', stock_id)

    if len(stock_id) < 2:
      return {}

    df = load_stock_info()

    rows = find_symbol(df, stock_id)

    if rows is None:
      return {}

    values = []
    for _, row in rows.iterrows():
      print(row)

      values.append({
        "name": row['code_name'],
        "exchange-traded": row['exchange'],
        "exchange-listed": row['exchange'],
        "timezone": "Asia/Shanghai",
        "description": row['code_name'],
        "ticker": row['exchange'] + row['symbol'],
      })

    return values


@blp.route("/<stock_id>/daily")
class StockDataDaily(MethodView):

  @blp.response(200, stock.StockDataSchema(many=True))
  @blp.arguments(stock.StockQueryArgsSchema, location="query")
  def get(self, data_range, stock_id):
    d = load_stock_data(stock_id, False)
    data = d.reset_index()
    value = data.to_dict(orient="records")

    return value


@blp.route("/<stock_id>/mins")
class StockDataMinutes(MethodView):

  @blp.response(200, stock.StockDataSchema(many=True))
  @blp.arguments(stock.StockQueryArgsSchema, location="query")
  def get(self, data_range, stock_id):
    return None

@blp.route("/watch_list")
class StockDataDaily(MethodView):

  @blp.response(200, stock.StockWatchListDataSchema(many=True))
  @blp.arguments(stock.StockWatchListQueryArgsSchema, location="query")
  def get(self, data):
    print(data)
    symbols = data['symbols']

    if len(symbols) == 0:
      return []

    df_info = load_stock_info()

    values = []
    for symbol in symbols:
      rows = find_symbol(df_info, symbol)

      if rows is None:
        continue

      for _, row in rows.iterrows():
        values.append(get_watch_data(row))

    return values


def get_watch_data(row):
  name = row['code_name']
  ticker = row['exchange'] + row['symbol']

  df_data = load_stock_data(ticker, False)
  df_data = df_data.reset_index()
  df_data = df_data[-2:]

  price = 0.0
  change = 0.0

  if len(df_data) == 2:
    price = df_data.iloc[1]['close']
    prev_price = df_data.iloc[0]['close']

    if (prev_price > 0):
      change = price - prev_price
  elif len(df_data) == 1:
    price = df_data.iloc[0]['close']

  return {
        'name': name,
        'price': price,
        'change': change,
  }
