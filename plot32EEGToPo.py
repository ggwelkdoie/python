import mne
import numpy as np
import matplotlib.pyplot as plt

# 创建一些模拟数据和通道信息
# data = np.random.randn(32, 1)
data = np.zeros((32,1))
ch_names = ['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9',
            'CP5', 'CP1', 'Pz', 'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8',
            'TP10', 'CP6', 'CP2', 'Cz', 'C4', 'T8', 'FT10', 'FC6', 'FC2', 'Fp2', 'F4', 'F8']
sfreq = 250  # 采样频率
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')

# 应用标准的10-20系统蒙太奇
montage = mne.channels.make_standard_montage('standard_1020')
info.set_montage(montage)

# 创建 RawArray 对象
raw = mne.io.RawArray(data, info)

# 绘制地形图，不显示默认的传感器标记
fig, ax = plt.subplots()
mne.viz.plot_topomap(data[:, 0], raw.info, axes=ax, show=False, sensors=False)

# 获取传感器位置
pos = mne.channels.layout._find_topomap_coords(info, picks=None)


# 绘制自定义的空心圆圈和通道名称
radius = 0.008  # 设置空心圆圈的半径
for i, (x, y) in enumerate(pos):
    ax.add_artist(plt.Circle((x, y), radius, color='black', fill=False))  # 空心圆圈
    ax.text(x, y, ch_names[i], ha='center', va='center', fontsize=8)  # 通道名称

ax.set_frame_on(False)
ax.axis('off')
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
# plt.subplots_adjust(top=1,bottom=0.059,left=0.061,right=0.833,hspace=0.1,wspace=0.2)
# plt.tight_layout()
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
# plt.show()
plt.savefig(r'E:\zyhGraduation\data\INTRA\topomap.svg', bbox_inches='tight')