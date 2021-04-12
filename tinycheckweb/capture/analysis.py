import os,sys,json
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
            # parent = "/".join(sys.path[0].split("/")[:-2])
            parent = current_app.root_path
            sp.Popen(
                [sys.executable, "{}/analysis/analysis.py".format(parent), "/tmp/{}".format(self.token)])
            
            return {"status": True,
                    "message": "Analysis started",
                    "token": self.token}
        else:
            return {"status": False,
                    "message": "Bad token provided",
                    "token": "null"}

    def get_report(self):
        report = {}
        if os.path.isfile("/tmp/{}/report.json".format(self.token)):
            with open("/tmp/{}/report.json".format(self.token), "r") as f:
                report = json.load(f)
        else:
            return jsonify(message="No report yet !")
      
        return report
