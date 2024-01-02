from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from flask_caching import Cache

from . import context


def create_app():
  app = Flask(__name__)

  app.config["API_TITLE"] = "Quant Exchange API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.2"
  # Flask-Caching related configs
  app.config["CACHE_TYPE"] = "SimpleCache"
  app.config["CACHE_DEFAULT_TIMEOUT"] = 300
  app.config.from_prefixed_env()

  context.cache = Cache(app)

  from . import extensions, views
  api = extensions.create_api(app)
  views.register_blueprints(api)

  return app
