import pandas as pd
import os

# 指定文件夹路径（请替换为您的文件夹路径）
folder_path = r'E:\zyhGraduation\data\PSDscope\OUTPUTSLOPE\REMSLOPE'

# 初始化一个空的列表来存储提取的数据
extracted_data = []

# 循环遍历文件名从YB001到YB040
for i in range(1, 41):
    # 生成文件名
    file_name = f'YB{str(i).zfill(3)}.xlsx'  # 将数字转换为三位数字符串，例如1变成001
    file_path = os.path.join(folder_path, file_name)

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 使用pandas读取特定单元格的值
        df = pd.read_excel(file_path, usecols=[2], header=None)  # 第三列的索引为2
        value = df.iloc[5][2]  # 第6行第3列的值（行和列的索引都是从0开始）
        extracted_data.append(value)  # 添加到列表中
    else:
        print(f'File {file_name} not found.')
        extracted_data.append('')  # 如果文件不存在，添加一个空字符串

# 将提取的数据转换为DataFrame
output_df = pd.DataFrame(extracted_data, columns=['Value'])

# 保存到新的Excel文件中
output_file_path = os.path.join(folder_path, 'REMSlope.xlsx')
output_df.to_excel(output_file_path, index=False)

print('Data extraction and file creation completed successfully.')
