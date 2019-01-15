# encoding:utf8

import sys
import os

import numpy as np
from PIL import Image, ImageQt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = ImageWithMouseControl(self)
        self.widget.setGeometry(10, 10, 600, 600)
        self.setWindowTitle('CT browser')

        # 设置拖拽事件
        self.setAcceptDrops(True)
        self.setWindowFlags(
                            Qt.WindowStaysOnTopHint)  # 窗体总在最前端

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

            # if os.path.isdir(filename):
            #     # dir
            #     event_for_dir(filename)
            if os.path.isfile(filename):
                # file
                self.widget.set_image(filename)
                self.widget.repaint()

    def resizeEvent(self, e):
        if self.parent is not None:
            self.widget.setGeometry(self.width()*0.05, self.height()*0.05, self.width()*0.9, self.height()*0.9)
            self.update()


class ImageWithMouseControl(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.set_image(bg=True)
        self.scaled_img = self.img.scaled(self.size())
        self.point = QPoint(0, 0)

        self.initUI()

    def initUI(self):

        self.setWindowTitle('CT browser')

    def set_image(self, path=None, bg=False):
        if bg:
            self.img = QPixmap('bg.jpg')
            self.repaint()
            return
        if path is None:
            return
        img = Image.open(path)
        img = np.array(img)
        img -= 32768
        img = Image.fromarray(img)
        img = img.convert("RGB")
        data = img.tobytes("raw", "RGB")
        img = QImage(data, img.size[0], img.size[1], QImage.Format_RGB888)
        self.img = QPixmap.fromImage(img)
        self.scaled_img = self.img.scaled(self.size())
        self.repaint()

    def paintEvent(self, e):
        '''
        绘图
        :param e:
        :return:
        '''
        painter = QPainter()
        painter.begin(self)
        self.draw_img(painter)
        painter.end()

    def draw_img(self, painter):
        painter.drawPixmap(self.point, self.scaled_img)

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self._startPos = e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = False
        elif e.button() == Qt.RightButton:
            self.point = QPoint(0, 0)
            self.scaled_img = self.img.scaled(self.size())
            self.repaint()

    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            # 放大图片
            self.scaled_img = self.img.scaled(self.scaled_img.width()-5, self.scaled_img.height()-5)
            new_w = e.x() - (self.scaled_img.width() * (e.x() - self.point.x())) / (self.scaled_img.width() + 5)
            new_h = e.y() - (self.scaled_img.height() * (e.y() - self.point.y())) / (self.scaled_img.height() + 5)
            self.point = QPoint(new_w, new_h)
            self.repaint()
        elif e.angleDelta().y() < 0:
            # 缩小图片
            self.scaled_img = self.img.scaled(self.scaled_img.width()+5, self.scaled_img.height()+5)
            new_w = e.x() - (self.scaled_img.width() * (e.x() - self.point.x())) / (self.scaled_img.width() - 5)
            new_h = e.y() - (self.scaled_img.height() * (e.y() - self.point.y())) / (self.scaled_img.height() - 5)
            self.point = QPoint(new_w, new_h)
            self.repaint()

    def resizeEvent(self, e):
        if self.parent is not None:
            self.scaled_img = self.img.scaled(self.size())
            self.point = QPoint(0, 0)
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    # ex = ImageWithMouseControl()
    ex.show()
    app.exec_()
