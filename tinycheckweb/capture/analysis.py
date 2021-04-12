import os,sys,json
import subprocess as sp
from flask import current_app


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
        
        """
            Generate a small json report of the analysis
            containing the alerts and the device properties.

            :return: dict containing the report or error message.
        """

        device, alerts = {}, {}

        # Getting device configuration.
        if os.path.isfile("/tmp/{}/assets/device.json".format(self.token)):
            with open("/tmp/{}/assets/device.json".format(self.token), "r") as f:
                device = json.load(f)

        # Getting alerts configuration.
        if os.path.isfile("/tmp/{}/assets/alerts.json".format(self.token)):
            with open("/tmp/{}/assets/alerts.json".format(self.token), "r") as f:
                alerts = json.load(f)

        if device != {} and alerts != {}:
            return {"alerts": alerts,
                    "device": device}
        else:
            return {"message": "No report yet"}


