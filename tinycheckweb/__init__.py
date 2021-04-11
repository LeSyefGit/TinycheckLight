#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from tinycheckweb.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
         
    from tinycheckweb.users.routes import users
    from tinycheckweb.analysis.routes import analysis_bp

    app.register_blueprint(users, url_prefix="/api/auth")
    app.register_blueprint(analysis_bp, url_prefix="/api/analysis")

    return app