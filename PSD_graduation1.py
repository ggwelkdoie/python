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
folder_path = r'E:\zyhGraduation\data\PSDscope\OUTPUT\N2csv'
excel_files = glob.glob(os.path.join(folder_path, '*.csv'))
df1 = pd.read_csv(excel_files[0], sep="\t", header=0)
average_psd_by_f1 = df1.groupby('F')['PSD'].mean().reset_index()
f_good = average_psd_by_f1['F'].values
df_ave = np.zeros((len(average_psd_by_f1), 40))
print(len(average_psd_by_f1))
i = 0
for file in excel_files:
    df = pd.read_csv(file, sep="\t", header=0)
    average_psd_by_f = df.groupby('F')['PSD'].mean().reset_index()
    Pxx_good = average_psd_by_f['PSD'].values
    df_ave[:,i] = Pxx_good
    i = i + 1
chengji = np.zeros((159, 1))
for j in range(0,159):
    if j < 80:
        chengji[j] = 1
    else:
        chengji[j] = 1.0005
df_ave_GS = df_ave[0:159,0:25]
df_ave_MS = df_ave[0:159,25:40]
# df_ave_GS = np.hstack((df_ave[:,0:40:2],df_ave[:,0:20]))
# df_ave_MS = np.hstack((df_ave[:,20:40],df_ave[:,20:40]))
# df_ave_GS = np.hstack((df_ave[:,21:31],df_ave[:,21:31],df_ave[:,21:31]))
# df_ave_MS = np.hstack((df_ave[:,31:41],df_ave[:,31:41],df_ave[:,31:41]))

mean_GS = np.mean(df_ave_GS, axis=1)
std_GS = np.std(df_ave_GS, axis=1)
mean_MS = np.mean(df_ave_MS, axis=1)
std_MS = np.std(df_ave_MS, axis=1)
t_stats, p_values = ttest_ind(df_ave_GS, df_ave_MS, axis=1)

# window_size = 3
# half_window = window_size // 2
# extended_x = np.pad(mean_GS, (half_window, half_window), mode='edge')
# weights = np.ones(window_size) / window_size
# mean_GS1 = np.convolve(extended_x, weights, mode='valid')
#
# extended_x1 = np.pad(mean_MS, (half_window, half_window), mode='edge')
# weights = np.ones(window_size) / window_size
# mean_MS1 = np.convolve(extended_x1, weights, mode='valid')
#
# extended_x2 = np.pad(std_GS, (half_window, half_window), mode='edge')
# weights = np.ones(window_size) / window_size
# std_GS1 = np.convolve(extended_x2, weights, mode='valid')
#
# extended_x3 = np.pad(std_MS, (half_window, half_window), mode='edge')
# weights = np.ones(window_size) / window_size
# std_MS1 = np.convolve(extended_x3, weights, mode='valid')
#
# extended_x4 = np.pad(p_values, (half_window, half_window), mode='edge')
# weights = np.ones(window_size) / window_size
# p_values1 = np.convolve(extended_x4, weights, mode='valid')
plt.plot(f_good[0:159], mean_GS, label='GS')
plt.fill_between(f_good[0:159],mean_GS.flatten()-std_GS.flatten(),mean_GS.flatten()+std_GS.flatten(), color='blue',alpha=0.2)
plt.plot(f_good[0:159],mean_MS,label='MS')
plt.fill_between(f_good[0:159],mean_MS.flatten()-std_MS.flatten(),mean_MS.flatten()+std_MS.flatten(),color='red',alpha=0.2)
plt.xlim([0.47, 43])
plt.xscale('log')
plt.axvline(x=30,color='y',linestyle='--')
plt.axvline(x=40,color='y',linestyle='--')

# ax1 = plt.axes([0.12, 0.33, 0.85, 0.64])
# gs = gridspec.GridSpec(2,1,height_ratios=[6,1])
# ax1.plot(f_good, mean_GS, label='GS')
# ax1.fill_between(f_good, mean_GS.flatten() - std_GS.flatten(), mean_GS.flatten() + std_GS.flatten(), color='blue', alpha=0.2)
# ax1.plot(f_good, mean_MS, label='MS')
# ax1.fill_between(f_good, mean_MS.flatten() - std_MS.flatten(), mean_MS.flatten() + std_MS.flatten(), color='red', alpha=0.2)
# # ax1.plot(f_good, mean_GS1, label='GS')
# # ax1.fill_between(f_good, mean_GS1.flatten() - std_GS1.flatten(), mean_GS1.flatten() + std_GS1.flatten(), color='blue', alpha=0.2)
# # ax1.plot(f_good, mean_MS1, label='GS')
# # ax1.fill_between(f_good, mean_MS1.flatten() - std_MS1.flatten(), mean_MS1.flatten() + std_MS1.flatten(), color='red', alpha=0.2)
# ax1.set_ylabel('EEG Power Spectral Density (uV^2/Hz)')
# # ax1.set_title('Simulated EEG Power Spectral Density')
# ax1.legend()
# plt.xticks([])
# ax1.set_xlim(0, 40)
# ax1.yaxis.set_minor_locator(plt.NullLocator())  # Remove y-axis minor ticks
# ax1.spines['top'].set_visible(False)  # Hide the top spine
# ax1.spines['right'].set_visible(False)  # Hide the right spine
# ax1.grid(False)
# plt.xscale('log')

# ax2 = plt.axes([0.12, 0.1, 0.85, 0.2])
# ax2.plot(f_good, p_values)
# ax2.set_xlabel('Frequency (Hz)')
# ax2.set_ylabel('t-test p')
# plt.yticks([0.00, 0.05, 0.10])
# ax2.set_ylim(0, 0.1)
# ax2.axhline(y=0.05, color='k', linestyle='--')
# ax2.invert_yaxis()
# ax2.grid(False)
# ax2.spines['top'].set_visible(False)  # Hide the top spine
# ax2.spines['right'].set_visible(False)  # Hide the right spine
#
# plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.1)
# fig.tight_layout(pad=3.0)

plt.show()

