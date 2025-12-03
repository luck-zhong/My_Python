#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：serial_controller.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午6:14 
"""
from serial_pkg.serial_port import SerialPort
from serial.tools import list_ports
from utils.config import Config


class SerialController:
    def __init__(self, ui):
        """
        ui: 由UI层传入，必须包含 append_text(), show_status(), show_error() 等方法
        """
        self.ui = ui
        self.serial = None
        self.config = Config()

        # 控制选项
        self.hex_mode = False
        self.timestamp = False

    # ----------------------
    # 串口开关管理
    # ----------------------
    def open_port(self, port, baud, parity='N', stopbits=1, bytesize=8):
        try:
            self.serial = SerialPort(
                port=port,
                baudrate=baud,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize
            )
            self.serial.set_rx_callback(self.on_serial_data)
            self.serial.open()
            self.config.set('port', port)
            self.config.set('baudrate', baud)
            self.config.set('parity', parity)
            self.config.set('stopbits', stopbits)
            self.config.set('bytesize', bytesize)

            self.ui.show_status(f"串口已打开：{port}")
        except Exception as e:
            self.ui.show_error(f"打开串口失败: {e}")

    def close_port(self):
        if self.serial:
            self.serial.close()
            self.serial = None
            self.ui.show_status("串口已关闭")

    def get_serial_ports(self):
        return [p.device for p in list_ports.comports()]

    def get_last_config(self):
        """
        返回一个包含上次使用的串口配置的 dict。
        提供合理的默认值，避免缺键报错。
        """
        return {
            "port": self.config.get("port", ""),  # 上次的串口名或空
            "baud": self.config.get("baud", 115200),  # 上次波特率
            "parity": self.config.get("parity", "N"),  # 校验位
            "stopbits": self.config.get("stopbits", 1),  # 停止位
            "bytesize": self.config.get("bytesize", 8),  # 数据位
            "hex_mode": self.config.get("hex_mode", False),
            "timestamp": self.config.get("timestamp", False),
        }

    # ----------------------
    # 发送数据
    # ----------------------
    def send_text(self, text):
        if not self.serial:
            self.ui.show_error("串口未打开")
            return

        if self.hex_mode:
            # HEX → bytes
            try:
                clean = text.replace(" ", "")
                data = bytes.fromhex(clean)
            except ValueError:
                self.ui.show_error("HEX数据格式错误")
                return
        else:
            # 字符串 → bytes
            data = text.encode(errors="ignore")

        try:
            self.serial.send(data)
        except Exception as e:
            self.ui.show_error(f"发送失败: {e}")

    # ----------------------
    # 串口接收回调
    # ----------------------
    def on_serial_data(self, data: bytes):
        """
        串口接收到数据后的回调，由 SerialPort 自动调用
        """
        text = self.parse_received_data(data)
        self.ui.append_text(text)

    # ----------------------
    # 数据格式处理（HEX/Text/时间戳）
    # ----------------------
    def parse_received_data(self, data: bytes) -> str:
        if self.hex_mode:
            # bytes → HEX
            text = " ".join(f"{b:02X}" for b in data)
        else:
            # bytes → string
            text = data.decode(errors="ignore")

        if self.timestamp:
            import time
            t = time.strftime("[%H:%M:%S] ")
            text = t + text

        return text

    # ----------------------
    # 控制选项设置
    # ----------------------
    def set_hex_mode(self, enabled: bool):
        self.hex_mode = enabled
        self.config.set('hex_mode', enabled)

    def set_timestamp_mode(self, enabled: bool):
        self.timestamp = enabled
        self.config.set('timestamp', enabled)
