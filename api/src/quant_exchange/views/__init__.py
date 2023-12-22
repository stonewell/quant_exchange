from . import stocks


def register_blueprints(api):
  api.register_blueprint(stocks.blp)
