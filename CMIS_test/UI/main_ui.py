#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：cmis_test 
@File    ：main_ui.py
@IDE     ：PyCharm 
@Author  ：努力赚钱的小钟！
@Date    ：2025/4/23 下午8:32 
"""

import sys
import os
from image_select import Image_select
from environment import Environment
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QToolBar, QVBoxLayout, QWidget, QMenu, QSizePolicy,
                             QToolButton, QProgressBar, QHBoxLayout, QDockWidget, QTextBrowser, QStackedLayout,
                             QPushButton, QTextEdit)
from PyQt6.QtGui import QAction, QIcon, QDesktopServices, QFont, QTextOption


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口属性
        self.setWindowTitle("Cmis 测试程序")
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        app_path = Environment.get_application_dir()
        image_path = os.path.join(app_path, 'App_image', 'app.ico')
        self.setWindowIcon(QIcon(image_path))

        # 创建中心控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 中心布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建 QTextEdit 实例
        text_edit1 = QTextEdit(self)
        text_edit1.setPlainText("这是一个富文本编辑器1。")
        layout.addWidget(text_edit1)

        # 创建 QTextEdit 实例
        text_edit2 = QTextEdit(self)
        text_edit2.setPlainText("这是一个富文本编辑器2。")
        layout.addWidget(text_edit2)

        self.set_ui()

    def set_ui(self):
        # 创建工具栏
        self._create_tool_bar()

        self.setDockNestingEnabled(True)
        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

        # left panel
        self.ui_tree_test_cases = TestCaseTreeDockWidget(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.ui_tree_test_cases)

        # central
        central_widget = QWidget(self)
        self.central_stack_layout = QStackedLayout(central_widget)
        self.central_stack_layout.setContentsMargins(0, 0, 0, 0)
        self.central_stack_layout.setSpacing(0)
        self.listResult = QTextBrowser()
        self.listResult.setFont(QFont(['Consolas'] + self.listResult.font().families()))
        self.listResult.setOpenLinks(False)
        self.listResult.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.listResult.document().setDefaultStyleSheet('a {text-decoration: none;} p {padding: 1px 0;}')
        self.listResult.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.central_stack_layout.addWidget(self.listResult)
        self.listResult.setFocus(Qt.FocusReason.NoFocusReason)
        self.setCentralWidget(central_widget)

        # log output
        bottomDockWidget = QDockWidget(self)
        bottomDockWidget.setWindowTitle('日志输出')
        bottomDockWidget.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                                     QDockWidget.DockWidgetFeature.DockWidgetMovable)
        bottomDockWidget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.listOutput = LogOutputWidget()
        self.listOutput.setMaximumBlockCount(0)
        self.listOutput.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        bottomDockWidget.setWidget(self.listOutput)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, bottomDockWidget)

        # 创建状态栏
        self._create_status_bar()

    def _create_tool_bar(self):
        """创建工具栏"""
        self.tool_bar = QToolBar("主工具栏", self)
        self.tool_bar.setMovable(False)
        self.addToolBar(self.tool_bar)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # 添加全选按钮
        self.select_action = QAction(QIcon(Image_select.get_image('select-all.svg')), '全选', self)
        self.tool_bar.addAction(self.select_action)

        # 添加全不选按钮
        self.unselect_action = QAction(QIcon(Image_select.get_image('unselect-all.svg')), '全不选', self)
        self.tool_bar.addAction(self.unselect_action)
        # 添加分隔线
        self.tool_bar.addSeparator()

        # 添加设置按钮
        self.setting_action = QAction(QIcon(Image_select.get_image('setting.svg')), '设置', self)
        self.tool_bar.addAction(self.setting_action)
        # 添加分隔线
        self.tool_bar.addSeparator()

        # 添加历史日志按钮
        self.log_action = QAction(QIcon(Image_select.get_image('log.svg')), '历史日志', self)
        self.tool_bar.addAction(self.log_action)
        # 添加分隔线
        self.tool_bar.addSeparator()

        # 添加清空结果按钮
        self.clear_action = QAction(QIcon(Image_select.get_image('clear.svg')), '清空结果', self)
        self.tool_bar.addAction(self.clear_action)
        # 添加分隔线
        self.tool_bar.addSeparator()

        # 添加开始测试按钮
        self.run_action = QAction(QIcon(Image_select.get_image('run.svg')), '开始测试', self)
        self.tool_bar.addAction(self.run_action)
        # 添加停止测试按钮
        self.stop_action = QAction(QIcon(Image_select.get_image('stop.svg')), '停止测试', self)
        self.tool_bar.addAction(self.stop_action)
        # 添加强制停止按钮
        self.terminated_action = QAction(QIcon(Image_select.get_image('terminated.svg')), '强制停止', self)
        self.tool_bar.addAction(self.terminated_action)
        # 添加分隔线
        self.tool_bar.addSeparator()

        # 添加终端按钮
        self.terminal_action = QAction(QIcon(Image_select.get_image('terminal.svg')), '终端', self)
        self.tool_bar.addAction(self.terminal_action)
        # 添加分隔线
        self.tool_bar.addSeparator()
        # 添加弹簧撑开空间
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tool_bar.addWidget(spacer)

        # 1. 创建带下拉菜单的检查更新按钮
        self.dropdown_button = QToolButton()
        self.dropdown_button.setText("检查更新")  # 按钮文本
        self.dropdown_button.setIcon(QIcon(Image_select.get_image('check-new-version.svg')))  # 设置图标（替换为实际路径）
        self.dropdown_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)  # 文字在图标下方
        self.dropdown_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)  # 点击箭头弹出菜单
        # 2. 创建下拉菜单
        menu = QMenu(self)
        menu.addAction(QIcon("option1.png"), "选项1", self.on_option1_clicked)
        menu.addAction(QIcon("option2.png"), "选项2", self.on_option2_clicked)
        menu.addSeparator()  # 添加分隔线
        menu.addAction("设置", self.on_settings_clicked)
        # 3. 将菜单关联到按钮
        self.dropdown_button.setMenu(menu)
        # 4. 将按钮添加到工具栏
        self.tool_bar.addWidget(self.dropdown_button)

        # 添加项目源码按钮
        self.code = QAction(QIcon(Image_select.get_image('code.svg')), '项目源码', self)
        self.tool_bar.addAction(self.code)
        # 添加帮助按钮
        self.help_action = QAction(QIcon(Image_select.get_image('help.svg')), '帮助', self)
        self.tool_bar.addAction(self.help_action)

        self.tool_bar.actionTriggered.connect(self.on_toolbar_action)

    def _create_status_bar(self):
        """创建状态栏"""
        self.statusbar = self.statusBar()

        # add general progress bar to status bar
        self.general_progress_bar = QProgressBar()
        self.general_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.general_progress_bar.setMaximumSize(360, 20)
        self.general_progress_bar.setValue(0)
        self.general_progress_bar.setVisible(True)
        self.statusbar.addPermanentWidget(self.general_progress_bar)

        # add test case progress bar to status bar
        self.test_case_progress_bar = QProgressBar()
        self.test_case_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.test_case_progress_bar.setMaximumSize(180, 20)
        self.test_case_progress_bar.setValue(0)
        self.test_case_progress_bar.setVisible(True)
        self.test_case_progress_bar.setFormat('%v/%m')
        self.test_case_progress_bar.setToolTip('Progress of the test case')
        self.statusBar().addPermanentWidget(self.test_case_progress_bar)

        # add test round progress bar to status bar
        self.test_round_progress_bar = QProgressBar()
        self.test_round_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.test_round_progress_bar.setMaximumSize(180, 20)
        self.test_round_progress_bar.setValue(0)
        self.test_round_progress_bar.setVisible(True)
        self.test_round_progress_bar.setFormat('%v/%m')
        self.test_round_progress_bar.setToolTip('Progress of the round')
        self.statusBar().addPermanentWidget(self.test_round_progress_bar)

        # add test summary count to status bar
        self.btnPassedCount = QToolButton()
        self.btnPassedCount.setText('0')
        self.btnPassedCount.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnPassedCount.setIcon(QIcon(Image_select.get_image('passed.svg')))
        self.btnPassedCount.setStyleSheet('QToolButton { border: none; }')
        self.btnPassedCount.setToolTip('PASSED')

        self.btnFailedCount = QToolButton()
        self.btnFailedCount.setText('0')
        self.btnFailedCount.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnFailedCount.setIcon(QIcon(Image_select.get_image('error.svg')))
        self.btnFailedCount.setStyleSheet('QToolButton { border: none; }')
        self.btnFailedCount.setToolTip('FAILED')

        self.btnPendingCount = QToolButton()
        self.btnPendingCount.setText('0')
        self.btnPendingCount.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnPendingCount.setIcon(QIcon(Image_select.get_image('pending.svg')))
        self.btnPendingCount.setStyleSheet('QToolButton { border: none; }')
        self.btnPendingCount.setToolTip('PENDING')

        self.btnSkippedCount = QToolButton()
        self.btnSkippedCount.setText('0')
        self.btnSkippedCount.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btnSkippedCount.setIcon(QIcon(Image_select.get_image('skip.svg')))
        self.btnSkippedCount.setStyleSheet('QToolButton { border: none; }')
        self.btnSkippedCount.setToolTip('SKIPPED')

        summary_widget = QWidget()
        summary_layout = QHBoxLayout(summary_widget)
        summary_layout.setContentsMargins(0, 0, 0, 0)
        summary_layout.addWidget(self.btnPassedCount)
        summary_layout.addWidget(self.btnFailedCount)
        summary_layout.addWidget(self.btnPendingCount)
        summary_layout.addWidget(self.btnSkippedCount)
        self.statusbar.addPermanentWidget(summary_widget)

    def on_option1_clicked(self):
        print("执行选项1操作")

    def on_option2_clicked(self):
        print("执行选项2操作")

    def on_settings_clicked(self):
        print("打开设置")

    def start_action_clicked(self):
        self.run_action.setEnabled(False)
        self.stop_action.setEnabled(True)
        self.terminated_action.setEnabled(True)
        self.terminal_action.setEnabled(True)

    def stop_action_clicked(self):
        self.run_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.terminated_action.setEnabled(False)
        self.terminal_action.setEnabled(False)

    def open_code_web(self):
        # 指定要打开的网页 URL
        url = QUrl("http://www.example.com")
        # 使用 QDesktopServices 打开网页
        QDesktopServices.openUrl(url)

    def on_toolbar_action(self, action):
        if action is self.run_action:
            self.run_action.triggered.connect(self.start_action_clicked)
        elif action is self.stop_action:
            self.stop_action.triggered.connect(self.stop_action_clicked)
        elif action is self.terminated_action:
            self.terminated_action.triggered.connect(self.stop_action_clicked)
        elif action is self.code:
            self.code.triggered.connect(self.open_code_web)


class LogOutputWidget(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFont(QFont(['Consolas'] + self.font().families()))
        self.setOpenLinks(False)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.document().setDefaultStyleSheet('a {text-decoration: none;} p {padding: 1px 0;}')

    def sizeHint(self):
        size = super().sizeHint()
        height = self.screen().availableGeometry().height()
        return QSize(size.width(), int(height / 3))

    def setMaximumBlockCount(self, maximum):
        self.document().setMaximumBlockCount(maximum)


class TestCaseTreeDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('测试用例')
        self.setAcceptDrops(True)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                         QDockWidget.DockWidgetFeature.DockWidgetMovable)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
