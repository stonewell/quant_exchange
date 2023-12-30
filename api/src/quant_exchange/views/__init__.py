from . import stocks, udf


def register_blueprints(api):
  api.register_blueprint(stocks.blp)
  api.register_blueprint(udf.blp)
