#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：cmis_test 
@File    ：image_select.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/5/17 下午6:14 
"""
from environment import Environment
import os
import UI

dir_path = Environment.get_base_path(UI.__file__)
image_path = os.path.join(dir_path, 'images')


class Image_select(object):
    @staticmethod
    def get_image(name):
        return os.path.join(image_path, name)
