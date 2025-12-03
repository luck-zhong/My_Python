#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：config.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午6:34 
"""
# utils/config.py

import json
import os


class Config(object):
    def __init__(self, file="config.json"):
        self.file = file
        self.data = {}

        if os.path.exists(file):
            self.load()

    def load(self):
        with open(self.file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()
