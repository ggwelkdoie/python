import pandas as pd
import os

# Set the directory where your CSV files are stored
directory = r'E:\zyhGraduation\data\PSDscope\OUTPUTSLOPE\REMSLOPE'

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.startswith('YB') and filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        # Read the CSV file
        data = pd.read_csv(file_path, delimiter='\t', header=None)

        # Calculate the average of the second to fifth rows of the third column
        average_value = data.iloc[1:5, 2].astype(float).mean()

        # Append the average value to the sixth row of the third column
        new_row = [None, None, average_value]
        data.loc[5] = new_row

        # Save the updated data to a new Excel file
        output_file_path = file_path.replace('.csv', '.xlsx')
        data.to_excel(output_file_path, index=False, header=False)

print('All files have been processed and saved as Excel files.')
