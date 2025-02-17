#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exercise 
@File    ：Temperature_conversion.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/2/17 下午10:45 
"""


def temp_conversion(temp: float) -> float:
    c_temp = (temp - 32) * 5 / 4
    return c_temp


if __name__ == '__main__':
    f_temp = float(input('请输入要转换的华氏度：'))
    print(f'{f_temp}应该转换为{temp_conversion(f_temp)}°')
