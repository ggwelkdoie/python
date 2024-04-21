# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import glob
# import os
# from scipy.stats import ttest_ind
# import matplotlib.gridspec as gridspec
# from matplotlib.ticker import NullLocator
#
# folder_path = r'E:\zyhGraduation\data\PSDscope\OUTPUT\N2csv'
# excel_files = glob.glob(os.path.join(folder_path, '*.csv'))

# import pandas as pd
# import os
#
# # 设置工作目录到包含CSV文件的文件夹
# folder_path = r'F:\WLwork\data\output\N3\N3_F'  # 替换为你的文件夹路径
# output_folder = r'F:\WLwork\data\output\N3\N3_F_excel'  # 输出Excel文件的文件夹路径，确保此文件夹存在
#
# # 检查并创建输出文件夹
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
#
# # 遍历文件夹中的所有CSV文件
# for filename in os.listdir(folder_path):
#     if filename.endswith('.csv'):
#         file_path = os.path.join(folder_path, filename)
#         # 读取CSV文件，假设数据在第一列，并且没有表头
#         df = pd.read_csv(file_path, header=None, sep='\t', engine='python')
#         # 将处理后的数据保存为Excel文件，文件名与CSV文件相同，扩展名为.xlsx
#         output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.xlsx")
#         df.to_excel(output_path, index=False, header=False)  # 不包含行索引和列标题
#
# print("所有文件处理完毕，保存在指定的输出文件夹。")

import pandas as pd
import os

# 设置工作目录到包含CSV文件的文件夹
folder_path = r'F:\WLwork\data\output\R\R_B'  # 替换为你的文件夹路径
output_folder = r'F:\WLwork\data\output\R\R_B_excel'  # 输出Excel文件的文件夹路径，确保此文件夹存在

# 检查并创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中的所有CSV文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        # 读取CSV文件，假设数据在第一列，并且没有表头
        try:
            df = pd.read_csv(file_path, header=None, sep='\t', engine='python')
        except pd.errors.EmptyDataError:
            df = pd.DataFrame()  # 创建一个空的DataFrame
        # 将处理后的数据保存为Excel文件，文件名与CSV文件相同，扩展名为.xlsx
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.xlsx")
        df.to_excel(output_path, index=False, header=False)  # 不包含行索引和列标题

print("所有文件处理完毕，保存在指定的输出文件夹。")

