from src_fun.eeg_read_save.eeg_read import *
from src_fun.eeg_preprocess.eegFilter import Filtereeg
from src_fun.eeg_visual_board.eeg_visual import *
import os

class EEGData(object):

    def __init__(self):

        self.dirpath = "/home/qch/Desktop/EEGproject/data/"
        self.eeg_name = "happy"

        self.eegpath = self.dirpath + self.eeg_name + ".eeg"
        self.vhdrpath = self.dirpath + self.eeg_name + ".vhdr"
        self.vmrkpath = self.dirpath + self.eeg_name + ".vmrk"

        self.locpath = "/home/qch/Desktop/EEGproject/data/Standard-10-20-Cap81.ced"

        self.eeg_raw = []
        self.eeg_prefilter = []
        self.eeg_ICA = []

        self.eeg_bands_alpha = []
        self.eeg_bands_beta = []
        self.eeg_bands_gamma = []

        self.eeg_features_timedomain = []
        self.eeg_features_frequencydomain = []

        self.configuration = {}
        self.marks = []
        self.out_marks = []
        self.ROI = [2000, 4000]
        self.brainhot_plotname = 'raw'

        self.eeg_raw, self.configuration, self.marks = readBP(
                                   self.eegpath, self.vhdrpath, self.vmrkpath)
        print(self.eeg_raw.shape,self.configuration, self.marks)
        # eeg_visual_raw(self.eeg_raw)
    def readBP(self):
        self.eeg_raw, self.configuration, self.marks = readBP(
                                   self.eegpath, self.vhdrpath, self.vmrkpath)

        print(self.eeg_raw.shape)


    def readLoc(self):
        print(self.locpath)
        self.sensorLoc, self.sensorName = readLoc(self.locpath)
        # print(self.sensorLoc,self.sensorName,self.sensorLoc.shape)

    def readoutMark(self,outmarkpath):
        self.out_marks = outmarkRead(outmarkpath=outmarkpath)

    def prefilter(self):
        self.eeg_prefilter = Filtereeg(eegdata=self.eeg_raw, methodID="BUTTER",
                                         fs=self.configuration['Frequency'], downfz=1, upfz=64)
        return True

    def preprocess(self,ICA=False, Alpha=False, Beta=False, Gamma=False):

        if ICA==True:
            print("EEGClass: wait to realize ICA")
        if Alpha==True:
            self.eeg_bands_alpha = Filtereeg(eegdata=self.eeg_raw,methodID="BUTTER",
                            fs=self.configuration['Frequency'],downfz=8,upfz=13)
            print(self.eeg_bands_alpha.shape,self.configuration['Frequency'])
            print("EEGClass: Alpha extracted")
        if Beta==True:
            self.eeg_bands_beta = Filtereeg(eegdata=self.eeg_raw,methodID="BUTTER",
                            fs=self.configuration['Frequency'],downfz=16,upfz=31)
            print(self.eeg_bands_beta.shape)
            print("EEGClass: Beta extracted")
        if Gamma==True:
            self.eeg_bands_gamma = Filtereeg(eegdata=self.eeg_raw,methodID="BUTTER",
                            fs=self.configuration['Frequency'],downfz=32,upfz=64)
            print(self.eeg_bands_gamma.shape)
            print("EEGClass: Gamma extracted")

        return True
    def visualBoard(self, Raw=False, Sensor=False, ICA=False, Alpha=False, Beta=False
                    , Gamma=False, BrainHot=False):
        if Raw==True:
            Visualeeg32_subplot(self.eeg_raw,'Raw')
            Visualeeg32_one(self.eeg_raw[0:32,:],'Raw')
            print("EEGClass: ploting rawdata")
        if Sensor==True:
            Visualeeg_sensor2D(self.sensorName,self.sensorLoc)
            Visualeeg_sensor3D(self.sensorName,self.sensorLoc)
            print("EEGClass: plot sensor location\n")
            print(self.sensorLoc,self.sensorName)
        if ICA==True:
            print("EEGClass: wait to realize")
        if Alpha==True:
            Visualeeg32_one(self.eeg_bands_alpha,'Alpha')
            print(self.eeg_bands_alpha.shape)
            print("EEGClass: ploting alpha")
        if Beta==True:
            Visualeeg32_one(self.eeg_bands_beta,'Beta')
            print("EEGClass: ploting beta")
        if Gamma==True:
            Visualeeg32_one(self.eeg_bands_gamma,'Gamma')
            print("EEGClass: ploting gamma")
        if BrainHot==True:
            left=self.ROI[0]
            right=self.ROI[1]
            if self.brainhot_plotname == 'raw':
                eeg_brainhot = self.eeg_raw[:,left:right]
            elif self.brainhot_plotname == 'alpha':
                eeg_brainhot = self.eeg_bands_alpha[:,left:right]
            elif self.brainhot_plotname == 'beta':
                eeg_brainhot = self.eeg_bands_beta[:,left:right]
            elif self.brainhot_plotname == 'gamma':
                eeg_brainhot = self.eeg_bands_gamma[:,left:right]
            elif self.brainhot_plotname == 'prefilter':
                eeg_brainhot = self.eeg_prefilter
            else:
                eeg_brainhot = self.eeg_raw
            print(eeg_brainhot.shape,self.brainhot_plotname,self.sensorLoc.shape)
            Visual_BrainHot_all(self.brainhot_plotname,eeg_brainhot, self.sensorName, self.sensorLoc)
            # Visual_BrainHot_animation(self.brainhot_plotname,eeg_brainhot, self.sensorName, self.sensorLoc)

            # Visual_BrainHot('alpha',self.eeg_bands_alpha[:,2000:-2000], self.sensorName, self.sensorLoc)
            # Visual_BrainHot('beta',self.eeg_bands_beta[:,2000:-2000], self.sensorName, self.sensorLoc)
            # Visual_BrainHot('gamma',self.eeg_bands_gamma[:,2000:-2000], self.sensorName, self.sensorLoc)
            print("EEGClass: ploting brainhot map")
# print(os.getcwd())
# e = EEGData()
