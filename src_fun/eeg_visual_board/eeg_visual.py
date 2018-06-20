import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib import animation
from matplotlib.animation import FuncAnimation

def Visualeeg_sensor2D(name,loc):
    X = loc[:,0]
    Y = loc[:,1]
    plt.figure("sensor_2D")
    for i in range(len(name)):
        plt.scatter(X[i],Y[i],marker='o')
        plt.text(X[i],Y[i],name[i])
    plt.legend()
    plt.show()

def Visualeeg_sensor3D(name,loc):
    X = loc[:,0]
    Y = loc[:,1]
    Z = loc[:,2]
    plt.figure("sensor_3D")
    ax = plt.subplot(111,projection='3d')

    for i in range(len(name)):
        ax.scatter(X[i],Y[i],Z[i],c='r')
        ax.text(X[i],Y[i],Z[i],name[i])
    plt.legend()
    plt.show()


def Visualeeg32_subplot(eegdata,name):
    plt.figure(name+'_32subplot')
    channels,points = eegdata.shape
    width = 8
    i = 1

    for eegdata_single_channel in eegdata[0:32,0::]:
        print(i)
        print(width)
        plt_ = plt.subplot(width,4,i)
        plt_.plot(range(points),eegdata_single_channel,label=str(i))

        i=i+1
        plt_.legend()
    plt.show()

def Visualeeg32_one(eegdata,name):
    plt.figure(name+'_32one')
    channels,points = eegdata.shape
    i = 1
    print("one:",eegdata.shape)
    for eegdata_single_channel in eegdata[0:32,0::]:
        color = (i*7,i*7,i*7)
        plt.plot(range(points),eegdata_single_channel,label=str(i))

        i=i+1
    plt.legend()
    plt.show()

def Visual_BrainHot(figurename, eegdata,sensorName,sensorLoc):
    plt.figure('BrainHot-average'+figurename)
    value=[]
    for eegdata_single_channel in eegdata[0:32, 0::]:
        average = sum(eegdata_single_channel)/len(eegdata_single_channel)
        var = np.var(eegdata_single_channel)
        power = sum(eegdata_single_channel*eegdata_single_channel)

        value.append(average)


    Value = np.array(value)


    x_y = sensorLoc[:,0:2]
    grid_x, grid_y = np.mgrid[-1:1:1000j, -1:1:1000j]
    grid_z = griddata(x_y, Value, (grid_x,grid_y), method='cubic' )

    # print(Value)
    # print(np.max(grid_z),np.min(grid_z))
    cm = plt.cm.get_cmap('RdYlBu_r')
    sc = plt.contourf(grid_x, grid_y, grid_z, 100, alpha = 1, cmap = cm)
    # C = plt.contour(grid_x, grid_y, grid_z, 10, alpha=0.5, colors = 'black')
    # plt.clabel(C, inline = True, fontsize = 10)
    X = sensorLoc[:,0]
    Y = sensorLoc[:,1]
    for i in range(len(sensorName)):
        plt.scatter(X[i],Y[i],marker='o')
        plt.text(X[i],Y[i],sensorName[i])
    # plt.legend()
    plt.colorbar(sc)
    plt.show()
    print("brainhot")

