#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess as sp
from flask import Blueprint, jsonify
from app.utils import read_config

misc_bp = Blueprint("misc", __name__)


@misc_bp.route("/reboot", methods=["GET"])
def api_reboot():
    """ 
        Reboot the device 
    """
    sp.Popen("reboot", shell=True)
    return jsonify({"mesage": "Let's reboot."})


@misc_bp.route("/config", methods=["GET"])
def get_config():
    """ 
        Get configuration keys relative to the GUI 
    """
    return jsonify({
        "virtual_keyboard": read_config(("frontend", "virtual_keyboard")),
        "hide_mouse": read_config(("frontend", "hide_mouse")),
        "download_links": read_config(("frontend", "download_links")),
        "sparklines": read_config(("frontend", "sparklines")),
    })
