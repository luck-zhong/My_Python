#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：logger.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午6:34 
"""
# utils/logger.py

import time
import os

class Logger:
    def __init__(self, filename="serial.log"):
        self.filename = filename

    def log(self, text: str):
        """写一条日志到文件"""
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} {text}\n"

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(line)

    def log_hex(self, data: bytes):
        """写 HEX 数据到文件"""
        hex_str = " ".join(f"{b:02X}" for b in data)
        self.log(f"HEX: {hex_str}")

    def log_raw(self, data: bytes):
        """写文本数据到文件"""
        try:
            txt = data.decode(errors="ignore")
        except:
            txt = str(data)
        self.log(f"RAW: {txt}")
