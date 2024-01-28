from . import stocks, udf, backtest


def register_blueprints(api):
  api.register_blueprint(stocks.blp)
  api.register_blueprint(udf.blp)
  api.register_blueprint(backtest.blp)
