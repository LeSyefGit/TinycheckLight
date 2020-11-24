#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import sys
import os
from functools import reduce


def read_config(path):
    """
        Read a value from the configuration
        :return: value (it can be any type)
    """
    dir = "/".join(sys.path[0].split("/")[:-2])
    config = yaml.load(open(os.path.join(dir, "config.yaml"), "r"),
                       Loader=yaml.SafeLoader)
    return reduce(dict.get, path, config)


def write_config(cat, key, value):
    """
        Write a new value in the configuration
        :return: bool, operation status
    """
    try:
        dir = "/".join(sys.path[0].split("/")[:-2])
        config = yaml.load(open(os.path.join(dir, "config.yaml"),
                                "r"), Loader=yaml.SafeLoader)
        config[cat][key] = value
        with open(os.path.join(dir, "config.yaml"), "w") as yaml_file:
            yaml_file.write(yaml.dump(config, default_flow_style=False))
            return True
    except:
        return False
