import csv
# Let's start by reading the contents of the provided text file to understand its structure.
file_path = r'E:\zyhGraduation\data\EEGdata\CLA041_N2.txt'
file_path1 = r'E:\zyhGraduation\data\EEGdata\CLA041_N3.txt'
file_path2 = r'E:\zyhGraduation\data\EEGdata\CLA041_N2N3.txt'
file_path3 = r'E:\zyhGraduation\data\EEGdata\CLA041_REM.txt'
# Path for the output CSV file
output_csv_path = r'E:\zyhGraduation\data\EEGdata\psd\CLA041_N2.csv'
output_csv_path1 = r'E:\zyhGraduation\data\EEGdata\psd\CLA041_N3.csv'
output_csv_path2 = r'E:\zyhGraduation\data\EEGdata\psd\CLA041_N2N3.csv'
output_csv_path3 = r'E:\zyhGraduation\data\EEGdata\psd\CLA041_REM.csv'
# Reading the first few lines of the file to get a sense of its format and structure

# Function to convert the text file to a CSV file
def txt_to_csv(txt_file_path, csv_file_path):
    with open(txt_file_path, 'r') as txt_file, open(csv_file_path, 'w', newline='') as csv_file:
        # Creating a csv writer object
        csv_writer = csv.writer(csv_file)

        # Reading and writing each line from the txt file to the csv file
        for line in txt_file:
            # Splitting the line by tab character and writing to csv
            csv_writer.writerow(line.strip().split('\t'))





if __name__ == '__main__':
    txt_to_csv(file_path, output_csv_path)
    txt_to_csv(file_path1, output_csv_path1)
    txt_to_csv(file_path2, output_csv_path2)
    txt_to_csv(file_path3, output_csv_path3)

