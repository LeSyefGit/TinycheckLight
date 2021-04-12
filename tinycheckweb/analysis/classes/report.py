import weasyprint
import os
import json
import hashlib
import re
import sys

from weasyprint import HTML
from pathlib import Path
from datetime import datetime
from utils import get_config


class Report(object):

    def __init__(self, capture_directory):
        self.capture_directory = capture_directory
        self.alerts = self.read_json(os.path.join(
            capture_directory, "assets/alerts.json"))
        self.whitelist = self.read_json(os.path.join(
            capture_directory, "assets/whitelist.json"))
        self.conns = self.read_json(os.path.join(
            capture_directory, "assets/conns.json"))
        try:
            with open(os.path.join(self.capture_directory, "capture.pcap"), "rb") as f:
                self.capture_sha1 = hashlib.sha1(f.read()).hexdigest()
        except:
            self.capture_sha1 = "N/A"

        self.userlang = get_config(("frontend", "user_lang"))

        # Load template language
        if not re.match("^[a-z]{2,3}$", self.userlang):
            self.userlang = "en"
        with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "locales/{}.json".format(self.userlang))) as f:
            self.template = json.load(f)["report"]

    def read_json(self, json_path):
        """
            Read and convert a JSON file.
            :return: array or dict.
        """
        with open(json_path, "r") as json_file:
            return json.load(json_file)
    

    def generate_report(self):
        """
            Generate the full report in Json format
            :return: Json
        """
        content1 = self.generate_warning()
        content2 = self.generate_alerts() 
        content3 = {"suspect_communication":self.generate_suspect_conns_block()}
        content4 = {"whitelist":self.generate_whitelist_block()}
       
        content = {**content1, **content2, **content3, **content4}
        return json.dumps(content)
        
        
       
    def generate_warning(self):
        """
            Generate the warning message.
            :return: str
        """
        if len(self.alerts["high"]):
            msg = {"warning":{"high":self.template["high_msg"].format(
                self.nb_translate(len(self.alerts["high"])))}}
            
            return msg
        elif len(self.alerts["moderate"]):
            msg = {"warning":{"moderate":self.template["moderate_msg"].format(
                self.nb_translate(len(self.alerts["moderate"])))}}
            return msg
        elif len(self.alerts["low"]):
            msg = {"warning":{"low":self.template["low_msg"].format(
                self.nb_translate(len(self.alerts["low"])))}}
            return msg
        else:
           
            msg = {"warning":self.template["none_msg"]}
            return msg

    def nb_translate(self, nb):
        """
            Translate a number in a string.
            :return: str
        """
        a = self.template["numbers"]
        return a[nb-1] if nb <= 9 else str(nb)

    def generate_suspect_conns_block(self):
        """
            Generate the table of the network non-whitelisted communications.
            :return: string
        """
        return self.conns

    def generate_whitelist_block(self):
        """
            Generate the table of the whitelisted communications.
            :return: string
        """
        return self.whitelist

    def generate_alerts(self):
        """
            Generate the alerts.
            :return: string
        """
        alert1={}
        alert2={}
        alert3={}
        for alert in self.alerts["high"]:
            alert1= {
                "level":"High",
                "alert-id":alert["id"],
                "alert-title":alert["title"],
                "alert-description":alert["description"]
            }

        for alert in self.alerts["moderate"]:
             alert2 = {
                "level":"Moderate",
                "alert-id":alert["id"],
                "alert-title":alert["title"],
                "alert-description":alert["description"]
            }
         
        for alert in self.alerts["low"]:
             alert2= {
                "level":"Low",
                "alert-id":alert["id"],
                "alert-title":alert["title"],
                "alert-description":alert["description"]
            }
        
        alerts = {"alerts":{**alert1,**alert2, **alert3}}
        return alerts

   
