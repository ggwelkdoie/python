from xml.dom import minidom  # 导入模块
from csv import writer, reader
import os
import re

global duration
duration = [0]*120

def readrml():
    for idx in range(120):
        wStages = []
        wStarts = []
        path = r'C:\Users\15028\Desktop\ysf\rml_ysf\YB%03d.rml' % (idx+1)
        savefname = r'C:\Users\15028\Desktop\ysf\G3rml_CoarseStages\G3rml_CoarseStagesSLP%03d.csv' % (idx+1)
        if not os.path.exists(path):
            continue
        dom = minidom.parse(path)
        Nodedur = dom.getElementsByTagName("Duration")
        duration[idx] = int(Nodedur[0].childNodes[0].data)
        NodeUser = dom.getElementsByTagName("UserStaging")
        if NodeUser:
            NodeStages = NodeUser[0].childNodes[1].getElementsByTagName("Stage")
            with open(savefname, 'w+', newline='') as csvf:
                csvwriter = writer(csvf, dialect='excel')
                for stagei in NodeStages:
                    wStages.append(stagei.getAttribute('Type'))
                    wStarts.append(stagei.getAttribute('Start'))
                    csvwriter.writerow([stagei.getAttribute('Type'), stagei.getAttribute('Start')])
                print('一个人结束', idx)
    print(duration)



def refinelabels():

    labeldict = {'NotScored':0, 'Wake': 0, 'NonREM1': 1, 'NonREM2': 2, 'NonREM3': 3, 'REM': 4}
    labeldictR = {0: 'Wake', 1: 'NonREM1', 2: 'NonREM2', 3: 'NonREM3', 4: 'REM'}

    nowstage = ['Wake', '0']

    for idx in range(120):
        stageslist = []
        ilabel = []
        # filename = r'C:\Users\15028\Desktop\ysf\G3rml_CoarseStages\G3rml_CoarseStagesSLP%03d.csv' % (idx+1)
        # savefname = r'C:\Users\15028\Desktop\ysf\refined_Stage_Labels\YB%03d.txt' % (idx + 1)
        filename = r'E:\zyhGraduation\data\EEGdata\edfs\CLA016_all.csv'
        savefname = r'E:\zyhGraduation\data\EEGdata\edfs\CLA016_all.txt'
        if not os.path.exists(filename):
            continue
        with open(filename, newline='')  as f:
            readercsv = reader(f)
            # 使用csv的reader()方法，创建一个reader对象
            for row in readercsv:
                # 遍历reader对象的每一行
                stageslist.append(row)
        dura_num = duration[idx]//30
        for i_30s in range(dura_num):
            i_1s = i_30s * 30  # 递增30秒

            if len(stageslist) > 0:
                if i_1s >= int(stageslist[0][1]):  # 判断时间点
                    nowstage = stageslist[0]
                    stageslist.pop(0)  # 保存最新转变点，并从列表去除
                    ilabel.append(labeldict[nowstage[0]])
                else:
                    ilabel.append(labeldict[nowstage[0]])

            elif len(stageslist) == 0:
                ilabel.append(labeldict[nowstage[0]])

        # 保存labels
        # with open(savefname, 'w+', newline='') as csvf:
        #     csvwriter = writer(csvf, dialect='excel')
        #     ilabelvertical = list(map(lambda x: [x], ilabel))
        #     csvwriter.writerows(ilabelvertical)
        with open(savefname, 'w+', newline='\n') as txtf:
            txtwriter = writer(txtf)
            ilabelvertical = list(map(lambda x: [x], ilabel))
            txtwriter.writerows(ilabelvertical)



def total_labels():
    import numpy as np
    from h5py import File as h5file
    import pandas as pd
    total_labels_list=[]
    excel_savefname = r'D:\experiment\experiment data\ymj exp data\sleep stage\total_labels.xlsx'

    for idx in range(20):
        labels = []
        filename = r'D:\experiment\experiment data\ymj exp data\sleep stage\csv\refined_Stage_Labels\refined_Stage_LabelsSLP%03d.csv' % (idx + 1)
        if not os.path.exists(filename):
            continue
        with open(filename, newline='')  as f:
            readercsv = reader(f)
            for row in readercsv:
                # 遍历reader对象的每一行
                labels.append(int(row[0]))
        total_labels_list .append(labels)
    total_labels = np.array(total_labels_list)
    data = pd.DataFrame(total_labels)
    writer = pd.ExcelWriter(excel_savefname)  # 写入Excel文件
    data.to_excel(writer, '60per', float_format='%d', header=False,index=False)  # ‘page_1’是写入excel的sheet名
    writer.save()
    writer.close()

    return total_labels




if __name__ == '__main__':
    refinelabels()
    # total_labels()