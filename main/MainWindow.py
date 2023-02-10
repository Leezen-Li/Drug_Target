import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5 import QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Javascript call PyQt5')
        self.setGeometry(5, 30, 1355, 730)
        self.browser = QWebEngineView()
        # 加载外部的web界面
        # self.browser.load(QUrl(QFileInfo("../html/hahaha.html").absoluteFilePath()))
        # self.browser.load(QUrl(QFileInfo("../dist_back/index.html").absoluteFilePath()))
        self.browser.load(QUrl(QFileInfo("../dist/index.html").absoluteFilePath()))
        self.setCentralWidget(self.browser)

    def calljs(self, js_code):
        # 只能主线程调用
        self.browser.page().runJavaScript("1")



