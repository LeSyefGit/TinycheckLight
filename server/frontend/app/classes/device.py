#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re


class Device(object):

    def __init__(self, token):
        self.token = token if re.match(r"[A-F0-9]{8}", token) else None
        return None

    def get(self):
        """
            Get the device properties (such as Mac address, name, IP etc.)
            By reading the device.json file if exists. Or reading
            the leases files and writing the result into device.json. 

            :return: dict containing device properties.
        """
        if not os.path.isfile("/tmp/{}/device.json".format(self.token)):
            device = self.read_leases()
            if device["status"] != False:
                with open("/tmp/{}/device.json".format(self.token), "w") as f:
                    f.write(json.dumps(device))
        else:
            with open("/tmp/{}/device.json".format(self.token)) as f:
                device = json.load(f)
        return device

    @staticmethod
    def read_leases():
        """
            Read the DNSMasq leases files to retrieve
            the connected device properties. 

            :return: dict containing device properties.
        """
        with open("/var/lib/misc/dnsmasq.leases") as f:
            for line in f.readlines():
                return {
                    "status": True,
                    "name": line.split(" ")[3],
                    "ip_address": line.split(" ")[2],
                    "mac_address": line.split(" ")[1],
                    "timestamp": int(line.split(" ")[0])
                }
            else:
                return {"status": False,
                        "message": "Device not connected"}
