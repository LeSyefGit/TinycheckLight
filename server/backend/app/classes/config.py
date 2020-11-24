#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import sys
import io
import os
import re
import hashlib
from functools import reduce
from flask import send_file


class Config(object):
    def __init__(self):
        self.dir = "/".join(sys.path[0].split("/")[:-2])
        return None

    def read_config(self, path):
        """
            Read a single value from the configuration
            :return: value (it can be any type)
        """
        config = yaml.load(
            open(os.path.join(self.dir, "config.yaml"), "r"), Loader=yaml.SafeLoader)
        return reduce(dict.get, path, config)

    def export_config(self):
        """
            Export the configuration
            :return: dict (configuration content)
        """
        config = yaml.load(
            open(os.path.join(self.dir, "config.yaml"), "r"), Loader=yaml.SafeLoader)
        config["interfaces"] = self.get_wireless_interfaces()
        return config

    def write_config(self, cat, key, value):
        """
            Write a new value in the configuration
            :return: bool, operation status
        """
        config = yaml.load(
            open(os.path.join(self.dir, "config.yaml"), "r"), Loader=yaml.SafeLoader)
        config[cat][key] = value if key != "password" else self.make_password(
            value)

        if cat == "network" and key == "in":
            self.edit_configuration_files(value)

        with open(os.path.join(self.dir, "config.yaml"), "w") as yaml_file:
            yaml_file.write(yaml.dump(config, default_flow_style=False))
            return True

    def make_password(self, clear_text):
        """
            Make a simple password hash (without salt)
        """
        return hashlib.sha256(clear_text.encode()).hexdigest()

    def export_db(self):
        """
            Export the database.
            :return: send_file (the database)
        """
        with open(os.path.join(self.dir, "tinycheck.sqlite3"), "rb") as f:
            return send_file(
                io.BytesIO(f.read()),
                mimetype="application/octet-stream",
                as_attachment=True,
                attachment_filename='tinycheck-export-db.sqlite')

    def get_wireless_interfaces(self):
        """
            List the Wireless interfaces installed on the box
            :return: list of the interfaces
        """
        try:
            return [i for i in os.listdir("/sys/class/net/") if i.startswith("wlan")]
        except:
            return ["Fake iface1", "Fake iface 2"]

    def edit_configuration_files(self, iface):
        """
            Edit the DNSMasq and DHCPCD configuration files
            :return: nothing.
        """
        try:
            if re.match("^wlan[0-9]{1}$", iface):
                # Edit of DHCPD.conf
                with open("/etc/dhcpcd.conf", 'r') as file:
                    content = file.readlines()
                for i, line in enumerate(content):
                    if line.startswith("interface"):
                        content[i] = "interface {}\n".format(iface)
                with open("/etc/dhcpcd.conf", 'w') as file:
                    file.writelines(content)
                # Edit of DNSMASQ.conf
                with open("/etc/dnsmasq.conf", 'r') as file:
                    content = file.readlines()
                for i, line in enumerate(content):
                    if line.startswith("interface"):
                        content[i] = "interface={}\n".format(iface)
                with open("/etc/dnsmasq.conf", 'w') as file:
                    file.writelines(content)
        except:
            pass
