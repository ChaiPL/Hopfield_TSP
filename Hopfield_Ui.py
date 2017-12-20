from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
import sys
import numpy as np
from Hopfield_Distance import distance_matrix, normalize, distanceLines, arrayTwoToOne
from Hopfield_Algorithm import HopfieldNet
from Hopfield_CreateCity import CreateCity


shape = ["Init", "LoadMap", "Points", "Lines"]

class TSPThread(QThread):
    signal_msg = QtCore.pyqtSignal(str)
    signal_draw = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(TSPThread, self).__init__(parent)
        self.running = False   #线程开关标志位
        self.iter = 0

    def startTSP(self):
        self.start()
        self.running = True  # 开启线程

    def stopTSP(self):
        # self.start()
        self.running = False  # 停止线程

    def run(self):
        bestDistance = 100000.00
        bestDistance_x = []
        bestDistance_y = []
        for i in range(city_num):
            bestDistance_x.append(distance_x[i])
            bestDistance_y.append(distance_y[i])

        self.signal_msg.emit("路径搜索中...")
        distances = distance_matrix(city_matrix)
        normalized_distances = normalize(distances)
        net = HopfieldNet(normalized_distances)

        while self.running:
            self.iter += 1
            net.update()
            TransformArray = net.EnergyToAddress()
            valid = net.HopfieldValidTest(TransformArray)
            if valid == True:
                x = np.mat(distance_x)
                y = np.mat(distance_y)
                t = np.mat(TransformArray)
                newdistance_x = (x * t).tolist()[0]
                newdistance_y = (y * t).tolist()[0]
                for i in range(city_num):
                    distance_x[i] = newdistance_x[i]
                    distance_y[i] = newdistance_y[i]
            else:
                self.sleep(0.001)

            DistanceCity = distanceLines(city_num, distance_x, distance_y)
            if DistanceCity < bestDistance:
                bestDistance = DistanceCity
                for i in range(city_num):
                    bestDistance_x[i] = distance_x[i]
                    bestDistance_y[i] = distance_y[i]
            for i in range(city_num):
                distance_x[i] = bestDistance_x[i]
                distance_y[i] = bestDistance_y[i]
            self.signal_draw.emit("Lines")
            if self.iter % 100 == 0:
                DistanceCity = distanceLines(city_num, distance_x, distance_y)
                self.signal_msg.emit("第 %d 次路径搜索" % self.iter)
                self.signal_msg.emit("当前路径长度为：%.2f" % DistanceCity)
                self.signal_msg.emit("最短路径长度为 ：%.2f" % bestDistance)
            self.sleep(0.01)

class StockDialog(QWidget):
    def __init__(self):
        super(StockDialog, self).__init__()
        self.init_ui()
        self.TSP = TSPThread()
        self.TSP.signal_msg.connect(self.slotShowMsg)
        self.TSP.signal_draw.connect(self.slotSetShape)

    def init_ui(self):
        self.setWindowTitle("Hopfield神经网络解决TSP问题程序")
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.setOpaqueResize(True)

        frame = QFrame(mainSplitter)
        mainLayout = QGridLayout(frame)
        mainLayout.setSpacing(6)

        self.LoadMapPushButton = QPushButton("加载地图")
        self.InitPushButton = QPushButton("初始化")
        self.StartPushButton = QPushButton("开始搜索")
        self.EndPushButton = QPushButton("结束搜索")
        self.ExitPushButton = QPushButton("退出程序")
        self.OutputLabel = QLabel("运行信息")
        self.OutputTextEdit = QTextEdit()

        # 建立布局
        PushButtonCol = 0.4
        mainLayout.addWidget(self.LoadMapPushButton, 0, PushButtonCol)
        mainLayout.addWidget(self.InitPushButton, 1, PushButtonCol)
        mainLayout.addWidget(self.StartPushButton, 2, PushButtonCol)
        mainLayout.addWidget(self.EndPushButton, 3, PushButtonCol)
        mainLayout.addWidget(self.ExitPushButton, 4, PushButtonCol)
        mainLayout.addWidget(self.OutputLabel, 5, PushButtonCol)
        mainLayout.addWidget(self.OutputTextEdit, 6, PushButtonCol)

        mainSplitter1 = QSplitter(Qt.Horizontal)
        mainSplitter1.setOpaqueResize(True)

        stack1 = QStackedWidget()
        stack1.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.area = PaintArea()
        stack1.addWidget(self.area)
        frame1 = QFrame(mainSplitter1)
        mainLayout1 = QVBoxLayout(frame1)
        mainLayout1.setSpacing(6)
        mainLayout1.addWidget(stack1)

        layout = QGridLayout(self)
        layout.addWidget(mainSplitter, 0, 0.5)       # 两个ui的位置，第二个参数为行，打三个参数为列
        layout.addWidget(mainSplitter1, 0, 1)
        self.setLayout(layout)

        # 信号和槽函数
        self.LoadMapPushButton.clicked.connect(self.slotLoadMap)
        self.InitPushButton.clicked.connect(self.slotInitialization)
        self.StartPushButton.clicked.connect(self.slotStartSearch)
        self.EndPushButton.clicked.connect(self.slotStopSearch)
        self.ExitPushButton.clicked.connect(self.slotClose)

        self.area.setShape("Init")    #初始化, 画与背景颜色相同的点

    def slotSetShape(self, shape):
        self.area.setShape("%s" % shape)

    def slotLoadMap(self):
        self.area.setShape("LoadMap")

    def slotInitialization(self):
        self.area.setShape("Lines")

        DistanceCity = distanceLines(city_num, distance_x, distance_y)
        self.slotShowMsg("初始总距离：%.2f" % DistanceCity)

    def slotStartSearch(self, evt=None):
        self.slotShowMsg("开始搜索路径...")
        self.TSP.startTSP()

    def slotStopSearch(self):
        self.slotShowMsg("结束路径搜索")
        self.TSP.stopTSP()

    def slotClose(self):
        self.destroy()
        print("程序已退出...")
        sys.exit()

    def slotShowMsg(self, text):
        self.OutputTextEdit.append(str(text))


