#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：cmis_test 
@File    ：environment.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/5/17 下午5:55 
"""
import os


class Environment(object):
    @staticmethod
    def get_base_path(path):
        return os.path.dirname(os.path.abspath(path))

    @staticmethod
    def get_application_dir():
        return os.getcwd()
