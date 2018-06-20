from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog, QMessageBox
from eegmainwindow import Ui_MainWindow
from MatplotlibWidget import MatplotlibWidget
from src_fun.EEGClass import EEGData
from AboutThisData import Ui_AboutThisData
from Data_info import Ui_DataInfo
from Data_edit import Ui_Data_edit
from Sensor_edit import Ui_Sensor_edit
import numpy
import copy

EEGnow = EEGData()

class DataEditWindow(QDialog,Ui_Data_edit):

    def __init__(self, parent=None):

        super(DataEditWindow, self).__init__(parent)
        self.setupUi(self)

        self.STACK = True
        self.FILTER = False
        self.mark_win = EEGnow.marks
        self.eegshow = copy.deepcopy(EEGnow.eeg_raw)
        self.channels = range(self.eegshow.shape[0])

        self.Stack.toggled.connect(self.__stack_state_change__)
        self.Filter.toggled.connect(self.__filter_state_change__)
        self.Reset.clicked.connect(self.__reset_button__)
        self.plot.clicked.connect(self.__plot_brain_hot__)
        self.clear.clicked.connect(self.__clear_line_edit__)
        self.Add_line.clicked.connect(self.__add_line__)
        self.Clear.clicked.connect(self.__clear_mark_line__)
        self.Undo.clicked.connect(self.__undo__)
        self.From_outside_txt.clicked.connect(self.__from_outside_txt__)
        self.Clear_line.clicked.connect(self.__clear_line__)
        self.update_diagram.clicked.connect(self.__choosen_channel_display__)
        self.__update_diagram__()

    def __choosen_channel_display__(self):
        line_channels = self.channel_choose.text()
        self.channels = list(map(int, line_channels.split('-')))
        print(self.channels,type(self.channels))
        if self.FILTER == False:
            eegnow = copy.deepcopy(EEGnow.eeg_raw)
        else:
            EEGnow.prefilter()
            eegnow = copy.deepcopy(EEGnow.eeg_prefilter)
        if self.STACK == False:
            n_max = eegnow.max()
            n_min = eegnow.min()
            scale = n_max - n_min
            for i in range(eegnow.shape[0]):
                eegnow[i, :] = eegnow[i, :] + i * scale
        eegchannels = eegnow[self.channels,:]
        self.__update_data_edit_diagram__(eeg = eegchannels)

    def __clear_line__(self):
        self.mark_win = numpy.array([])
        self.__update_diagram__()

    def __add_line__(self):
        mark = int(self.mark_blank.text())
        datapoint = int(self.datapoint_blank.text())
        mark_now_list = self.mark_win.tolist()
        mark_now_list.append([mark,datapoint,-1])
        self.mark_win = numpy.array(mark_now_list)
        self.__update_diagram__()
    def __clear_mark_line__(self):
        self.mark_blank.clear()
        self.datapoint_blank.clear()

    def __undo__(self):
        mark_now_list = self.mark_win.tolist()
        mark_now_list = mark_now_list[0:-1]
        self.mark_win = numpy.array(mark_now_list)
        self.__update_diagram__()

    def __from_outside_txt__(self):
        self.From_outside_txt_Dialog = QFileDialog()
        txt_file_name = self.From_outside_txt_Dialog.getOpenFileName(self, 'Open mark txt File', './',
                                                                  "txt file (*.txt)")
        self.txt_file_name = txt_file_name[0]

        EEGnow.readoutMark(self.txt_file_name)
        out_marks = EEGnow.out_marks
        if self.mark_win.size == 0:
            mark_now_list = out_marks
        else:
            mark_now_list = numpy.r_[self.mark_win, out_marks]

        mark_now_list = mark_now_list.tolist()

        self.mark_win = numpy.array(mark_now_list)

        self.__update_diagram__()

    def __clear_line_edit__(self):
        self.start.clear()
        self.end.clear()

    def __plot_brain_hot__(self):
        start_point = int(self.start.text())
        end_point = int(self.end.text())
        EEGnow.readLoc()
        EEGnow.prefilter()
        EEGnow.preprocess()
        EEGnow.brainhot_plotname = 'prefilter'
        EEGnow.ROI = [start_point,end_point]
        EEGnow.visualBoard(BrainHot=True)

    def __reset_button__(self):
        self.channels = range(EEGnow.eeg_raw.shape[0])
        self.__choosen_channel_display__()
        
    def __stack_state_change__(self):
        self.STACK = not self.STACK
        self.__update_diagram__()

    def __filter_state_change__(self):
        self.FILTER = not self.FILTER
        self.__update_diagram__()

    def __update_diagram__(self):

        if self.FILTER == False:
            eegnow = copy.deepcopy(EEGnow.eeg_raw)
        else:
            EEGnow.prefilter()
            eegnow = copy.deepcopy(EEGnow.eeg_prefilter)
        if self.STACK == False:
            n_max = eegnow.max()
            n_min = eegnow.min()
            scale = n_max - n_min
            for i in range(eegnow.shape[0]):
                eegnow[i, :] = eegnow[i, :] + i * scale

        self.__update_data_edit_diagram__(eeg = eegnow[self.channels])


    def __update_data_edit_diagram__(self,eeg=numpy.array([])):
        print("update_data:", eeg.shape)
        L = len(eeg[0])
        stride = 1
        if L >= 1000:
            stride = L // 1000
            eegnow =eeg[0:32, 0:-1:stride]
        else:
            eegnow = eeg
        self.diagram.mpl.start_static_plot( Xdata=numpy.array(range(0,stride*len(eegnow[0]),stride)),
                                            Ydata=eegnow,title = 'EEG_time_domain_signal',
                                            marks= self.mark_win,
                                            Xlabel='Datapoints',Ylabel='Voltage/V')

