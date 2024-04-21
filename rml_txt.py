import random
from xml.dom import minidom  # 导入模块
from csv import writer, reader
import os
import re
import numpy as np

def readrml():
    for idx in range(20):
        wStages = []
        wStarts = []
        all = []
        filename = r'D:\experiment\experiment data\ymj exp data\sleep stage\rml\SLP%03d.rml' % (idx+1)
        savefname = r'D:\experiment\experiment data\YSF data\txt\SLP%03d.txt' % (idx+1)
        if not os.path.exists(filename):
            continue
        dom = minidom.parse(filename)
        Nodedur = dom.getElementsByTagName("Duration")
        duration = int(Nodedur[0].childNodes[0].data)
        duration = (duration // 30) * 30
        NodeUser = dom.getElementsByTagName("UserStaging")
        if NodeUser:
            NodeStages = NodeUser[0].childNodes[1].getElementsByTagName("Stage")
            with open(savefname, 'w+', newline='\n') as txtf:
                txtwriter = writer(txtf,delimiter='\t')
                for stagei in NodeStages:
                    wStages.append(stagei.getAttribute('Type'))
                    wStarts.append(stagei.getAttribute('Start'))
                wEnds = wStarts[1:]
                wEnds.append(int(duration))
                for i in range(len(NodeStages)):
                    txtwriter.writerow([wStages[i],wStarts[i],wEnds[i]])
                print('第%d个人结束' % (idx+1))

if __name__ == '__main__':
    readrml()




