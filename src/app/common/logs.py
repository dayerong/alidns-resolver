#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   logs.py
@Time    :   2022/11/23
@Author  :   chenrong
@Version :   1.0
@Contact :   chr@cuanon.com
@Desc    :   
"""

import logging
import os
from .read_yaml import read_config


class Log(object):
    def __init__(self):
        self.logformat = read_config('logging')['logformat']
        self.filename = read_config('logging')['file']
        self.datefmt = read_config('logging')['datefmt']

    def info(self, loggername, logcontent):
        path = self.filename[0:self.filename.rfind("/")]
        if not os.path.isdir(path):
            os.makedirs(path)

        if not os.path.isfile(self.filename):
            f = open(self.filename, 'w')
            f.close()

        logging.basicConfig(filename=self.filename, format=self.logformat, datefmt=self.datefmt)
        logger = logging.getLogger(loggername)
        logger.setLevel(20)
        logger.info(logcontent)

    def error(self, loggername, logcontent):
        path = self.filename[0:self.filename.rfind("/")]
        if not os.path.isdir(path):
            os.makedirs(path)

        if not os.path.isfile(self.filename):
            f = open(self.filename, 'w')
            f.close()

        logging.basicConfig(filename=self.filename, format=self.logformat, datefmt=self.datefmt)
        logger = logging.getLogger(loggername)
        logger.setLevel(40)
        logger.error(logcontent)
