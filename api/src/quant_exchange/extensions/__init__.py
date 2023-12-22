from flask_smorest import Api


def create_api(app):
  api = Api(app)

  return api
