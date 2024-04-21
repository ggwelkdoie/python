import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.stats import ttest_ind
import matplotlib.gridspec as gridspec
from matplotlib.ticker import NullLocator
# 读取上传的文件
folder_path = r'E:\zyhGraduation\data\PSDscope\OUTPUT\N2csv'
excel_files = glob.glob(os.path.join(folder_path, '*.csv'))
df1 = pd.read_csv(excel_files[0], sep="\t", header=0)
average_psd_by_f1 = df1.groupby('F')['PSD'].mean().reset_index()
f_good = average_psd_by_f1['F'].values
df_ave = np.zeros((len(average_psd_by_f1), 40))
i = 0
for file in excel_files:
    df = pd.read_csv(file, sep="\t", header=0)
    average_psd_by_f = df.groupby('F')['PSD'].mean().reset_index()
    Pxx_good = average_psd_by_f['PSD'].values
    df_ave[:, i] = Pxx_good
    i = i + 1
df_ave_GS = df_ave[:,0:20]
df_ave_MS = df_ave[:,20:40]
# df_ave_GS = np.hstack((df_ave[:,0:5],df_ave[:,0:5],df_ave[:,0:5]))
# df_ave_MS = np.hstack((df_ave[:,5:10],df_ave[:,5:10],df_ave[:,5:10]))

mean_GS = np.mean(df_ave_GS, axis=1)
std_GS = np.std(df_ave_GS, axis=1) * 0.3
mean_MS = np.mean(df_ave_MS, axis=1)
std_MS = np.std(df_ave_MS, axis=1) * 0.3
t_stats, p_values = ttest_ind(df_ave_GS, df_ave_MS, axis=1)

plt.figure(figsize=(5,6))
ax1 = plt.axes([0.16, 0.1, 0.8, 0.85])
# ax1 = plt.axes()
plt.xscale('log')
gs = gridspec.GridSpec(2,1,height_ratios=[6,1])
plt.plot(f_good, mean_GS, label='NREM',color='blue')
plt.fill_between(f_good, mean_GS.flatten() - 2 * std_GS.flatten(), mean_GS.flatten() + 2 * std_GS.flatten(), color='blue', alpha=0.2)
plt.plot(f_good, mean_MS, label='REM',color='red')
plt.fill_between(f_good, mean_MS.flatten() - 2 * std_MS.flatten(), mean_MS.flatten() + 2 * std_MS.flatten(), color='red', alpha=0.2)
ax1.set_ylabel('EEG Power Spectral Density (uV^2/Hz)', fontsize=14)
ax1.set_xlabel('Frequency(log10(Hz))', fontsize=14)
plt.legend()
plt.title('MS', fontsize=14)
ax1.set_xlim(0.5, 40)
ax1.yaxis.set_minor_locator(plt.NullLocator())  # Remove y-axis minor ticks
ax1.spines['top'].set_visible(False)  # Hide the top spine
ax1.spines['right'].set_visible(False)  # Hide the right spine
plt.grid(False)
ax = plt.gca()
ax.xaxis.set_minor_locator(NullLocator())
plt.xticks([1, 10], [0, 1])
plt.show()