from flask import Flask

from . import extensions, views

def create_app():
  app = Flask(__name__)

  app.config["API_TITLE"] = "Quant Exchange API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.2"

  api = extensions.create_api(app)
  views.register_blueprints(api)

  return app
