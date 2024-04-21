import pandas as pd
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import  glob
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.stats import ttest_ind
import random
import math
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d

# 加载数据
folder_path = r'E:\zyhGraduation\data\PSDscope\OUTPUT\REMcsv'
excel_files = glob.glob(os.path.join(folder_path, '*.csv'))
df1 = pd.read_csv(excel_files[0], sep="\t", header=0)
average_psd_by_f1 = df1.groupby('F')['PSD'].mean().reset_index()
f_good = average_psd_by_f1['F'].values[0:159]
df_ave = np.zeros((len(average_psd_by_f1), 40))
i = 0
for file in excel_files:
    df = pd.read_csv(file, sep="\t", header=0)
    average_psd_by_f = df.groupby('F')['PSD'].mean().reset_index()
    Pxx_good = average_psd_by_f['PSD'].values
    df_ave[:,i] = Pxx_good
    i = i + 1

df_ave_MS = df_ave[0:159,[0,1,2,3,4,5,6,7,10,12,15,16,17,19,20,21,22,23,24]]
df_ave_GS = df_ave[0:159,[25,26,27,28,29,30,31,32,33,35,36,37,38,39]]

mean_MS = np.mean(df_ave_MS, axis=1)
std_MS = np.std(df_ave_MS, axis=1)
mean_GS = np.mean(df_ave_GS, axis=1)
std_GS = np.std(df_ave_GS, axis=1)
t_stats, p_values = ttest_ind(df_ave_MS, df_ave_GS, axis=1)

window_size = 3
half_window = window_size // 2
extended_mean_MS = np.pad(mean_MS, (half_window, half_window), mode='edge')
weights = np.ones(window_size) / window_size
mean_MS1 = np.convolve(extended_mean_MS, weights, mode='valid')
# extended_mean_MS1 = np.pad(mean_MS1, (half_window, half_window), mode='edge')
# mean_MS2 = np.convolve(extended_mean_MS1, weights, mode='valid')

extended_mean_GS = np.pad(mean_GS, (half_window, half_window), mode='edge')
mean_GS1 = np.convolve(extended_mean_GS, weights, mode='valid')

extended_std_MS = np.pad(std_MS, (half_window, half_window), mode='edge')
std_MS1 = np.convolve(extended_std_MS, weights, mode='valid')
# extended_std_MS1 = np.pad(std_MS1, (half_window, half_window), mode='edge')
# std_MS2 = np.convolve(extended_std_MS1, weights, mode='valid')
# extended_std_MS2 = np.pad(std_MS2, (half_window, half_window), mode='edge')
# std_MS3 = np.convolve(extended_std_MS2, weights, mode='valid')

extended_std_GS = np.pad(std_GS, (half_window, half_window), mode='edge')
std_GS1 = np.convolve(extended_std_GS, weights, mode='valid')

print("mean_GS30 ", mean_GS1[118], " mean_GS40 ", mean_GS1[158], " mean_MS30 ", mean_MS1[118], " mean_MS40 ", mean_MS1[158])
print("mean_GS ", (mean_GS1[158] - mean_GS1[118]) / (10 * math.log(30, 10) - 10 * math.log(40, 10)), " mean_MS ", (mean_MS1[158] - mean_MS1[118]) / (10 * math.log(30, 10) - 10 * math.log(40, 10)))
plt.figure(figsize=(6, 5))
plt.plot(f_good[0:159], mean_MS1, label='MS', color='blue')
plt.fill_between(f_good[0:159],mean_MS1.flatten()-std_MS1.flatten(),mean_MS1.flatten()+std_MS1.flatten(), color='blue',alpha=0.2)
plt.plot(f_good[0:159],mean_GS1,label='GS', color='red')
plt.fill_between(f_good[0:159],mean_GS1.flatten()-std_GS1.flatten(),mean_GS1.flatten()+std_GS1.flatten(),color='red',alpha=0.2)
plt.xlim([0.47, 43])
plt.legend()
# plt.xticks(fontsize=17)
# plt.yticks(fontsize=17)
plt.xticks(fontsize=19)
plt.yticks(fontsize=19)
plt.subplots_adjust(left=0.16, bottom=0.16, right=0.98, top=0.98)
font = FontProperties(fname='C:\\Windows\\Fonts\\simsun.ttc', size=23)
plt.xlabel('频率(10*log(Hz))', fontproperties=font)
plt.ylabel('功率(dB)', fontproperties=font, labelpad=-1)
plt.xscale('log')
plt.axvline(x=30,color='y',linestyle='--')
plt.axvline(x=40,color='y',linestyle='--')
# N2
# plt.text(30, -21.5, f'{30}', ha='center', va='bottom', fontdict={'size': 16})
# plt.text(40, -21.5, f'{45}', ha='center', va='bottom', fontdict={'size': 16})
# N3
# plt.text(30, -23.5, f'{30}', ha='center', va='bottom', fontdict={'size': 16})
# plt.text(40, -23.5, f'{45}', ha='center', va='bottom', fontdict={'size': 16})
# NREM
# plt.text(30, -22, f'{30}', ha='center', va='bottom', fontdict={'size': 16})
# plt.text(40, -22, f'{45}', ha='center', va='bottom', fontdict={'size': 16})
# REM
plt.text(30, -21.5, f'{30}', ha='center', va='bottom', fontdict={'size': 16})
plt.text(40, -21.5, f'{45}', ha='center', va='bottom', fontdict={'size': 16})

plt.savefig(r'E:\zyhGraduation\data\分析结果\图\figure4_4.svg',bbox_inches='tight')
plt.show()