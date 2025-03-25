#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Exercise 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/3/25 下午9:08 
"""
import random


class Games:
    count = 1

    def __init__(self, begin, end):
        self._begin = begin
        self._end = end

    # 随机返回一个猜测正确的值
    def right_int(self):
        return random.randint(self._begin, self._end)

    def guess_process(self):
        right_value = self.right_int()
        print(f'要猜测的值为{right_value}')
        low, high = self._begin, self._end  # 初始化搜索范围
        while True:
            value = (low + high) // 2
            if value > right_value:
                high = value - 1
                print('Try Again! you guessed too high')
            elif value < right_value:
                low = value + 1
                print('Try Again! you guessed too small')
            else:
                print('Successful! you guessed right')
                break
            Games.count += 1


def user_play():
    begin = int(input('请输入猜数字的起始范围：'))
    end = int(input('请输入猜数字的结束范围：'))
    game = Games(begin, end)
    game.guess_process()
    print(Games.count)


if __name__ == '__main__':
    user_play()
