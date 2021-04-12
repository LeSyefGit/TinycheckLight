#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import yaml
import sys
import json
import os
from functools import reduce
from flask import current_app


#add the root path of application to syspath to be able to import 
#element from tinycheckweb module as shown below
sys.path.append(os.path.abspath('./'))

from tinycheckweb.models import IOC, Whitelist

parent = "/".join(sys.path[0].split("/")[:-1])

def get_iocs(ioc_type):
    """
        Get a list of IOCs specified by their type.
        :return: list of IOCs
    """
    res = IOC.query.filter_by(type=ioc_type).all()
    return [[r.value, r.tag] for r in res] if res is not None else []


def get_whitelist(elem_type):
    """
        Get a list of whitelisted elements specified by their type.
        :return: list of elements
    """
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



