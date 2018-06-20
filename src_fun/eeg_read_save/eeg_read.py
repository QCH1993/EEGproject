import numpy as np

def readLoc(locpath):
    LOC = ["AF7","Fp1","Fpz","Fp2","AF8","AF3","AF4","F5","F3","Fz","F4","F6",\
            "C5","C3","C1","Cz","C2","C4","C6","CP5","CPz","CP6","P3","Pz","P4",\
            "P7","PO3","PO4","P8","O1","Oz","O2"]

    LocationXYZList = []
    label = []
    if locpath.split('.')[1] != "ced":
        print("Location file format is wrong")
    else:
        locfile = open(locpath,'r')
        i=0
        for line in locfile:
            for i in range(len(LOC)):
                strlist = line.split()
                if LOC[i].lower() == strlist[1].lower():
                    label.append(LOC[i])
                    # print("match",strlist,LOC[i])
                    for s in strlist[4:7]:
                        LocationXYZList.append(float(s))

        LocationXYZline = np.array(LocationXYZList)
        LocationXYZ = np.reshape(LocationXYZline,(-1,3))
        return LocationXYZ,label



def readBP( eegpath,vhdrpath,vmrkpath):
    configuration = vhdrRead(vhdrpath=vhdrpath)
    rawdata = eegRead(eegpath=eegpath,configuration=configuration)
    mark = vmrkRead(vmrkpath=vmrkpath)
    return rawdata,configuration,mark

def vhdrRead(vhdrpath):

    vhdrfile = open(vhdrpath, 'r')
    configuration = {}
    for line in vhdrfile:
        if line.find("DataFormat=")==0:
            configuration['DataFormat'] = \
                                        line.split('=')[1][0:-1]
        if line.find("DataOrientation=")==0:
            configuration['DataOrientation'] = \
                                        line.split('=')[1][0:-1]
        if line.find("DataType=")==0:
            configuration['DataType'] = \
                                        line.split('=')[1][0:-1]
        if line.find("NumberOfChannels=")==0:
            configuration['NumberOfChannels'] = \
                                        int(line.split('=')[1][0:-1])
        if line.find("DataPoints=")==0:
            configuration['DataPoints'] = \
                                        int(line.split('=')[1][0:-1])
        if line.find("SamplingInterval=")==0:
            configuration['SamplingInterval'] = \
                                        int(line.split('=')[1][0:-1])
            configuration['Frequency'] = \
                    1000000/configuration['SamplingInterval']
        if line.find("BinaryFormat=")==0:
            configuration['BinaryFormat'] = \
                                        line.split('=')[1][0:-1]
    vhdrfile.close()
    return configuration


def eegRead(eegpath,configuration):

    if configuration['BinaryFormat'].find('IEEE_FLOAT_32') != 0:
        print("ERRO:eegRead-the format is not IEEE_FLOAT_32\n")

    else:
        eegline = np.fromfile(eegpath, dtype=np.float32)
        print(eegline.shape)
        col = configuration['NumberOfChannels']
        row = eegline.shape[0] // col

        try:
            eeg = eegline.reshape((row,col)).T
            return eeg
        except ValueError:
            print("EERO: eegline does not match the \
                    [N_channel,single_channel_datapoint]\n")


def vmrkRead(vmrkpath):
    vmrkfile = open(vmrkpath, 'r')
    markline = []
    for line in vmrkfile:
        if line.find("Mk")==0:
            for number in line.split(',')[1:-1]:
                markline.append(int(number))

    mark = np.array(markline).reshape(-1,3)
    return mark

def outmarkRead(outmarkpath):
    outmarkfile = open(outmarkpath, 'r')
    markline = []
    for line in outmarkfile:
        for number in line.split(','):
             markline.append(float(number))
        markline.append(-1)

    mark = np.array(markline).reshape(-1, 3)
    return mark
