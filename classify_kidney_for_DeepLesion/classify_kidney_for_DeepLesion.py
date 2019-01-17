# encoding:utf8

import sys
import os
import json

import numpy as np
from glob import glob
from PIL import Image, ImageQt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def load_dict(filename):
    '''load dict from json file'''
    with open(filename,"r") as json_file:
        dic = json.load(json_file)
    return dic


def save_dict(filename, dic):
    '''save dict into json file'''
    with open(filename,'w') as json_file:
        json.dump(dic, json_file, ensure_ascii=False)


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 800)
        self.setWindowTitle('label')

        self.cur_class = 0              # 当前类别
        self.qList = []                 # 当前view list
        self.cur_image_idx = 0          # 当前图片文件id

        self.dir_path = None            # 当前处理图片的目录

        self.list_view = None           # 当前的listview组件（显示当前目录下文件）

        self.initUI()                   # 初始化UI界面

        # json文件名称
        # 存储标注文件列表的清单
        self.dir_paths_filename = 'dir_paths.json'
        # 当前标注文件
        self.annotation_filename = None

        # 标注文件dict
        if os.path.exists(self.dir_paths_filename):
            self.dir_paths_dict = load_dict(self.dir_paths_filename)
        else:
            self.dir_paths_dict = {}

        # # 假设选择了目录
        # self.update_dir_path(dir_path='../000001_01_01')

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.image_view = ImageWithMouseControl(self)
        self.grid.addWidget(self.image_view, 1, 1, 8, 8)

        # 初始化listview
        self.init_list_view()
        # 初始化选择类别按钮
        self.init_radio_button()
        # 初始化上下页按钮
        self.init_control_control()

    def init_list_view(self):
        # 实例化列表视图
        if self.list_view is None:
            self.list_view = QListView()

        # 实例化列表模型，添加数据
        self.slm = QStringListModel()

        # 设置模型列表视图，加载数据列表
        self.slm.setStringList(self.qList)

        # 设置列表视图的模型
        self.list_view.setModel(self.slm)

        # 单击触发自定义的槽函数
        self.list_view.clicked.connect(self.clicked)

        # 设置窗口布局，加载控件
        self.grid.addWidget(self.list_view, 9, 9, 2, 4)

    def init_radio_button(self):
        '''
        初始化单选按钮列表
        '''

        self.button_group = QButtonGroup(self)
        self.button_0 = QPushButton('未分类', self)
        self.button_1 = QPushButton('kidney', self)
        self.button_2 = QPushButton('其他类别', self)

        self.button_0.setCheckable(True)
        self.button_1.setCheckable(True)
        self.button_2.setCheckable(True)

        self.button_group.addButton(self.button_0, 0)
        self.button_group.addButton(self.button_1, 1)
        self.button_group.addButton(self.button_2, 2)

        self.button_0.setChecked(True)

        self.grid.addWidget(self.button_0, 2, 9, 1, 2)
        self.grid.addWidget(self.button_1, 3, 9, 1, 2)
        self.grid.addWidget(self.button_2, 4, 9, 1, 2)

        self.button_0.clicked.connect(self.btnclicked)
        self.button_1.clicked.connect(self.btnclicked)
        self.button_2.clicked.connect(self.btnclicked)

    def init_control_control(self):
        '''
        初始化控制键
        '''
        self.open_dir = QPushButton('打开目录', self)
        self.pre_image = QPushButton('上一张', self)
        self.next_image = QPushButton('下一张', self)

        self.grid.addWidget(self.open_dir, 6, 9, 1, 2)
        self.grid.addWidget(self.pre_image, 7, 9, 1, 2)
        self.grid.addWidget(self.next_image, 8, 9, 1, 2)

        self.open_dir.clicked.connect(self.btnclicked)
        self.pre_image.clicked.connect(self.btnclicked)
        self.next_image.clicked.connect(self.btnclicked)

    def btnclicked(self):
        '''
        处理按钮事件
        '''
        sender = self.sender()
        if sender == self.button_0:
            # class 0
            self.cur_class = 0
            self.annotation_dict[self.qList[self.cur_image_idx]] = 0
            save_dict(self.annotation_filename, self.annotation_dict)
        elif sender == self.button_1:
            # class 1
            self.cur_class = 1
            self.annotation_dict[self.qList[self.cur_image_idx]] = 1
            save_dict(self.annotation_filename, self.annotation_dict)
            self.do_next_image()
        elif sender == self.button_2:
            # class 2
            self.cur_class = 2
            self.annotation_dict[self.qList[self.cur_image_idx]] = 2
            save_dict(self.annotation_filename, self.annotation_dict)
            self.do_next_image()
        elif sender == self.pre_image:
            # pre image
            self.do_pre_image()
        elif sender == self.next_image:
            # next image
            self.do_next_image()
        elif sender == self.open_dir:
            # open dir
            dir_path = QFileDialog.getExistingDirectory(self, 'Open Dirs')
            self.update_dir_path(dir_path)

    def update_dir_path(self, dir_path):
        '''
        更新当前处理文件目录
        '''
        if dir_path in self.dir_paths_dict.keys():
            # 如果当前目录处理过，读取相应的标注文件
            self.annotation_filename = self.dir_paths_dict[dir_path]
            self.annotation_dict = load_dict(self.annotation_filename)
            self.qList = list(self.annotation_dict.keys())
        else:
            # 当前目录没有处理过，创建新的标注文件
            self.annotation_filename = 'anno_%d.json'%(len(glob('./anno_*.json')))
            self.dir_paths_dict[dir_path] = self.annotation_filename
            self.annotation_dict = {}
            self.qList = os.listdir(dir_path)
            # 默认为目录下全部文件为要标注的CT图片文件
            for i in range(len(self.qList)):
                self.qList[i] = os.path.join(dir_path, self.qList[i]).replace('\\', '/')
                self.annotation_dict[self.qList[i]] = 0
        # 保存存储标注信息的词典
        save_dict(self.dir_paths_filename, self.dir_paths_dict)
        save_dict(self.annotation_filename, self.annotation_dict)

        self.dir_path = dir_path
        self.init_list_view()
        self.cur_image_idx = 0
        self.load_image()
        self.update()

    def load_image(self):
        '''
        加载当前CT图像
        '''
        image_path = os.path.join(self.dir_path, self.qList[self.cur_image_idx])
        if os.path.exists(image_path):
            # 获取当前类别
            self.cur_class = self.annotation_dict[self.qList[self.cur_image_idx]]
            # 高亮当前处理的文件
            self.list_view.setCurrentIndex(self.slm.index(self.cur_image_idx))
            # 加载图像
            self.image_view.set_image(image_path)
            # 高亮当前类别的按钮
            eval('self.button_%d.setChecked(True)'%(self.cur_class))

    def do_next_image(self):
        '''
        加载下一张图像
        '''
        if self.cur_image_idx+1 < len(self.qList):
            self.cur_image_idx+=1
            self.load_image()
            self.update()
        else:
            QMessageBox.information(self, 'Info', '已经是最后一张')

    def do_pre_image(self):
        '''
        加载上一张图像
        '''
        if self.cur_image_idx > 0:
            self.cur_image_idx-=1
            self.load_image()
            self.update()
        else:
            QMessageBox.information(self, 'Info', '已经是第一张')

    def clicked(self, qModelIndex):
        self.cur_image_idx = qModelIndex.row()
        self.load_image()
        self.update()


class ImageWithMouseControl(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.set_image(bg=True)
        self.scaled_img = self.img.scaled(self.size())
        self.point = QPoint(0, 0)

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
    ex.show()
    app.exec_()