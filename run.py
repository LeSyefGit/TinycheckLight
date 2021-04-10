#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.blueprints.analysis import analysis_bp
from app.blueprints.misc import misc_bp
from app.blueprints.update import update_bp
from app.utils import read_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinycheck.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = "analysis/capture/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


# API Blueprints.
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(misc_bp, url_prefix='/api/misc')
app.register_blueprint(update_bp, url_prefix='/api/update')


class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    captures = db.relationship('Capture', backref='user',lazy=True)

    def __repr__(self):
        return self.email


class Capture(db.Model):
    __tablename__="captures"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.name

class IOC(db.Model):
    __tablename__="iocs"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    tlp = db.Column(db.Text, nullable=False)
    tag = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    added_on = db.Column(db.Numeric, nullable=False)


class Whitelist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.Text, nullable=False, unique=True)
    type = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    added_on = db.Column(db.Integer, nullable=False)

if __name__ == '__main__':
    # if read_config(("frontend", "remote_access")):
    #     app.run(host="0.0.0.0", port=8080, debug=True)
    # else:
    app.run(port=8080, debug=True)