class PaintArea(QWidget):
    def __init__(self):
        super(PaintArea, self).__init__()
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(350, 350)

    def setShape(self, s):
        self.shape = s
        self.update()

    def Init(self):
        p = QtGui.QPainter()
        p.begin(self)

        for i in range(city_num):
            x1 = distance_x[i]
            y1 = distance_x[i]
            p.setPen(QtCore.Qt.white)
            r = 3
            p.drawEllipse(x1-r, y1-r, 2*r, 2*r)  #城市坐标处画圆，半径为r

        p.end()

    def drawPoints(self):
        p = QtGui.QPainter()
        p.begin(self)

        for i in range(city_num):
            x1 = distance_x[i]
            y1 = distance_y[i]
            p.setPen(QtCore.Qt.red)
            r = 3
            p.drawEllipse(x1-r, y1-r, 2*r, 2*r)

        p.end()

    def drawLines(self):
        p = QtGui.QPainter()
        p.begin(self)

        for i in range(city_num):
            x1 = distance_x[i]
            y1 = distance_y[i]
            if i != city_num - 1:
                x2 = distance_x[i+1]
                y2 = distance_y[i+1]
            else:
                x2 = distance_x[0]
                y2 = distance_y[0]
            p.setPen(QtCore.Qt.red)
            r = 3
            p.drawEllipse(x1-r, y1-r, 2*r, 2*r)
            p.setPen(QtCore.Qt.blue)
            p.drawLine(x1, y1, x2, y2)

        p.end()

    def paintEvent(self, QPaintEvent):
        if self.shape == "Init":
            self.Init()
        if self.shape == "LoadMap":
            self.drawPoints()
        if self.shape == "Lines":
            self.drawLines()
        elif self.shape == "Points":
            self.drawPoints()


def run(get_cityMatrix):
    print(u""" 
    --------------------------------------------------------
        程序：Hopfield神经网络解决TSP问题程序 
        作者：柴培林 
        邮箱：chaiplhit@163.com
        日期：2017-11-29
        语言：Python 3.6.2 
    -------------------------------------------------------- 
        """)
    global city_matrix, city_num, distance_x, distance_y
    city_matrix = get_cityMatrix
    city_num, distance_x, distance_y = arrayTwoToOne(get_cityMatrix)


    app = QApplication(sys.argv)
    form = StockDialog()
    form.show()
    app.exec_()


if __name__ == '__main__':
    # 城市坐标
    # city_address = [(25, 120), (240, 55), (330, 50), (295, 275), (100, 35), (90, 290), (245, 110), (295, 165)]
    city_address = CreateCity(8)

    run(city_address)



