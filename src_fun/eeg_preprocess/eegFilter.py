import numpy as np
from scipy.signal import butter,lfilter
DEFAULT_EEG = np.zeros([37,1000])
def Filtereeg(eegdata=DEFAULT_EEG,methodID="BUTTER",fs=500,downfz=1,upfz=50):
    channels,points = eegdata.shape
    eegdataF = np.zeros(points)
    for row in eegdata:
        eegdataf = Filtereeg_single(row,methodID,fs,downfz,upfz)
        eegdataF = np.row_stack((eegdataF,eegdataf))
    eegdataF = np.delete(eegdataF,[0],axis=0)
    return eegdataF

def Filtereeg_single(eegdata_single_channel=DEFAULT_EEG[0],methodID="BUTTER",fs=500,downfz=1,upfz=50):
    methods = {"BUTTER":ButterFiltereeg,
                "ELLIPSE":EllipseFiltereeg,
                "OTHERS":OthersSituation}
    return methods.get(methodID)(eegdata_single_channel,fs,downfz,upfz)
#ButterFiltereeg Design
def ButterFiltereeg(eegdata_single_channel=DEFAULT_EEG[0],fs=500,downfz=1,upfz=50):
    eegdata_single_channel = butter_bandpass_filter(eegdata_single_channel,\
                                                    downfz,upfz,fs,order=6)
    return eegdata_single_channel

def butter_bandpass(lowcut,highcut,fs,order=5):
    nyq = 0.5*fs
    low = lowcut / nyq
    high = highcut / nyq
    b,a = butter(order,[low,high],btype='bandpass')
    return b,a
def butter_bandpass_filter(data,lowcut,highcut,fs,order=5):
    b,a = butter_bandpass(lowcut,highcut, fs,order=order)
    y = lfilter(b,a,data)
    return y

def EllipseFiltereeg(eegdata_single_channel=DEFAULT_EEG[0],fs=500,downfz=1,upfz=50):
    print("EllipseFiltereeg hasnt been realized,using ButterFiltereeg instead")
    return ButterFiltereeg(eegdata_single_channel,downfz,upfz)


def OthersSituation(eegdata_single_channel=DEFAULT_EEG[0],fs=500,downfz=1,upfz=50):
    print("OthersSituation hasnt been realized,using ButterFiltereeg instead")
    return ButterFiltereeg(eegdata_single_channel,downfz,upfz)
