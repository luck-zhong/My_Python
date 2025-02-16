#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exercise 
@File    ：Calculate_area.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/2/16 下午8:09 
"""
import math
PI = 3.14
def calculate_area(r:int) ->int:
    try:
        return PI * r**2
    except ValueError as e:
        print('半径r不能小于0')

if __name__ == '__main__':
    r = int(input('请输入要计算圆面积的半径大小：'))
    print(f'圆面积为:{calculate_area(r)}')
