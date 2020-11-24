#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyudev
import psutil
import shutil
import re
import io
from os import mkdir
from datetime import datetime
from flask import jsonify, send_file


class Save():

    def __init__(self):
        self.mount_point = ""
        return None

    def usb_check(self):
        """
            Check if an USB storage is connected or not.
            :return: a json containing the connection status.
        """
        self.usb_devices = []
        context = pyudev.Context()
        removable = [device for device in context.list_devices(
            subsystem='block', DEVTYPE='disk')]
        for device in removable:
            if "usb" in device.sys_path:
                partitions = [device.device_node for device in context.list_devices(
                    subsystem='block', DEVTYPE='partition', parent=device)]
                for p in psutil.disk_partitions():
                    if p.device in partitions:
                        self.mount_point = p.mountpoint
                        return jsonify({"status": True,
                                        "message": "USB storage connected"})
        self.mount_point = ""
        return jsonify({"status": False,
                        "message": "USB storage not connected"})

    def save_capture(self, token, method):
        """
            Save the capture to the USB device or push a ZIP
            file to download.
            :return: binary or json.
        """
        if re.match(r"[A-F0-9]{8}", token):
            try:
                if method == "usb":
                    cd = datetime.now().strftime("%d%m%Y-%H%M")
                    if shutil.make_archive("{}/TinyCheck_{}".format(self.mount_point, cd), "zip", "/tmp/{}/".format(token)):
                        return jsonify({"status": True,
                                        "message": "Capture saved on the USB key"})
                elif method == "url":
                    cd = datetime.now().strftime("%d%m%Y-%H%M")
                    if shutil.make_archive("/tmp/TinyCheck_{}".format(cd), "zip", "/tmp/{}/".format(token)):
                        with open("/tmp/TinyCheck_{}.zip".format(cd), "rb") as f:
                            return send_file(
                                io.BytesIO(f.read()),
                                mimetype="application/octet-stream",
                                as_attachment=True,
                                attachment_filename="TinyCheck_{}.zip".format(cd))
            except:
                return jsonify({"status": False,
                                "message": "Error while saving capture"})
        else:
            return jsonify({"status": False,
                            "message": "Bad token value"})
