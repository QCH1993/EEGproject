#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import random
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
DATA = np.array([[random.randint(0, 10)+channel*10 for x in range(1000)] for channel in range(32)])

class MyMplCanvas(FigureCanvas):

#"""FigureCanvas的最终的父类其实是QWidget。"""
    def __init__(self, parent=None, width=5, height=5, dpi=100):

        # 配置中文显示
        # plt.rcParams['font.family'] = ['fantasy']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # define the channel(list:[channel,points]) you need to plot


    '''绘制静态图，可以在这里定义自己的绘图逻辑'''
    def start_static_scatter(self, Xdata=np.array(range(len(DATA[0]))),Ydata=DATA,
                          labels= [],
                          title = 'eeg_sensor',
                           Xlabel='back-front',Ylabel='left-right', gridswitch=True):


        print("start scatter static fig...")
        print(Ydata.shape)
        self.axes.clear()
        self.fig.suptitle(title)

        for i in range(len(Ydata)):
            self.axes.scatter(Xdata[i], Ydata[i], label=labels[i])

        self.axes.set_ylabel(Ylabel)
        self.axes.set_xlabel(Xlabel)
        self.axes.grid(gridswitch)
        # handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend()

        self.draw()

    def start_static_plot(self, Xdata=np.array(range(len(DATA[0]))),Ydata=DATA,
                          marks = [],
                          title = 'example_eeg_signal',
                           Xlabel='Datapoints',Ylabel='Voltage/uV', gridswitch=True):


        print("start plot static fig...")
        print(Ydata.shape)
        self.axes.clear()
        self.fig.suptitle(title)

        for i in range(len(Ydata)):
            self.axes.plot(Xdata, Ydata[i], label=str(i))

        max_data = Ydata.max()
        min_data = Ydata.min()
        scale_max_min = max_data-min_data
        mid_len = scale_max_min*0.6
        mid = (max_data+min_data)/2
        if marks != []:
            for markline in marks:
                mark = markline[1]
                mark_label = str(markline[0])
                self.axes.plot([mark,mark],[mid-mid_len,mid+mid_len],'r')
                self.axes.text(mark, mid+mid_len,mark_label)
                self.axes.text(mark,mid-mid_len, str(mark))

        self.axes.set_ylabel(Ylabel)
        self.axes.set_xlabel(Xlabel)
        self.axes.grid(gridswitch)
        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend()
        # self.axes.legend()
        self.draw()

    # def add_static_line(self, Xdata, label, ):
    #
    #     print("add_static_plot...")
    #     for i in range(len(Xdata)):
    #         self.axes.plot(Xdata,Ydata[i])

    def start_dynamic_plot(self, *args, **kwargs):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)  # 每隔一段时间就会触发一次update_figure函数。
        timer.start(1000)  # 触发的时间间隔为1秒。

    '''动态图的绘图逻辑可以在这里修改'''

    def update_figure(self,data=DATA):

        self.axes.clear()

        self.fig.suptitle('测试动态图')
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.axes.set_ylabel('动态图：Y轴')
        self.axes.set_xlabel('动态图：X轴')
        self.axes.grid(True)
        self.draw()


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=5, dpi=100)
        # self.mpl.start_static_plot()
        # self.mpl.start_static_plot() # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        #self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)

    # # pass the data to the MyMplCanvas
    # def plot_static_fig(self, data=DATA):
    #     # data format check
    #     try:
    #         len(data)
    #         len(data[0])
    #     except TypeError as e:
    #         print(e)
    #
    #     if data!=None:
    #         self.mpl.data = data
    #         print(data)
    #     self.mpl.start_static_plot()
    #     print(data)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    # ui.mpl.start_static_plot()  # 测试静态图效果
    # ui.mpl.start_dynamic_plot() # 测试动态图效果
    ui.show()
    sys.exit(app.exec_())
