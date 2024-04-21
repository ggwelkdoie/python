import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import windows, lfilter, butter

# 设置参数
fs = 256                  # 采样率
duration = 30             # 信号长度，单位：秒
t = np.arange(0, duration, 1/fs)

# 创建多频带基线噪声
def create_multiband_noise(fs, duration, bands):
    noise = np.zeros(fs*duration)
    time = np.arange(0, duration, 1/fs)
    for band, power in bands.items():
        noise += power * np.random.normal(0, 1, len(time)) * np.sin(2 * np.pi * np.mean(band) * time)
    return noise

# 定义一个Butterworth滤波器
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# 设置脑波频段的基础噪声功率
bands_power = {
    (1, 4): 0.5,    # Delta 波
    (4, 8): 0.3,    # Theta 波
    (8, 12): 0.2,   # Alpha 波
    (12, 30): 0.1,  # Beta 波
    (30, 45): 0.05  # Gamma 波
}

# 创建基线噪声
baseline_noise = create_multiband_noise(fs, duration, bands_power)

# 生成睡眠纺锤波
def create_spindle(frequency, duration, amplitude, fs):
    samples = int(duration * fs)
    time = np.arange(0, duration, 1/fs)
    spindle = amplitude * np.sin(2 * np.pi * frequency * time)
    window = windows.hann(samples)
    return spindle * window

# 插入纺锤波
number_of_spindles = 3
spindle_freq = 14
spindle_duration = 1.0
spindle_amplitude = 0.5  # 更接近真实脑电信号的幅度

eeg_signal = baseline_noise
for _ in range(number_of_spindles):
    start = np.random.randint(0, len(t) - int(spindle_duration * fs))
    while np.any(eeg_signal[start:start+int(spindle_duration * fs)] != baseline_noise[start:start+int(spindle_duration * fs)]):
        start = np.random.randint(0, len(t) - int(spindle_duration * fs))
    spindle = create_spindle(spindle_freq, spindle_duration, spindle_amplitude, fs)
    eeg_signal[start:start+len(spindle)] += spindle

# 应用滤波器模拟脑电信号的频带特性
eeg_signal = butter_bandpass_filter(eeg_signal, 0.5, 45, fs)

# 绘图展示模拟的EEG信号
plt.figure(figsize=(15, 5))
plt.plot(t, eeg_signal)
plt.title('Simulated EEG Signal with Sleep Spindles')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()
