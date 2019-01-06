# encoding:utf8

import os
import sys

import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QWidget

from do_event import event_for_dir, event_for_file


class DragFilesDoEvent(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setWindowTitle('File Manager')
        self.resize(150, 150)

        desktop = QApplication.desktop()
        x = int(desktop.width()*0.9) - self.window().width()
        y = int(desktop.height()*0.1)
        self.move(x, y)

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
                            QtCore.Qt.WindowCloseButtonHint |      # 使能关闭按钮
                            QtCore.Qt.WindowStaysOnTopHint)        # 窗体总在最前端
        self.setFixedSize(self.width(), self.height())             # 固定窗体大小

        self.setAcceptDrops(True)
    
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



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = DragFilesDoEvent()
    ex.show()
    app.exec_()
