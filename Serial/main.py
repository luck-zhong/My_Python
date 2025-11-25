#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：ui.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午6:38 
"""
import tkinter as tk
from controller.serial_controller import SerialController
from ui.ui_main import SerialUI


def main():
    root = tk.Tk()
    controller = SerialController(None)  # 或者先放 None，稍后再 set
    ui = SerialUI(root, controller)
    controller.ui = ui  # 建立反向引用
    root.mainloop()


if __name__ == "__main__":
    main()
