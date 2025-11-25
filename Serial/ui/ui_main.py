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

        tk.Label(top_frame, text="串口号:").pack(side="left")
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(top_frame, textvariable=self.port_var, width=10)
        self.port_combo['values'] = self.controller.get_serial_ports()
        self.port_combo.pack(side="left", padx=5)

        tk.Label(top_frame, text="波特率:").pack(side="left")
        self.baud_var = tk.StringVar(value="115200")
        self.baud_combo = ttk.Combobox(top_frame, textvariable=self.baud_var, width=10)
        self.baud_combo['values'] = ["9600", "19200", "38400", "57600", "115200", "230400"]
        self.baud_combo.pack(side="left", padx=5)

        self.open_btn = tk.Button(top_frame, text="打开串口", command=self.on_open_clicked)
        self.open_btn.pack(side="left", padx=5)

        # --- 设置区域 ---
        set_frame = tk.Frame(self.root)
        set_frame.pack(fill="x")

        self.hex_var = tk.BooleanVar()
        tk.Checkbutton(set_frame, text="HEX", variable=self.hex_var,
                       command=self.on_hex_changed).pack(side="left")

        self.timestamp_var = tk.BooleanVar()
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

    def on_hex_changed(self):
        self.controller.set_hex_mode(self.hex_var.get())

    def on_timestamp_changed(self):
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
