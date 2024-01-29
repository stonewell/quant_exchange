import json
import bt
import pandas as pd
import datetime

from flask_smorest import Blueprint
from flask.views import MethodView

from quant_exchange.models import backtest as bt_model
from quant_exchange import context

from stock_data_provider.cn_a import load_stock_data


def baseline_backtest(args, data):
  s = bt.Strategy('baseline', [
      bt.algos.RunOnce(),
      bt.algos.SelectAll(),
      bt.algos.WeighEqually(),
      bt.algos.Rebalance()
  ])

  return bt.Backtest(s, data)


def get_date_offset(d, frequent):
  if frequent == 'D':
    return pd.DateOffset(days=d)

  return pd.DateOffset(days=d)


def backtest(args, data):
  s = bt.Strategy('custom', [
      bt.algos.RunEveryNPeriods(args['tradingInterval']),
      bt.algos.SelectAll(),
      bt.algos.SelectMomentum(
          args['stockCount'],
          get_date_offset(args['tradingInterval'], args['frequent'])),
      bt.algos.WeighEqually(),
      bt.algos.Rebalance()
  ])

  return bt.Backtest(s, data)


def create_dataframe(stocks, f, t):
  trading_data = {}
  for stock_id in stocks:
    d = load_stock_data(stock_id, False)
    d = d.set_index('day').sort_index()
    trading_data[stock_id] = d['close']

  panel = pd.DataFrame(data=trading_data)

  panel = filter_dataframe(panel.ffill(), f, t)
  return panel


def filter_dataframe(data, start_date=None, end_date=None):
  if start_date:
    start_date = pd.to_datetime(start_date)
  if end_date:
    end_date = pd.to_datetime(end_date)

  if not start_date and not end_date:
    return data

  if not start_date:
    return data[data.index <= end_date]

  if not end_date:
    return data[data.index >= start_date]

  return data[(data.index >= start_date) & (data.index <= end_date)]


def normalize_date(d):
  dd = datetime.datetime.fromtimestamp(d)

  dd = pd.to_datetime(dd).tz_localize(None)
  return dd.date()


def to_date_string(d):
  dd = datetime.datetime.fromtimestamp(d)
  dd = pd.to_datetime(dd).tz_localize(None)
  return dd.date().strftime('%Y-%m-%d')


def to_chart_data(result, key):
  v = result[key]

  idx = v['index'].to_list()
  val = v[key].to_list()

  return [{
      'x': to_date_string(int(idx[i].timestamp())),
      'y': val[i]
  } for i in range(len(idx))]


blp = Blueprint("BackTest",
                __name__,
                url_prefix="/backtest",
                description="backtest Operations")


@blp.route("/run")
class BackTests(MethodView):

  @blp.arguments(bt_model.RunBackTestSchema)
  @blp.response(200)
  def post(self, args):
    f = normalize_date(args['timeRangeFrom'])
    t = normalize_date(args['timeRangeTo'])

    print(args, f, t)

    data = create_dataframe(args['manualSelectedStocks'], f, t)
    benchmark = create_dataframe([args['baseline']], f, t)

    bt_benchmark = baseline_backtest(args, benchmark)
    bt_data = backtest(args, data)

    res = bt.run(bt_data, bt_benchmark)

    result = {}
    for key in res:
      result[key] = res[key].daily_prices.reset_index()

    return {
        'baseline': to_chart_data(result, 'baseline'),
        'custom': to_chart_data(result, 'custom'),
    }
