# encoding:utf8

import os
import sys

import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from do_event import event_for_dir, event_for_file


class DragFilesDoEvent(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setWindowTitle('File Manager')
        self.resize(100, 100)

        desktop = QApplication.desktop()
        x = int(desktop.width()*0.9) - self.window().width()
        y = int(desktop.height()*0.1)
        self.move(x, y)

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
                            QtCore.Qt.WindowCloseButtonHint |      # 使能关闭按钮
                            QtCore.Qt.FramelessWindowHint |        # 去掉边框
                            QtCore.Qt.WindowStaysOnTopHint)        # 窗体总在最前端
        self.setFixedSize(self.width(), self.height())             # 固定窗体大小

        # 设置拖拽事件
        self.setAcceptDrops(True)

        # 设置背景图片
        self.set_background()


    def set_background(self, pic_info='bg'):
        '''
            设置背景图片
        '''
        if pic_info == 'processing':
            # TODO:想加入处理文件时的动画
            self.bg_label = QLabel(self)
            gif = QMovie('./processing.gif')
            gif.setScaledSize(self.size())
            self.bg_label.setAlignment(Qt.AlignCenter)
            self.bg_label.setMovie(gif)
            gif.start()
        else:
            bg_pic = QPixmap('./bg.jpg')
            if not bg_pic.isNull():
                bg_resize_pic = bg_pic.scaled(self.size())
                bg_palette = QPalette()
                bg_palette.setBrush(self.backgroundRole(), QBrush(bg_resize_pic))
                self.setPalette(bg_palette)


    def dragEnterEvent(self, e):
        e.accept()
        
    def dropEvent(self, e):
        filenames = e.mimeData().text()
        filenames = filenames.split('\n')
        for filename in filenames:
            filename = filename.strip()
            if filename == '':
                continue
            if not filename.startswith('file:///'):
                print('bye')
                return
            filename = filename.replace('file:///', '')
            
            if os.path.isdir(filename):
                # dir
                event_for_dir(filename)

            if os.path.isfile(filename):
                # file
                event_for_file(filename)

    def mouseMoveEvent(self, e):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
        elif e.button() == Qt.RightButton:
            exit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = DragFilesDoEvent()
    ex.show()
    app.exec_()
