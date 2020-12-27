#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, send_file
from app.decorators import *
from app.classes.config import Config
import sys

config_bp = Blueprint("config", __name__)
config = Config()


@config_bp.route('/switch/<cat>/<key>', methods=['GET'])
@require_header_token
def switch(cat, key):
    """
        Switch the Boolean value of a configuration key.
        :return: status in JSON
    """
    try:
        value = config.read_config((cat, key))
        if value:
            config.write_config(cat, key, False)
            res = {"status": True,
                   "message": "Key switched to false"}
        else:
            config.write_config(cat, key, True)
            res = {"status": True,
                   "message": "Key switched to true"}
    except:
        res = {"status": True,
               "message": "Issue while changing value"}

    return jsonify(res)


@config_bp.route('/edit/<cat>/<key>/<path:value>', methods=['GET'])
@require_header_token
def edit(cat, key, value):
    """
        Edit the string (or array) value of a configuration key.
        :return: status in JSON
    """
    return jsonify(config.write_config(cat, key, value))


@config_bp.route('/db/export', methods=['GET'])
@require_get_token
def export_db():
    """
        Export the database.
        :return: current database as attachment
    """
    return config.export_db()


@config_bp.route('/db/import', methods=['POST'])
@require_header_token
def import_db():
    """
        Import a database and replace the existant.
        :return: status in JSON
    """
    try:
        f = request.files["file"]
        assert f.read(15) == b"SQLite format 3"
        d = "/".join(sys.path[0].split("/")[:-2])
        f.save("/{}/tinycheck.sqlite3".format(d))
        res = {"status": True,
               "message": "Database updated"}
    except:
        res = {"status": False,
               "message": "Error while database upload"}
    return jsonify(res)


@config_bp.route('/list', methods=['GET'])
def list():
    """
        List key, values of the configuration
        :return: configuration in JSON
    """
    res = config.export_config()
    res["backend"]["password"] = ""
    return jsonify(res)
