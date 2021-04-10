#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess as sp
import json
import sys
import re
import os
from flask import current_app

class Analysis(object):

    # def __init__(self, token):
    #     self.token = token if re.match(r"[A-F0-9]{8}", token) else None

    def start(self):
        """
            Start an analysis of the captured communication by lauching
            analysis.py with the capture token as a paramater.

            :return: dict containing the analysis status
        """

       
        # parent = "/".join(sys.path[0].split("/")[:-2])
        parent = current_app.root_path+"/../../"
        sp.Popen(
            [sys.executable, "{}/analysis/analysis.py".format(parent),"{}/analysis/capture".format(parent)])
        
        # Load the report 
        if os.path.isfile("{}/analysis/capture/report.json".format(parent)):
            with open("{}/analysis/capture/report.json".format(parent), "r") as f:
                report = json.load(f)
        return report
    

    # def get_report(self):
    #     """
    #         Generate a small json report of the analysis
    #         containing the alerts and the device properties.

    #         :return: dict containing the report or error message.
    #     """

    #     alerts = {}, {}

    #     # # Getting device configuration.
    #     # if os.path.isfile("/tmp/{}/assets/device.json".format(self.token)):
    #     #     with open("/tmp/{}/assets/device.json".format(self.token), "r") as f:
    #     #         device = json.load(f)

    #     # Getting alerts configuration.
    #     parent = "/".join(sys.path[0].split("/")[:-2])
    #     if os.path.isfile("{}/analysis/capture/alerts.json".format(parent)):
    #         with open("{}/analysis/capture/alerts.json".format(parent), "r") as f:
    #             alerts = json.load(f)

    #     if alerts != {}:
    #         return {"alerts": alerts}
    #     else:
    #         return {"message": "No report yet"}
