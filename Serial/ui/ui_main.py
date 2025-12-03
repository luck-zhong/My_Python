#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Serial 
@File    ：ui_main.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/11/25 下午6:39 
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class SerialUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("串口助手 - Python")
        self.root.geometry("700x500")

        self.build_ui()

    # --------------------------
    # UI 构建
    # --------------------------
    def build_ui(self):
        # --- 顶部串口区域 ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=5)

        # 左侧：端口选择、开关按钮
        left_frame = tk.Frame(top_frame)
        left_frame.pack(side="left", fill="x", expand=True)
        tk.Label(left_frame, text="串口号:").pack(side="left")
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(left_frame, textvariable=self.port_var, width=10)
        self.port_combo['values'] = self.controller.get_serial_ports()
        self.port_combo.pack(side="left", padx=5)
        self.open_btn = tk.Button(left_frame, text="打开串口", command=self.on_open_clicked)
        self.open_btn.pack(side="left", padx=5)
        self.open_btn = tk.Button(left_frame, text="关闭串口", command=self.on_close_clicked)
        self.open_btn.pack(side="left", padx=5)


        last = self.controller.get_last_config()

        # 右侧：连接参数竖排
        params_frame = tk.LabelFrame(top_frame, text="连接参数")
        params_frame.pack(side="right", fill="y", padx=5)

        # 波特率
        baud_row = tk.Frame(params_frame)
        baud_row.pack(fill="x", pady=2)
        tk.Label(baud_row, text="波特率").pack(side="left")
        self.baud_var = tk.StringVar(value=self.controller.get_last_config().get("baud", 115200))
        self.baud_combo = ttk.Combobox(baud_row, textvariable=self.baud_var, width=10)
        self.baud_combo['values'] = ["9600", "19200", "38400", "57600", "115200", "230400"]
        self.baud_combo.pack(side="left", padx=5)

        # 校验位
        parity_row = tk.Frame(params_frame)
        parity_row.pack(fill="x", pady=2)
        tk.Label(parity_row, text="校验位").pack(side="left")
        self.parity_var = tk.StringVar(value=self.controller.get_last_config().get("parity", "N"))
        self.parity_combo = ttk.Combobox(parity_row, textvariable=self.parity_var, width=5)
        self.parity_combo['values'] = ["N", "E", "O"]
        self.parity_combo.pack(side="left", padx=5)

        # 停止位
        stop_row = tk.Frame(params_frame)
        stop_row.pack(fill="x", pady=2)
        tk.Label(stop_row, text="停止位").pack(side="left")
        self.stop_var = tk.StringVar(value=str(self.controller.get_last_config().get("stopbits", 1)))
        self.stop_combo = ttk.Combobox(stop_row, textvariable=self.stop_var, width=5)
        self.stop_combo['values'] = ["1", "1.5", "2"]
        self.stop_combo.pack(side="left", padx=5)

        # 数据位
        data_row = tk.Frame(params_frame)
        data_row.pack(fill="x", pady=2)
        tk.Label(data_row, text="数据位").pack(side="left")
        self.bytesize_var = tk.StringVar(value=str(self.controller.get_last_config().get("bytesize", 8)))
        self.bytesize_combo = ttk.Combobox(data_row, textvariable=self.bytesize_var, width=5)
        self.bytesize_combo['values'] = ["5", "6", "7", "8"]
        self.bytesize_combo.pack(side="left", padx=5)



        # --- 设置区域 ---
        set_frame = tk.Frame(self.root)
        set_frame.pack(fill="x")

        self.hex_var = tk.BooleanVar(value=last.get("hex_mode", False))
        tk.Checkbutton(set_frame, text="HEX", variable=self.hex_var,
                       command=self.on_hex_changed).pack(side="left")

        self.timestamp_var = tk.BooleanVar(value=last.get("timestamp", False))
        tk.Checkbutton(set_frame, text="时间戳", variable=self.timestamp_var,
                       command=self.on_timestamp_changed).pack(side="left")

        tk.Button(set_frame, text="清屏", command=self.on_clear_clicked).pack(side="right")

        # --- 接收窗口 ---
        recv_frame = tk.Frame(self.root)
        recv_frame.pack(fill="both", expand=True, pady=5)

        self.recv_text = tk.Text(recv_frame, wrap="word")
        self.recv_text.pack(fill="both", expand=True)

        # --- 发送区域 ---
        send_frame = tk.Frame(self.root)
        send_frame.pack(fill="x")

        self.send_entry = tk.Entry(send_frame)
        self.send_entry.pack(side="left", fill="x", expand=True, padx=5)

        tk.Button(send_frame, text="发送", command=self.on_send_clicked).pack(side="right")

        # --- 状态栏 ---
        self.status_var = tk.StringVar(value="状态：就绪")
        status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w")
        status_label.pack(fill="x")

    # --------------------------
    # UI 回调（传给 Controller）
    # --------------------------
    def on_open_clicked(self):
        port = self.port_var.get()
        baud = int(self.baud_var.get())
        self.controller.open_port(port, baud)

    def on_close_clicked(self):
        self.controller.close_port()

    def on_hex_changed(self):
        self.controller.config.set('hex_mode', self.hex_var.get())
        self.controller.set_hex_mode(self.hex_var.get())

    def on_timestamp_changed(self):
        self.controller.config.set('timestamp', self.timestamp_var.get())
        self.controller.set_timestamp_mode(self.timestamp_var.get())

    def on_send_clicked(self):
        text = self.send_entry.get()
        self.controller.send_text(text)

    def on_clear_clicked(self):
        self.recv_text.delete("1.0", tk.END)

    # --------------------------
    # Controller 调用的 UI 方法
    # --------------------------
    def append_text(self, text):
        self.recv_text.insert(tk.END, text + "\n")
        self.recv_text.see(tk.END)

    def show_status(self, msg):
        self.status_var.set(f"状态：{msg}")

    def show_error(self, msg):
        messagebox.showerror("错误", msg)