class SensorEditWindow(QDialog, Ui_Sensor_edit):
    def __init__(self, parent=None):
        super(SensorEditWindow, self).__init__(parent)
        self.setupUi(self)
        EEGnow.readLoc()
        self.sensorName = EEGnow.sensorName
        self.sensorLoc = EEGnow.sensorLoc


        # self.update_diagram.clicked.connect(self.__choosen_channel_display__)
        self.__update_diagram__()

    def __update_diagram__(self):
        self.sensor_diagram.mpl.start_static_scatter(Xdata = self.sensorLoc[0], Ydata = self.sensorLoc[1],labels=self.sensorName)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        EEGnow.preprocess(self, Alpha=True, Beta=True, Gamma=True)

        # initial overview plot
        self.__update_overview__()
        self.__update_datainfo_label__()

        ## File Menu
        # From_vhdr_file binding
        self.actionFrom_vhdr_file.triggered.connect(self.__get_vhdr_file__)

        # From_ced_file binding
        self.actionFrom_ced_file.triggered.connect(self.__get_ced_file__)

        # As_csv_file binding
        self.actionAs_csv_file.triggered.connect(self.__save_csv_file__)

        ## Edit Menu
        # Sensor_edit binding
        self.SensorEdit_Window = SensorEditWindow()
        self.actionSensor_edit.triggered.connect(self.__sensor_edit_show__)
        # Data_edit binding
        self.DataEdit_Window = DataEditWindow()
        self.actionData_edit.triggered.connect(self.__data_edit_show__)
        # Data_info binding
        self.DataInfo_Dialog = QDialog()
        self.DataInfo_Ui = Ui_DataInfo()
        self.DataInfo_Ui.setupUi(self.DataInfo_Dialog)
        self.actionData_info.triggered.connect(self.__data_info_show__)

        # About_this_data binding
        self.AboutThisData_Dialog = QDialog()
        self.AboutThisData_Ui = Ui_AboutThisData()
        self.AboutThisData_Ui.setupUi(self.AboutThisData_Dialog)
        self.actionAbout_this_data.triggered.connect(self.__about_this_data__)

        ## Tools Menu
        self.actionPre_Filter.triggered.connect(self.__prefilter__)
        self.actionFilter_different_bands.triggered.connect(self.__filter_different_bands__)
        self.actionNormalization.triggered.connect(self.__normalization__)
        # self.plotPie(self.mplYearWidget, ListOfPie.yearList, ['blue', 'gray'])
        # self.plotPie(self.mplMonthWidget, ListOfPie.monthList, ['blue', 'gray'])
        # self.plotPie(self.mplWeekWidget, ListOfPie.weekList, ['blue', 'gray'])
        # self.plotPie(self.mplDayWidget, ListOfPie.dayList, ['blue', 'gray'])

    def __update_overview__(self):
        eeg_overview = EEGnow.eeg_raw
        L = len(eeg_overview[0])
        stride = 1
        if L >= 1000:
            stride = L // 1000
            eegnow =eeg_overview[0:32, 0:-1:stride]
        else:
            eegnow = eeg_overview
        print("this ",eegnow.shape, L)
        self.Overview.mpl.start_static_plot(Xdata=numpy.array(range(0,stride*len(eegnow[0]),stride)),
                                            Ydata=eegnow,title = 'Overview_of_eeg_raw_signal',
                                            marks = EEGnow.marks,
                                            Xlabel='Datapoints',Ylabel='Voltage/V')
        # print(EEGnow.marks)

    # Need to be refined
    def __save_csv_file__(self):
        self.As_csv_file_Dialog = QFileDialog()
        csv_file_name = self.As_csv_file_Dialog.getSaveFileName(self, "Save file", "./", ".csv")
        # EEGnow.save
        name_eeg_raw = csv_file_name[0]+csv_file_name[1]
        numpy.savetxt(name_eeg_raw, EEGnow.eeg_raw, delimiter = ',')

    def __get_ced_file__(self):
        self.From_ced_file_Dialog = QFileDialog()
        ced_file_name = self.From_ced_file_Dialog.getOpenFileName(self, 'Open ced File', './',
                                                                    "ced file (*.ced)")
        EEGnow.locpath = ced_file_name[0]

        EEGnow.readLoc()
        self.__update_datainfo_label__()


    def __get_vhdr_file__(self):
        self.From_vhdr_file_Dialog = QFileDialog()
        vhdr_file_name = self.From_vhdr_file_Dialog.getOpenFileName(self, 'Open vhdr File', './',"vhdr file (*.vhdr)")
        tmp_name = vhdr_file_name[0].split('/')[-1]
        EEGnow.eeg_name = tmp_name.split('.')[0]
        EEGnow.dirpath = '--To_do--'
        EEGnow.vhdrpath = vhdr_file_name[0]
        EEGnow.vmrkpath = vhdr_file_name[0].replace('.vhdr','.vmrk')
        EEGnow.eegpath = vhdr_file_name[0].replace('.vhdr','.eeg')

        EEGnow.readBP()
        self.__update_datainfo_label__()
        self.__update_overview__()
        # self.Overview.mpl.start_static_plot(EEGnow.eeg_raw[0:32, 2500:5500].tolist())

    def __update_datainfo_label__(self):
        text_data_info = "<html><head/><body><p>Data_information:</p><p>Name:" + EEGnow.eeg_name + "</p><p>Datapoints:" + str(
            EEGnow.configuration['DataPoints']) + "</p><p>Sampling rate:" + str(
            EEGnow.configuration['Frequency']) + "</p><p><br/></p></body></html>"
        self.datainfo_label.setText(text_data_info)

    def __about_this_data__(self):
        self.AboutThisData_Dialog.show()


    def __data_info_show__(self):
        text_data_info = "<html><head/><body><p>Data_information:</p><p>Name:" + EEGnow.eeg_name + "</p><p>Datapoints:" + str(
            EEGnow.configuration['DataPoints']) + "</p><p>Sampling rate:" + str(
            EEGnow.configuration['Frequency']) + "</p><p><br/></p></body></html>"
        self.DataInfo_Ui.label_data_info.setText(text_data_info)
        self.DataInfo_Dialog.show()

    def __sensor_edit_show__(self):
        self.SensorEdit_Window.__init__()
        self.SensorEdit_Window.show()

    def __data_edit_show__(self):
        self.DataEdit_Window.__init__()
        self.DataEdit_Window.show()

    def __update_data_edit_diagram__(self,eeg=0,stack=False,Filter=False):
        L = len(eeg[0])
        stride = 1
        if L >= 1000:
            stride = L // 1000
            eegnow =eeg[0:32, 0:-1:stride]
        else:
            eegnow = eeg
        self.DataEdit_Ui.diagram.mpl.start_static_plot(Xdata=numpy.array(range(0,stride*len(eegnow[0]),stride)),
                                            Ydata=eegnow,title = 'Overview_of_eeg_raw_signal',
                                            Xlabel='Datapoints',Ylabel='Voltage/V')
    def __prefilter__(self):
        msg = EEGnow.prefilter()
        text_msg = 'Prefilter fail!'
        if msg == True:
            text_msg = 'Prefilter success!'
        reply = QMessageBox.about(self,'Info about Prefilter', text_msg )
        self.__update_overview__(EEGnow.eeg_prefilter[:,2500:-1])



    def __filter_different_bands__(self):
        msg = EEGnow.preprocess(Alpha=True,Beta=True, Gamma=True)
        text_msg = 'Filter different bands operation fail!'
        if msg == True:
            text_msg = 'Filter different bands operation success!'
        reply = QMessageBox.about(self,'Info about filtering different bands',text_msg)

    def __normalization__(self):
        pass

    # def plotPie(self, widget, list, colors):
    #     widget.canvas.ax.clear()
    #     widget.canvas.ax.pie(list, explode=None, labels=None, colors=colors, \
    #                          labeldistance=1.1, autopct=None, shadow=False, \
    #                          startangle=90, pctdistance=0.6)
    #     widget.canvas.draw()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())