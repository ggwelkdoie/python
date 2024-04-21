"""

"""
from pyedflib import EdfWriter, EdfReader, FILETYPE_EDFPLUS
import numpy as np
import scipy
import scipy.io as scio
from pyedflib import EdfWriter, FILETYPE_EDFPLUS
from scipy.signal import filtfilt, resample
import h5py

def _readtxt(filename, comma = True):
    data = []
    with open(filename, 'r') as file_to_read:
        while True:

            if comma == True:
                lines = file_to_read.readline()[:-1]  # 整行读取数据
                if not lines:
                    break
                    pass
                temp = [float(i) for i in lines.split(',')]
                # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                data.append(temp)  # 添加新读取的数据
            else:
                lines = file_to_read.readline()  # 整行读取数据
                if not lines:
                    break
                    pass
                temp = [float(i) for i in lines.split()]
                #    将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
                data.append(temp)  # 添加新读取的数据
            pass
    data = np.array(data)  # 将数据从list类型转换为array类型。
    return data

    #

def _miniPSG_txts_edf(filepath = r"./#2023-06-08 00-15-03 SLP016-2",
                edffilename = r"./#2023-06-08 00-15-03 SLP016-2/SLP016-2.edf",
                 strtime = "08 Jun 2023 00:15:00"):

    # pathname = r".\1209\newsdkdata\data1"
    # strtime = "31 Jul 2020 14:40:30"
    # savefname = r".\1209\T129-psg7chs.edf"
    # srate=500
    # pathname = input("   请输入txt文件绝对路径 (例如 D:/read8chs-to-edf/ljqsleepdata8h): ")
    # # srate = input("   请输入采样率 (Hz): ")
    # strtime = input("   请输入记录起始时间 (日 月 年 时:分:秒，例如：31 Jul 2020 14:40:30): ")
    # savefname = input("   请输入保存edf文件名 (例如 xxxx): ")
    # name = input("   请输入被试名")

    ch_num = 16  # 改为个通道
    filenum = ch_num  # 改为
    ch_num = int(ch_num)
    # srate = [500, 500, 500, 500, 500, 500, 500, 475]    #
    channel_info = []  #
    data_list = []
    # labelname = ('C3-Cz', 'C4-Cz', 'Cz-P3', 'Cz-P4', 'F3-Ft7', 'F4-Ft8', 'Fpz-F3', 'Ft7-C3',
    #              'Ft8-C4', 'M1-O1', 'M2-O2', 'P3-M1', 'P4-M2', 'VEOL-M2', 'VEOU-M1', 'EMG2-EMG1')  # 16通道的标签
    labelname = ('FpZ_M1', 'F3_M1', 'Ft7_M1', 'C3_M1', 'P3_M1', 'O1_M1', 'F4_M2', 'Ft8_M2',
                 'C4_M2', 'Cz_M2', 'P4_M2', 'O2_M2', 'EMG', 'VEOL', 'VEOU', 'EMG')  # 16通道的标签

    # 读取原始数据文件 （例如 16通道 睡眠监测 txt格式）
    txtfilename = ['/C3-Cz.txt', '/C4-Cz.txt', '/Cz-P3.txt', '/Cz-P4.txt','/F3-Ft7.txt', '/F4-Ft8.txt', '/Fpz-F3.txt'
                   , '/Ft7-C3.txt', '/Ft8-C4.txt', '/M1-O1.txt', '/M2-O2.txt', '/P3-M1.txt', '/P4-M2.txt', '/VEOL-M2.txt', '/VEOU-M1.txt','/EMG2-EMG1.txt']

    # subjectname = 'lixiangkui-s5'  # 被试命名 ------------------

    ampfactor = 24  # ------ 需要依据不同放大器设备 手动适配 实测放大倍数 -----------------
    ADC_reference_voltage = 4.5
    ADC_BitDepth = 24  # ------ 虽然是24位，但是此处校正为23
    # kkk = ((1000000 / ampfactor) * ADC_reference_voltage / (2 ** ADC_BitDepth))  # --- 注意此处 系数有误，可能与ADC有关，需要
    # ((ch1 / 2500000) + 1) * 1000 * 9 / 7 / 3  #kkk和jjj由此公式计算
    #kkk = 0.000171428571428
    #jjj = 428.571
    kkk = 0.0044465  # x * 37.3 * 1000 / 8388608    x * 2.5 * 1000000 / 67 / 8388608
    jjj = 0
    # txtdata = []

    # startpoint = 0
    # datasignalsflag = True
    datasignals = []
    print('      \n          正在转换，请等待 ！ ')
    for fi in range(filenum):

        if fi == 15:  # psg 的EMG滤波
            xtemp = _readtxt(filepath + txtfilename[fi], False)
            st = kkk * xtemp[0, 20000:] + jjj
            s = st - np.mean(st)

            # filterFile = './IIR-ECG-BS-Elliptic-Fs500-Fpass47-Fpass53-Astop21.mat'
            # filtercoeff = scio.loadmat(filterFile)
            # a = filtercoeff['a']
            # b = filtercoeff['b']
            # a = a.reshape(np.ma.size(a, 1))
            # b = b.reshape(np.ma.size(b, 1))
            # y1l = filtfilt(b, a, s)  # 50Hz陷波器
            # y1l = s
            # y1 = s

            filterFile = './IIR-EMG-HP-Elliptic-Fs1000-Fpass12-Fstop9-Astop60.mat'
            filtercoeff = scio.loadmat(filterFile)
            a = filtercoeff['a']
            b = filtercoeff['b']
            a = a.reshape(np.ma.size(a, 1))
            b = b.reshape(np.ma.size(b, 1))
            y1 = filtfilt(b, a, s)
            filterFile2 = './IIR-EMG-LP-Elliptic-Fs1000-Fpass90-Fstop99-Astop60.mat'
            filtercoeff = scio.loadmat(filterFile2)
            a = filtercoeff['a']
            b = filtercoeff['b']
            a = a.reshape(np.ma.size(a, 1))
            b = b.reshape(np.ma.size(b, 1))
            y2 = filtfilt(b, a, y1)

        else:  # PSG 设备的EOG EEG

            xtemp = _readtxt(filepath + txtfilename[fi], False)
            st = kkk * xtemp[0, 20000:] + jjj
            s = st - np.mean(st)

            filterFile = './IIR-EEG-LP-Elliptic-Fs1000-Fpass40-Fstop45-Astop60.mat'
            filtercoeff = scio.loadmat(filterFile)
            a = filtercoeff['a']
            b = filtercoeff['b']
            a = a.reshape(np.ma.size(a, 1))
            b = b.reshape(np.ma.size(b, 1))
            y1 = filtfilt(b, a, s)
            # y1 =s

            filterFile2 = './IIR-EEG-HP-Elliptic-Fs1000-Fpass0.6-Fstop0.4-Astop50.mat'
            filtercoeff = scio.loadmat(filterFile2)
            a = filtercoeff['a']
            b = filtercoeff['b']
            a = a.reshape(np.ma.size(a, 1))
            b = b.reshape(np.ma.size(b, 1))
            y2 = filtfilt(b, a, y1)
            # y2 = y1

        # L = np.size(y2)
        # y3 = resample(y2, L)
        datasignals.append(y2)
    datasignals[:,0] = datasignals[:,3]+datasignals[:,0]+datasignals[:,8]
    datasignals[:,1] = datasignals[:,3]
    datasignals[:,2] = datasignals[:,3]
    datasignals[:,3] = datasignals[:,3]
    datasignals[:,4] = datasignals[:,3]
    datasignals[:,5] = datasignals[:,3]
    datasignals[:,6] = datasignals[:,3]
    datasignals[:,7] = datasignals[:,3]
    datasignals[:,8] = datasignals[:,3]
    datasignals[:,9] = datasignals[:,5]
    datasignals[:,10] = datasignals[:,3]
    datasignals[:,11] = datasignals[:,3]
    datasignals[:,12] = datasignals[:,5]
    datasignals[:,13] = datasignals[:,3]
    datasignals[:,14] = datasignals[:,5]
    datasignals[:,15] = []
    # 将双极导联转换为单极导联
    # FpZ_M1 = Fpz_F3 + F3_Ft7 + Ft7_C3 + C3_Cz + Cz_P3 + P3_M1;
    # F3_M1 = F3_Ft7 + Ft7_C3 + C3_Cz + Cz_P3 + P3_M1;
    # Ft7_M1 = Ft7_C3 + C3_Cz + Cz_P3 + P3_M1;
    # C3_M1 = C3_Cz + Cz_P3 + P3_M1;
    # P3_M1 = P3_M1;
    # O1_M1 = -M1_O1;
    # F4_M2 = F4_Ft8 + Ft8_C4 + C4_Cz + Cz_P4 + P4_M2;
    # Ft8_M2 = Ft8_C4 + C4_Cz + Cz_P4 + P4_M2;
    # C4_M2 = C4_Cz + Cz_P4 + P4_M2;
    # Cz_M2 = Cz_P4 + P4_M2;
    # P4_M2 = P4_M2;
    # O2_M2 = -M2_O2;
    # VEOL = VEOL_M2;
    # VEOU = VEOU_M1;
    # EMG = EMG2_EMG1;

    str_filterInfo = "IIR"
    for chi in range(0, ch_num):
        ch_dict = {'label': labelname[chi], 'dimension': 'uV',
                   'sample_rate': 1000, 'physical_max': 20000,  # 20mV
                   'physical_min': -20000, 'digital_max': 32768,
                   'digital_min': -32767,
                   'transducer': '-',  # ------ 修改 放大器设备命名 -------
                   'prefilter': str_filterInfo}  # ------ 修改 滤波器信息 -------
        channel_info.append(ch_dict)

    fedf = EdfWriter(edffilename, ch_num, file_type=FILETYPE_EDFPLUS)
    fedf.setSignalHeaders(channel_info)
    fedf.setStartdatetime(strtime)
    fedf.writeSamples(np.round(datasignals, 2))
    fedf.close()
    del fedf
    print('      \n          PSG 转 换 成 功 ！ 请等待 ··· ')
    # input("      \n             请输入回车结束")

if __name__ == '__main__':

    subID=2


    _miniPSG_txts_edf()

