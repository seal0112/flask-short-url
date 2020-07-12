from flask import Flask
from config import config
from app.extensions import db, migrate


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    from .short_url import short_url as short_url_blueprint
    app.register_blueprint(short_url_blueprint, url_prefix='/')
