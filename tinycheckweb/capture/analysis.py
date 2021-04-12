import os
import sys
import json
import subprocess as sp
from flask import current_app, jsonify


class Analysis(object):

    def __init__(self, token):
        self.token = token

    def start(self):
        """
            Start an analysis of the captured communication by lauching
            analysis.py with the capture token as a paramater.

            :return: dict containing the analysis status
        """

        if self.token is not None:
            parent = current_app.root_path
            sp.Popen(
                [sys.executable, "{}/analysis/analysis.py".format(parent), "/tmp/{}".format(self.token)])

            return {"message": "Analysis started"}
        else:
            return {"message": "Bad token provided"}

    def get_report(self):
        """Get the full report in JSON Format"""
        report = {}
        if os.path.isfile("/tmp/{}/report.json".format(self.token)):
            with open("/tmp/{}/report.json".format(self.token), "r") as f:
                report = json.load(f)
        else:
            return jsonify(message="No report yet !")

        return report
