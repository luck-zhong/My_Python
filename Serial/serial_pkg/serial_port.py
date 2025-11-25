#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：serial_port.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午5:55 
"""

import threading
import serial
import time


class SerialPort:
    def __init__(self, port=None, baudrate=115200, parity='N', stopbits=1, bytesize=8):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize

        self.ser = None
        self.rx_thread = None
        self.is_running = False

        self.rx_callback = None  # 重点：接收回调函数

    def open(self):
        """打开串口"""
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=0.1
        )
        self.is_running = True
        self.start_rx_thread()

    def close(self):
        """关闭串口"""
        self.is_running = False
        if self.rx_thread and self.rx_thread.is_alive():
            self.rx_thread.join()

        if self.ser and self.ser.is_open:
            self.ser.close()

    def send(self, data: bytes):
        """发送数据"""
        if self.ser and self.ser.is_open:
            self.ser.write(data)

    def start_rx_thread(self):
        """启动接收线程"""
        self.rx_thread = threading.Thread(target=self._rx_loop, daemon=True)
        self.rx_thread.start()

    def _rx_loop(self):
        """接收线程函数"""
        while self.is_running:
            if self.ser.in_waiting:
                data = self.ser.read(self.ser.in_waiting)

                # 如果上层注册了回调函数，就调用它
                if self.rx_callback:
                    self.rx_callback(data)

            time.sleep(0.01)

    def set_rx_callback(self, func):
        """设置接收回调函数"""
        self.rx_callback = func
