# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFrame

import sys
from video import Video
from QSS import QSS
from titlePage import TitlePage
import re
import os
import time

# 获取当前操作系统
sys_ = sys.platform


class MyBili(QMainWindow):
    # 记录每个视频的位置
    __POS = []
    # 记录每个视频对象
    __OBJECT = []
    # 计数器(记录视频对象的下标)
    __INDEX = 0

    def __init__(self):
        super(MyBili, self).__init__()

        self.__qss = QSS()
        self.__titlepage = TitlePage(sys_)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 无边框
        # 下载位置
        self._downPos = os.path.dirname(sys.argv[0])+"/"
        print(self._downPos)
        try:
            with open("path.txt", "r") as f:
                self._downPos = f.read()
        except Exception:
            with open("path.txt", "w") as f:
                f.write(os.path.dirname(sys.argv[0])+"/")
        # print("原始路径:",self._downPos)

        # 设置可以接受拖拽
        self.setAcceptDrops(True)
        self.setupUi()



    # 无边移动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            # # print("m: ",self.m_Position)
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # ----
    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        # print(e)

        if e.mimeData().hasText():

            # 设置背景图片
            self.setStyleSheet(self.__qss.homeBackDropIng())
            e.accept()
        else:
            e.ignore()

        # 拖拽离开事件

    def dragLeaveEvent(self, e: QtGui.QDragLeaveEvent) -> None:
        # 设置背景图片
        self.setStyleSheet(self.__qss.homeBackDropDefault())

    # 拖拽放下事件
    def dropEvent(self, e: QtGui.QDropEvent) -> None:
        # 获取网站
        html = e.mimeData().text()
        # print("ee",html)
        # [0-9][0-9]|[0-9]  带修改正则
        rel = re.findall("BV(.*)\?p=([0-9][0-9]|[0-9])",html)
        # 匹配普通的视频
        if not rel:
            rel = re.findall("BV(.*)\?", html)
        if not rel:
            rel = re.findall("bv(.*)\?",html)
        # 匹配番剧
        if not rel:
            rel = re.findall("BV(.*)/?", html)
            rel[0]=rel[0].replace(r"/","")
        # rel =["1qJ411N7Fc"]
        # print("_rel: ",rel)
        # self.close()
        # 设置背景图片
        self.setStyleSheet(self.__qss.homeBackDropDefault())

        w = 0
        if self.scrollAreaWidgetContents.width() - 10 > 700:
            w = 690
        else:
            w = self.scrollAreaWidgetContents.width() - 10



        # 设置封面下载路径
        self.__titlepage.setPath(self._downPos)
        # 添加视频
        if not MyBili.__OBJECT:
            # print("url:",rel)
            MyBili.__OBJECT.append(Video(rel[0],self.scrollAreaWidgetContents))
            # 区别普通视频和系统视频
            if len(rel[0]) == 1:
                bv = rel[0]
            elif len(rel[0]) == 2:
                bv = rel[0][0]
            else:
                bv = rel[0]
            # print("bv:",bv)

            # 图片名称
            imageName = MyBili.__OBJECT[MyBili.__INDEX].downOBJ().getVideoTile()
            # print("imageName:", imageName)
            if not imageName:
                imageName = time.strftime("%Y_%m_%d_%H:%M", time.localtime())  # 当前日期和时间

            self.__titlepage.down(bv,imgaeName=imageName)


            MyBili.__OBJECT[0].backgroundColor(self.__titlepage.getPath())        # 设置背景颜色
            MyBili.__OBJECT[0].videoWidgetName(html)     # 设置标题名称
            MyBili.__OBJECT[0].downOBJ().setDownloadPath(self._downPos)   # 设置下载路径
            # 视频关闭按钮事件
            MyBili.__OBJECT[0].sequence[str].connect(lambda :self.videoDel(10))
            MyBili.__OBJECT[0].setGeometry(QtCore.QRect(10, 200, w, 150))
            MyBili.__POS.append(10)
            MyBili.__OBJECT[0].show()
            # 加一
        else:
            MyBili.__OBJECT.append(Video(rel[0],self.scrollAreaWidgetContents))  # type: Video

            # 区别普通视频和系统视频
            if len(rel[0]) == 1:
                bv = rel[0]
            elif len(rel[0]) == 2:
                bv = rel[0][0]
            else:
                bv = rel[0]
            # 图片名称
            imageName = MyBili.__OBJECT[MyBili.__INDEX].downOBJ().getVideoTile()
            # print("imageName:", imageName)
            if not imageName:
                imageName = time.strftime("%Y_%m_%d_%H:%M", time.localtime())  # 当前日期和时间

            self.__titlepage.down(bv, imgaeName=imageName)


            MyBili.__OBJECT[-1].backgroundColor(self.__titlepage.getPath())        # 设置背景颜色
            MyBili.__OBJECT[-1].videoWidgetName(html)
            MyBili.__OBJECT[-1].downOBJ().setDownloadPath(self._downPos)  # 设置下载路径
            posw = MyBili.__POS[-1] + 128 + 10
            # 视频关闭按钮事件
            MyBili.__OBJECT[-1].sequence[str].connect(lambda :self.videoDel(posw))
            MyBili.__OBJECT[-1].setGeometry(QtCore.QRect(10, posw, w, 150))
            MyBili.__POS.append(posw)
            MyBili.__OBJECT[-1].show()

        # print(MyBili.__OBJECT)

        # 排序
        self._videoSequence()

        # 所有视频总长+50 大于的当前窗口大小，则自动扩大
        videoSum = sum([len_.height() for len_ in MyBili.__OBJECT])
        if videoSum + 50 > self.height():
            # 自动扩容
            self.scrollAreaWidgetContents.setMinimumSize(250, videoSum+256)


    # 视频排序
    def _videoSequence(self):
        # 根据视频的个数来重新排列顺序
        videoLen = len(MyBili.__POS)
        temp = 25  # 视频间间距
        for i in range(videoLen):
            # x = MyBili.__OBJECT[i].pos().x()
            # y = MyBili.__OBJECT[i].pos().y()
            # # print("移动前: ",MyBili.__OBJECT[i].pos().x())
            if i == 0:
                MyBili.__OBJECT[i].move(10, temp)
            else:
                temp += 138
                MyBili.__OBJECT[i].move(10, temp)
            # # print("移动后: ", MyBili.__OBJECT[i].pos())

    # 视频删除，并释放
    def videoDel(self,indexNum):
        '''
        视频删除，并释放
        :param indexNum: 视频所在位置
        :return:
        '''
        # # print("排序：",indexNum)
        # 获取索引
        # # print("原始数组：",MyBili.__POS)
        index = MyBili.__POS.index(indexNum)
        # # print("索引值: ",index)
        # 删除索引
        MyBili.__POS.pop(index)
        # # print("删除了:{},{}".format(indexNum,MyBili.__POS))
        # 释放对象
        MyBili.__OBJECT[index].close()
        # 删除对象
        MyBili.__OBJECT.pop(index)

        # 视频排序
        self._videoSequence()


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, self.width(), self.height()))
        if MyBili.__OBJECT:
            for obj_index in MyBili.__OBJECT:
                obj_index.myrsize(self.scrollAreaWidgetContents.width() - 20)
        # # print(self.scrollAreaWidgetContents.width())

    # 设置标签颜色
    def _setPathStyle(self,color:str,text:str):
        '''

        :param color: 文本颜色
        :param text: 文本内容
        :return:
        '''

        # 给显示路径做替换
        html = '''
                                    <html>
                                     <body>
                                        <span style="font-size: 12px;color: darkgrey;">当前路径:<span> <span style="color: C;">@</span>
                                     </body>
                                    </html>
           '''

        html = html.replace("C",color).replace("@",text)
        return html


    def setupUi(self):
        self.resize(711, 582)
        self.setMinimumSize(QtCore.QSize(450, 410))
        self.setMaximumSize(QtCore.QSize(166666, 166666))
        self.setWindowOpacity(0.99)
        # 设置背景图片
        self.setStyleSheet(self.__qss.homeBackDropDefault())
        # self.setWindowIcon(QIcon(""))

        # <---
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QVBoxLayout()
        self.gridLayout.setContentsMargins(0,0,0,0)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setMinimumSize(250, 582)

        self.scroll =  QtWidgets.QScrollArea()
        self.scroll.setStyleSheet(self.__qss.homeScrollAreaStyle())
        self.scroll.setWidget(self.scrollAreaWidgetContents)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横行滚动条

        self.gridLayout.addWidget(self.scroll)
        self.centralwidget.setLayout(self.gridLayout)
        # 背景设置透明
        self.centralwidget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # --->

        # 关闭窗口按钮
        self.btncolse = QtWidgets.QPushButton(self.centralwidget)
        self.btncolse.resize(15,15)
        self.btncolse.move(5,5)
        self.btncolse.setStyleSheet(self.__qss.homeCloseButton())
        self.btncolse.clicked.connect(self.close_mainWidget)

        # 最小化按钮
        self.btnmin = QtWidgets.QPushButton(self.centralwidget)
        self.btnmin.resize(15, 15)
        self.btnmin.move(25, 5)
        self.btnmin.setStyleSheet(self.__qss.homeMinButton())
        self.btnmin.clicked.connect(lambda :self.setWindowState(Qt.WindowMinimized))

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setText(" <span style='font-size: 15px;color:slategrey;'>B站视频下载器</span>")
        self.title.move(self.width()//2-50,-1)

        # 底部栏的控件
        # --------------------------
        self.btn = QtWidgets.QPushButton()
        self.btn.resize(20,40)
        self.btn.setStyleSheet(self.__qss.homedownPos())

        self.bel = QtWidgets.QLabel()

        self.bel.setText(self._setPathStyle("darkgrey", self._downPos))
        # self.bel.setText("<span style='font-size: 12px;color: darkgrey;'>当前路径:./</span>")

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.setStyleSheet("background-color:#b0f0f2")
        self.setStatusBar(self.statusBar)
        self.statusBar.addWidget(self.btn)
        self.statusBar.addWidget(self.bel)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        # 底部栏控件事件
        self.btn.clicked.connect(self._showPath)

    # 封装信息框
    def _information(self, title: str = "标题", text: str = "消息"):
        '''
                       EG:
                        if qm == QMessageBox.Yes:
                            pass
                        else:
                            pass
        '''
        qm = QMessageBox.information(QFrame(),  # 使用infomation信息框
                                     title,
                                     text,
                                     QMessageBox.Yes | QMessageBox.No)
        return qm
    # 关闭主窗口
    def close_mainWidget(self):
        qm = self._information(title="关闭", text="请检查是否下载完毕")
        if qm == QMessageBox.Yes:
            self.close()

    # 设置视频存放路径
    def _showPath(self):
        try:
            with open("path.txt","r") as f:
                path = f.read()
            _oldPtah = ""
            if path:
                _oldPtah = path  # 保存以存在的路径
                self._downPos = QFileDialog.getExistingDirectory(self, "存放位置", path)
                # 如果用户打开文件后,取消,则self._downPos为空值,需要用存在的路径重新覆盖
                if not self._downPos:
                    self._downPos = _oldPtah
            else:

                self._downPos = QFileDialog.getExistingDirectory(self, "存放位置", os.getcwd())
                # 如果用户打开文件后,取消,则self._downPos为空值,需要赋值
                if not self._downPos:
                    self._downPos = os.path.dirname(sys.argv[0])+"/"
        except Exception:
            self._downPos = QFileDialog.getExistingDirectory(self, "存放位置", os.getcwd())
        # 更改路径
        with open("path.txt", "w") as f:
            f.write(self._downPos)

        if MyBili.__OBJECT:
            self.bel.setText(self._setPathStyle("darkgrey",self._downPos))
        else:
            self.bel.setText(self._setPathStyle("darkgrey",self._downPos))

        # 设置路径
        if MyBili.__OBJECT:
            for obj in MyBili.__OBJECT:
                obj.downOBJ().setDownloadPath(self._downPos)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.setToolTip("<h5 style=;'color: darkgrey;'>请将网址拖入此处</h5>")
        self.setWindowOpacity(0.95)
        # self.setWindowIcon(QIcon("homeIco.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = MyBili()
    ui.show()

    sys.exit(app.exec_())
