from PIL import Image
import pytesseract
import re
import pandas as pd
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open the image file
img_path = r'E:\zyhGraduation\data\INTRA\gpt\image.png'
img = Image.open(img_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(img, lang='eng')

# Since we're interested in the numbers only, let's extract them
# The pattern looks for groups of digits possibly surrounded by spaces, commas or dots, and ± signs
numbers = re.findall(r'[\d\s]+[,\.]\d+|\d+\s?±\s?\d+', text)

# Replace commas with dots in the numbers
cleaned_numbers = [num.replace(',', '.') for num in numbers]
# cleaned_numbers

# Due to OCR misinterpretation, some numbers are concatenated incorrectly.
# They need to be split or corrected manually.
corrected_numbers = cleaned_numbers
# Manually correcting the numbers based on typical OCR errors observed
# corrected_numbers = [
#     '1.80', '0.36', '1.09', '2.52', '2.06', '0.25', '1.57', '2.55', '0.35', '0.554',
#     '1.38', '0.08', '1.23', '1.54', '1.44', '0.05', '1.34', '1.54', '0.33', '0.565',
#     '2.41', '0.36', '1.70', '3.13', '1.65', '0.24', '1.17', '2.13', '3.04', '0.084',
#     '1.23', '0.08', '1.08', '1.38', '1.20', '0.05', '1.10', '1.30', '0.08', '0.780',
#     '1.77', '0.36', '1.05', '2.48', '1.30', '0.25', '0.80', '1.79', '1.15', '0.285',
#     '0.92', '0.08', '0.77', '1.07', '0.95', '0.05', '0.84', '1.05', '0.07', '0.790',
#     '1.73', '0.36', '1.02', '2.45', '1.93', '0.24', '1.45', '2.41', '0.20', '0.654',
#     '1.34', '0.08', '1.19', '1.49', '1.39', '0.05', '1.28', '1.49', '0.21', '0.647'
# ]

# Now we will create a DataFrame to organize these numbers into the structure that reflects their original table format.
# Assuming the table has a structure similar to:
# Value ± Error | Lower CI - Upper CI | Value ± Error | Lower CI - Upper CI | ...

# Splitting the numbers into rows of the table, each row has 10 items (5 sets of Value ± Error and Lower CI - Upper CI)
rows = [corrected_numbers[i:i+10] for i in range(0, len(corrected_numbers), 10)]

# Create a DataFrame
df_table = pd.DataFrame(rows)

# Define the column names based on the structure of the table
columns = [
    'Value ± Error (1)', 'Lower CI - Upper CI (1)',
    'Value ± Error (2)', 'Lower CI - Upper CI (2)',
    'Value ± Error (3)', 'Lower CI - Upper CI (3)',
    'Value ± Error (4)', 'Lower CI - Upper CI (4)',
    'Value ± Error (5)', 'Lower CI - Upper CI (5)'
]

# Assign the column names to the DataFrame
df_table.columns = columns

# Save the DataFrame to an Excel file
excel_output_path = r'E:\zyhGraduation\data\INTRA\gpt\1.xlsx'
df_table.to_excel(excel_output_path, index=False)

# excel_output_path
