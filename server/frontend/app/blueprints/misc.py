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
    if read_config(("frontend", "reboot_option")):
        sp.Popen("shutdown -r now", shell=True)
        return jsonify({"mesage": "Let's reboot."})
    else:
        return jsonify({"message": "Option disabled", "status": False})


@misc_bp.route("/quit", methods=["GET"])
def api_quit():
    """ 
        Quit the interface (Chromium browser) 
    """
    if read_config(("frontend", "quit_option")):
        sp.Popen('pkill -INT -f "chromium-browser"', shell=True)
        return jsonify({"message": "Let's quit", "status": True})
    else:
        return jsonify({"message": "Option disabled", "status": False})


@misc_bp.route("/shutdown", methods=["GET"])
def api_shutdown():
    """ 
        Reboot the device 
    """
    if read_config(("frontend", "shutdown_option")):
        sp.Popen("shutdown -h now", shell=True)
        return jsonify({"message": "Let's shutdown", "status": True})
    else:
        return jsonify({"message": "Option disabled", "status": False})


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
        "quit_option": read_config(("frontend", "quit_option")),
        "shutdown_option": read_config(("frontend", "shutdown_option")),
        "reboot_option": read_config(("frontend", "reboot_option"))
    })
