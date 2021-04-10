#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory, jsonify, redirect
from app.blueprints.analysis import analysis_bp
from app.blueprints.misc import misc_bp
from app.blueprints.update import update_bp
from app.utils import read_config

app = Flask(__name__)

UPLOAD_FOLDER = "analysis/capture/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


# API Blueprints.
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(misc_bp, url_prefix='/api/misc')
app.register_blueprint(update_bp, url_prefix='/api/update')

if __name__ == '__main__':
    # if read_config(("frontend", "remote_access")):
    #     app.run(host="0.0.0.0", port=8080, debug=True)
    # else:
    app.run(port=8080, debug=True)
