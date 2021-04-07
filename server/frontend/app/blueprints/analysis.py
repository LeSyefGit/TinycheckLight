#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import sys
from flask import Blueprint, jsonify, current_app, request
from werkzeug.utils import secure_filename
from app.classes.analysis import Analysis
import subprocess as sp
import json

ALLOWED_EXTENSIONS = {'pcap'}

analysis_bp = Blueprint("analysis", __name__)


# @analysis_bp.route("/start/<token>", methods=["GET"])
# def api_start_analysis(token):
#     """ 
#         Start an analysis
#     """
#     return jsonify(Analysis(token).start())


# @analysis_bp.route("/report/<token>", methods=["GET"])
# def api_report_analysis(token):
#     """ 
#         Get the report of an analysis
#     """
#     return jsonify(Analysis(token).get_report())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analysis_bp.route("/start", methods=["POST"])
def api_start_analysis():
     if request.method == 'POST':
        # check if the post request has the file part
        if 'capture' not in request.files:
            return {"error":"No file part"}

        file = request.files['capture']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
           return {"error":"No selected file"}

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            # print(repr(current_app.root_path))
            report = Analysis().start()
            return report
