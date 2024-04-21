import numpy as np
import matplotlib.pyplot as plt
import mne
import matplotlib.font_manager as fm


# 定义通道的标签列表
channel_all = [
    'Fp1',    'Fz',    'F3',    'F7',    'FT9',    'FC5',    'FC1',    'C3',    'T7',    'CP5',    'CP1',    'Pz',    'P3',    'P7',    'O1',
    'Oz',    'O2',    'P4',    'P8',    'CP6',    'CP2',    'Cz',    'C4',    'T8',    'FT10',    'FC6',    'FC2',    'F4',    'F8',    'Fp2']
# 创建电极位置信息
montage = mne.channels.make_standard_montage('standard_1005')
info = mne.create_info(channel_all, 1000, ch_types='eeg')
info.set_montage(montage)
# 定义遮罩参数
mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='w', linewidth=0, markersize=4)


# ------------- 设置 data 和mask --------------------------------------------------
# np.random.seed(2023)
mean = -0.2
std = 1.2
data = np.random.normal(mean, std, size=30)  # 生成基础数据,所有通道
mask = np.zeros_like(data, dtype=bool)
# 要查找的区域的通道标签，预定义
target_PO = ['Oz','O1','O2','Pz','P3','P4','P7','P8']
target_CP = ['Cz','CP5','CP1','CP2','CP6','Pz','Oz']
target_FC = ['FP1','FP2','F3','F4','Fz','FC5','FC1','FC6','FC2']
"""
    · 某频带：Z-score 绝对PSD 数值范围 -1.8 ~ 1.8
    · 单通道内检验比较：t-values 数值范围 -6 ~ 6
"""
"""
                                    Fp1		FP2		
                                F7	F3	Fz	F4	F8	
                            FT9	FC5	FC1		FC2	FC6	FT10
                                T7	C3	Cz	C4	T8	
                                CP5	CP1		CP2	CP6	
                                P7	P3	Pz	P4	P8	
                                    O1	Oz	O2	

"""
#----------------------------------------------------------------------------------------
# cti = mne.pick_channels(channel_all, include=['Fp1', 'Fp2', 'FT9','FT10','F7','F8','FC5','FC6'])         # 选择电极下标
# data[cti] = data[cti] + np.random.normal(0.01, 0.01, size=len(cti))  #  正数值 多显著
# cti = mne.pick_channels(channel_all, include=['O1', 'Oz', 'O2'])  # 选择电极下标
# data[cti] =             np.random.normal(-1, 0.1, size=len(cti))   # 对部分电极 调整数据
#----------------------------------------------------------------------------------------
cti = mne.pick_channels(channel_all, include=['F3', 'Fz', 'F4', 'C3','Cz','C4'])  # 选择电极下标
data[cti] = data[cti] + np.random.normal(-0.1, 0.1, size=len(cti))   # 对部分电极 调整数据
#----------------------------------------------------------------------------------------
# cti = mne.pick_channels(channel_all, include=target_CP)  # 选择电极下标
# data[cti] =             np.random.normal(-0.5, 0.5, size=len(cti))   # 对部分电极 调整数据
#----------------------------------------------------------------------------------------
# 创建遮罩,随机遮罩: 在指定数组的数据中，不断随机选择数据，形成一个随机数组，并且指定每个数据被选择的概率
# mask = np.random.choice([True, False], size=data.shape, p=[0.5, 0.5])
# m_cti = mne.pick_channels(channel_all, include=['O1', 'Oz', 'O2'])         # 选择电极下标
# mask[m_cti] = True
mask[data > 4 ] = True

# 绘制地形图
"""
    ‘b’	蓝色 ‘g’	绿色 ‘r’	红色 ‘c’	青色
    ‘m’	品红色 ‘y’黄色 ‘k’黑色 ‘w’白色
"""
fig, ax = plt.subplots()
plot = mne.viz.plot_topomap(data, info,  sensors=True,
                            axes=ax, show=False, contours=6, image_interp='cubic',
                            mask=mask, mask_params=mask_params,
                            cmap='RdBu',
                            vlim=(-6, 6))
# Title
plt.title('Your Plot Title', fontsize=8, fontweight='bold', fontname='Arial')

# Remove white spaces
ax.set_frame_on(False)
ax.axis('off')
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
plt.subplots_adjust(top=0.941,bottom=0.059,left=0.061,right=0.833,hspace=0.2,wspace=0.2)

# Set font to Arial 8pt
prop = fm.FontProperties(fname='arial.ttf', size=8)
plt.setp(ax.get_xticklabels(), fontproperties=prop)
plt.setp(ax.get_yticklabels(), fontproperties=prop)

# Add color bar
cbar = plt.colorbar(plot[0], ax=ax)
cbar.ax.tick_params(labelsize=8)  # Change the font size (e.g., 8pt)
cbar.ax.set_aspect(4)
# Set the size of the figure
fig.set_size_inches(3.15, 3.15)  # 80mm = 3.15 inches
# 显示地形图
plt.show()