def Visual_BrainHot_all(figurename, eegdata,sensorName,sensorLoc):
    fig = plt.figure(figurename+'-brainhot')
    value_average = []
    value_var = []
    value_power = []
    for eegdata_single_channel in eegdata[0:32, 0::]:
        average = sum(eegdata_single_channel)/len(eegdata_single_channel)
        var = np.var(eegdata_single_channel)
        power = sum(eegdata_single_channel*eegdata_single_channel)

        value_average.append(average)
        value_var.append(var)
        value_power.append(power)

    Value_average = np.array(value_average)
    Value_var = np.array(value_var)
    Value_power = np.array(value_power)

    x_y = sensorLoc[:,0:2]
    grid_x, grid_y = np.mgrid[-1:1:1000j, -1:1:1000j]

    ax = plt.subplot(221)
    grid_z = griddata(x_y, Value_average, (grid_x,grid_y), method='cubic' )
    cm = plt.cm.get_cmap('RdYlBu_r')
    sc = plt.contourf(grid_x, grid_y, grid_z, 100, alpha = 1, cmap = cm)

    X = sensorLoc[:,0]
    Y = sensorLoc[:,1]
    for i in range(len(sensorName)):
        plt.scatter(X[i],Y[i],marker='o')
        plt.text(X[i],Y[i],sensorName[i])
    # plt.legend()
    plt.colorbar(sc)
    plt.title(figurename+'-average')

    plt.subplot(222)
    grid_z = griddata(x_y, Value_var, (grid_x,grid_y), method='cubic' )
    cm = plt.cm.get_cmap('RdYlBu_r')
    sc = plt.contourf(grid_x, grid_y, grid_z, 100, alpha = 1, cmap = cm)

    X = sensorLoc[:,0]
    Y = sensorLoc[:,1]
    for i in range(len(sensorName)):
        plt.scatter(X[i],Y[i],marker='o')
        plt.text(X[i],Y[i],sensorName[i])
    # plt.legend()
    plt.colorbar(sc)
    plt.title(figurename+'-var')

    plt.subplot(223)
    grid_z = griddata(x_y, Value_power, (grid_x,grid_y), method='cubic' )
    cm = plt.cm.get_cmap('RdYlBu_r')
    sc = plt.contourf(grid_x, grid_y, grid_z, 100, alpha = 1, cmap = cm)

    X = sensorLoc[:,0]
    Y = sensorLoc[:,1]
    for i in range(len(sensorName)):
        plt.scatter(X[i],Y[i],marker='o')
        plt.text(X[i],Y[i],sensorName[i])
    # plt.legend()
    plt.colorbar(sc)
    plt.title(figurename+'-power')

    plt.show()
    print("brainhot")

def Visual_BrainHot_animation(brainhot_plotname,eeg_brainhot, sensorName, sensorLoc):

    x_y = sensorLoc[:,0:2]
    grid_x, grid_y = np.mgrid[-1:1:100j, -1:1:100j]

    eeg_max = np.max(np.max(eeg_brainhot))
    eeg_min = np.min(np.min(eeg_brainhot))

    plt.figure('BrainHot-Animation-VisualBoard')
    plt.ion()

    LENGTH = eeg_brainhot.shape[1]
    FRAME_INTERVAL = 5
    TIME_INTERVAL = 1/(500/FRAME_INTERVAL)

    # 循环
    for index in range(LENGTH//FRAME_INTERVAL):
        # 清除原有图像
        plt.cla()

        strnum = 'No. '+str(index*FRAME_INTERVAL)
        # 设定标题等
        plt.title(brainhot_plotname + '-' + strnum)
        # plt.grid(True)
        grid_z = griddata(x_y, eeg_brainhot[0:32,index*FRAME_INTERVAL], (grid_x,grid_y), method='cubic' )

        x=grid_x.reshape(-1,1)
        y=grid_y.reshape(-1,1)
        z=grid_z.reshape(-1,1)

        z = (z-eeg_min)/(eeg_max-eeg_min)



        # # 生成测试数据
        # point_count = 5
        # x_index = np.random.random(point_count)
        # y_index = np.random.random(point_count)
        #
        # # 设置相关参数
        # color_list = np.random.random(point_count)
        # scale_list = np.random.random(point_count) * 100

        # 画散点图
        cm = plt.cm.get_cmap('RdYlBu_r')
        sc = plt.scatter(x, y, s=1, c=z, cmap = cm, marker="o")

        X = sensorLoc[:,0]
        Y = sensorLoc[:,1]
        for i in range(len(sensorName)):
            plt.scatter(X[i],Y[i],marker='o')
            plt.text(X[i],Y[i],sensorName[i])

        if index == 0:
            plt.colorbar(sc)

        # 暂停
        plt.pause(0.001)

    # 关闭交互模式
    plt.ioff()

    # 显示图形

    plt.show()
    return
# scatter_plot()