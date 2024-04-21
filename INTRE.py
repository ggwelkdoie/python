import pandas as pd
import re


def extract_numbers(file_path):
    # 读取文件中的每一行
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 处理每一行，提取数字
    processed_lines = []
    for line in lines:
        # 替换逗号为句号
        line = line.replace(',', '.')
        # 使用正则表达式提取所有数字
        numbers = re.findall(r'\d+\.\d+', line)
        processed_lines.append(numbers)

    # 将结果保存到DataFrame
    df = pd.DataFrame(processed_lines)

    # 保存到Excel文件
    output_file_path = r'E:\zyhGraduation\data\INTRA\gpt\INTRA_Data.xlsx'
    df.to_excel(output_file_path, index=False, header=False)

    return output_file_path

# 使用该函数
file_path = r'E:\zyhGraduation\data\INTRA\INTRA.txt'  # 将'your_file.txt'替换为您的文本文件路径
output_file_path = extract_numbers(file_path)
print(f"Processed data saved to {output_file_path}")
