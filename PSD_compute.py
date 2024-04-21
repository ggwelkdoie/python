import mne
import numpy as np
from scipy.signal import welch
import matplotlib.pyplot as plt

# 路径替换为你的EDF文件的路径
file_path = r'E:\zyhGraduation\data\EEGdata\edfs\CLA003_all.edf'
num_channels = 30
# 读取EDF文件
raw = mne.io.read_raw_edf(file_path, preload=True)
raw.pick_types(eeg=True)  # 确保只选择EEG通道

# 获取数据
data, times = raw[:]

# 选择一个EEG通道进行分析，这里我们以第一个EEG通道为例
all_psd = np.zeros((num_channels, 513))
for i in range(num_channels):
    eeg_channel = data[i]
    frequencies, power_spectral_density = welch(eeg_channel, fs=raw.info['sfreq'], nperseg=1024)
    all_psd[i] = power_spectral_density
# eeg_channel = data[0]  # 假设第一个通道是EEG数据
#
# # 计算功率谱密度
# frequencies, power_spectral_density = welch(eeg_channel, fs=raw.info['sfreq'], nperseg=1024)
average_psd = np.mean(all_psd, axis=0)
# 绘制功率谱密度
plt.figure(figsize=(10, 5))
plt.semilogy(frequencies, average_psd)
plt.title('Power Spectral Density of EEG')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power/Frequency [uV^2/Hz]')
plt.xlim(0, 40)
plt.show()
