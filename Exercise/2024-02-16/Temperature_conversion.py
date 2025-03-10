#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exercise 
@File    ：Temperature_conversion.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/2/17 下午10:45 
"""


# 输入的华氏度转换为摄氏度
def temp_conversion():
    f_temp = float(input('请输入要转换的华氏度：'))
    c_temp = (f_temp - 32) * 5 / 4
    print(f'{f_temp}应该转换为{c_temp}°')


# 反转字符串
def string_covert():
    s_convert = input('请输入要反转的字符串：')
    s = s_convert[::-1]
    print(f'{s_convert}反转后为：{s}')
    if s_convert == s:
        print('该字符串是回文！')
    else:
        print('该字符串不是回文！')


# 首字母大写
def string_total():
    input_string = "hello world!"
    print(input_string.title())


# 变位词
def change_string():
    s1_string = input('请输入字符串1：')
    s2_string = input('请输入字符串2：')
    num = 0
    if len(s1_string) == len(s2_string):
        for i in range(len(s1_string)):
            for j in range(len(s2_string)):
                if s1_string[i] == s2_string[j]:
                    num += 1
        if num == len(s2_string):
            print(f'{s1_string}和{s2_string}是变位词!')
        else:
            print(f'{s1_string}和{s2_string}不是变位词!')
    else:
        print(f'{s1_string}和{s2_string}不是变位词!')

    # 输入两个字符串
    # str1 = "eleven plus two"
    # str2 = "twelve plus one"
    # 将字符串转为小写并排序后比较
    # print(sorted(str1.lower()) == sorted(str2.lower()))


# 最大相同字符长度
def simple_string():
    s_string = input('请输入字符串：')
    current_len = 1
    max_len = 1
    char = s_string[0]
    for s in s_string[1:]:
        if s == char:
            current_len += 1
        else:
            max_len = max(current_len, max_len)
            current_len = 1
            char = s
    print(f'最大相同字符长度为{max_len}')


if __name__ == '__main__':
    fruits = ['苹果', '香蕉', '桔子']

    for fruit in fruits:
        fruits[2:2] = '西瓜'
        print(fruit)