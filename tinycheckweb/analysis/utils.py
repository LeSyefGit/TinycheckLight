#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import yaml
import sys
import json
import os
from functools import reduce
sys.path.append(os.path.abspath('./'))

from tinycheckweb.models import IOC, Whitelist
from flask import current_app

# I'm not going to use an ORM for that.
parent = "/".join(sys.path[0].split("/")[:-1])
# conn = sqlite3.connect(os.path.join(parent, "tinycheck.sqlite3"))
# cursor = conn.cursor()


def get_iocs(ioc_type):
    """
        Get a list of IOCs specified by their type.
        :return: list of IOCs
    """
    # print(vars(current_app))
    # cursor.execute(
    #     "SELECT value, tag FROM iocs WHERE type = ? ORDER BY value", (ioc_type,))
    # res = cursor.fetchall()
    res = IOC.query.filter_by(type=ioc_type).all()

    return [[r.value, r.tag] for r in res] if res is not None else []


def get_whitelist(elem_type):
    """
        Get a list of whitelisted elements specified by their type.
        :return: list of elements
    """
    # cursor.execute(
    #     "SELECT element FROM whitelist WHERE type = ? ORDER BY element", (elem_type,))
    # res = cursor.fetchall()
    res = Whitelist.query.filter_by(type=elem_type).all()
    return [r.element for r in res] if res is not None else []


def get_config(path):
    """
        Read a value from the configuration
        :return: value (it can be any type)
    """
    config = yaml.load(open(os.path.join(parent, "config.yaml"),
                            "r"), Loader=yaml.SafeLoader)
    return reduce(dict.get, path, config)



