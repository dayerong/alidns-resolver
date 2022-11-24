#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   read_yaml.py
@Time    :   2022/11/23
@Author  :   chenrong
@Version :   1.0
@Contact :   chr@cuanon.com
@Desc    :   
"""

import yaml

config_file = "./config/conf.yaml"


def read_config(key):
    with open(config_file, encoding='utf-8') as fp:
        content = yaml.load(fp, Loader=yaml.FullLoader)
        return content[key]
