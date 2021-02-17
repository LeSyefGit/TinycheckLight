#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify, Blueprint
from app.classes.update import Update

update_bp = Blueprint("update", __name__)


@update_bp.route("/check", methods=["GET"])
def check():
    """ Check the presence of new version """
    return jsonify(Update().check_version())


@update_bp.route("/process", methods=["GET"])
def process():
    """ Check the presence of new version """
    return jsonify(Update().update_instance())
