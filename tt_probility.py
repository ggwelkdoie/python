# import numpy as np
# import mne
# from mne.stats import permutation_cluster_test
#
# # 假设的功率数据，形状为(subjects, electrodes)，这里以10个被试为例
# n_subjects_per_group = 10
# power_data_group1 = np.random.rand(n_subjects_per_group, 30)  # 组1
# power_data_group2 = np.random.rand(n_subjects_per_group, 30)  # 组2
#
# # 电极名称
# electrodes = ["Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FT9", "FC5", "FC1",
#               "FC2", "FC6", "FT10", "T7", "C3", "Cz", "C4", "T8", "CP5", "CP1",
#               "CP2", "CP6", "P7", "P3", "Pz", "P4", "P8", "O1", "Oz", "O2"]
#
# # 创建MNE Info对象，这对于确定电极的空间信息很重要
# info = mne.create_info(ch_names=electrodes, sfreq=100, ch_types="eeg")
# montage = mne.channels.make_standard_montage('standard_1020')
# info.set_montage(montage)
#
# # 数据合并，以及创建MNE EpochsArray对象
# data = np.concatenate([power_data_group1, power_data_group2], axis=0)
# events = np.array([[i, 0, 1] for i in range(n_subjects_per_group * 2)])
# epochs = mne.EpochsArray(data[:, :, np.newaxis], info, events)
#
# # 分组标签
# group_labels = np.array([0] * n_subjects_per_group + [1] * n_subjects_per_group)
#
# # 进行基于簇的统计检验
# stat_fun = mne.stats.permutation_cluster_test
# T_obs, clusters, cluster_p_values, H0 = stat_fun([data[group_labels == 0], data[group_labels == 1]],
#                                                   n_permutations=1000, tail=0, n_jobs=1,
#                                                   threshold=None, adjacency=None, out_type='mask')
#
# # 输出显著的簇
# for i_c, c in enumerate(clusters):
#     if cluster_p_values[i_c] <= 0.05:
#         print(f"Cluster {i_c} is significant, p-value: {cluster_p_values[i_c]:.4f}")
#
# # 注意: 这个代码是一个示例，它使用了随机生成的数据

import numpy as np
import mne
from mne.stats import permutation_cluster_test
from scipy.stats import ttest_ind

# 假设这些是你的功率数据，shape为(n_subjects, n_electrodes)
power_data_group1 = np.random.randn(10, 30)  # 用随机数据模拟第一组
power_data_group2 = np.random.randn(10, 30)  # 用随机数据模拟第二组

# 电极名单
electrodes_names = ["Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FT9", "FC5", "FC1", "FC2", "FC6", "FT10", "T7", "C3", "Cz", "C4", "T8", "CP5", "CP1", "CP2", "CP6", "P7", "P3", "Pz", "P4", "P8", "O1", "Oz", "O2"]

# 创建MNE Info对象，其中包含电极位置信息
info = mne.create_info(ch_names=electrodes_names, sfreq=1, ch_types="eeg")
# 使用标准10-20蒙太奇设置电极位置
montage = mne.channels.make_standard_montage("standard_1020")
info.set_montage(montage)

# 由于我们处理的是静态功率数据，不涉及时间序列，因此创建的Epochs数据结构时间点为1
n_subjects = power_data_group1.shape[0]
# 创建事件信息，这里事件信息不重要，只是为了符合创建Epochs对象的需求
events = np.array([[i, 0, 1] for i in range(n_subjects * 2)])
# 创建Epochs对象所需的数据维度为(subjects, channels, times)
# 因此我们需要添加一个时间维度
data = np.concatenate([power_data_group1[:, :, np.newaxis], power_data_group2[:, :, np.newaxis]], axis=0)
epochs = mne.EpochsArray(data, info, events)

# 进行基于簇的多重比较校正
# 这里我们创建一个简单的函数来模拟独立样本t检验的结果
# 注意：在实际应用中，你可能需要根据数据特性调整这部分
threshold = dict(start=0, step=0.2)  # 用于簇形成的阈值
# 这里的T-观察值是两个独立样本的平均值差异
T_obs, clusters, cluster_p_values, H0 = permutation_cluster_test([epochs[:n_subjects].get_data(), epochs[n_subjects:].get_data()],
                                                                 n_permutations=1000, threshold=threshold, tail=0, n_jobs=1, out_type='mask')

# 输出显著的簇
significant_clusters = np.where(cluster_p_values < 0.05)[0]
print("显著的簇索引:", significant_clusters)

