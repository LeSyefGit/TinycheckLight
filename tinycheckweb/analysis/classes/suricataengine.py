#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import get_iocs, get_config
import time
import os
import subprocess as sp
import re
import json
import sys




class SuricataEngine():

    def __init__(self, capture_directory):

        self.wdir = capture_directory
        self.alerts = []
        self.rules_file = "/tmp/rules.rules"
        self.pcap_path = os.path.join(self.wdir, "capture.pcap")
        self.rules = [r[0] for r in get_iocs("snort")]

        self.userlang = get_config(("frontend", "user_lang"))

        # Load template language
        if not re.match("^[a-z]{2,3}$", self.userlang):
            self.userlang = "en"
        with open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "locales/{}.json".format(self.userlang))) as f:
            self.template = json.load(f)["alerts"]

    def start_suricata(self):
        """
            Launch suricata against the capture.pcap file.
            :return: nothing.
        """

        # Generate the rule file and launch suricata.
        if self.generate_rule_file():
            sp.Popen(["suricata", "-S", self.rules_file, "-r",
                      self.pcap_path, "-l", "/tmp/"]).wait()


    def generate_rule_file(self):
        """
            Generate the rules file passed to suricata.
            :return: bool if operation succeed.
        """
        try:
            with open(self.rules_file, "w+") as f:
                f.write("\n".join(self.rules))
                return True
        except:
            return False

    def get_alerts(self):
        return [dict(t) for t in {tuple(d.items()) for d in self.alerts}]
