#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：converter.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午6:34 
"""
# utils/converter.py

def bytes_to_hex(data: bytes) -> str:
    """将 bytes 转成 02X 格式的 HEX 字符串"""
    return " ".join(f"{b:02X}" for b in data)


def hex_to_bytes(text: str) -> bytes:
    """将 HEX 字符串转成 bytes，自动过滤空格"""
    clean = "".join(text.split())
    return bytes.fromhex(clean)


def safe_decode(data: bytes) -> str:
    """安全解码 bytes → string，忽略非法字符"""
    return data.decode(errors="ignore")


def is_valid_hex(text: str) -> bool:
    """检查一段字符串是不是有效 HEX"""
    clean = text.replace(" ", "")
    try:
        int(clean, 16)
        return True
    except ValueError:
        return False
