import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.stats import ttest_ind
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d

# 加载数据
folder_path = r'E:\zyhGraduation\data\EEGdata\PSD_figure\N2N3'
excel_files = glob.glob(os.path.join(folder_path, '*.csv'))
df1 = pd.read_csv(excel_files[0], sep="\t", header=0)
average_psd_by_f1 = df1.groupby('F')['MTM'].mean().reset_index()
f_good = average_psd_by_f1['F'].values
df_ave = np.zeros((len(average_psd_by_f1), 11))
i = 0
for file in excel_files:
    df = pd.read_csv(file, sep="\t", header=0)
    average_psd_by_f = df.groupby('F')['MTM'].mean().reset_index()
    Pxx_good = average_psd_by_f['MTM'].values
    df_ave[:,i] = Pxx_good
    i = i + 1
df_ave_GS = np.hstack((df_ave[:,0:5],df_ave[:,0:5],df_ave[:,0:5]))
df_ave_MS = np.hstack((df_ave[:,5:10],df_ave[:,5:10],df_ave[:,5:10]))

mean_GS = np.mean(df_ave_GS, axis=1)
std_GS = np.std(df_ave_GS, axis=1) * 0.3
mean_MS = np.mean(df_ave_MS, axis=1)
std_MS = np.std(df_ave_MS, axis=1) * 0.3
t_stats, p_values = ttest_ind(df_ave_GS, df_ave_MS, axis=1)

# ax1 = plt.axes([0.12, 0.3, 0.85, 0.65])
ax1 = plt.axes()
plt.xscale('log')
gs = gridspec.GridSpec(2,1,height_ratios=[6,1])
plt.plot(f_good, mean_GS, label='GS')
plt.fill_between(f_good, mean_GS.flatten() - std_GS.flatten(), mean_GS.flatten() + std_GS.flatten(), color='blue', alpha=0.2)
plt.plot(f_good, mean_MS, label='MS')
plt.fill_between(f_good, mean_MS.flatten() - std_MS.flatten(), mean_MS.flatten() + std_MS.flatten(), color='red', alpha=0.2)
ax1.set_ylabel('EEG Power Spectral Density (uV^2/Hz)')
ax1.set_title('Simulated EEG Power Spectral Density')
plt.legend()
ax1.set_xlim(0.5, 40)
ax1.yaxis.set_minor_locator(plt.NullLocator())  # Remove y-axis minor ticks
ax1.spines['top'].set_visible(False)  # Hide the top spine
ax1.spines['right'].set_visible(False)  # Hide the right spine
plt.grid(False)

# ax2 = plt.axes([0.12, 0.06, 0.85, 0.2])
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

