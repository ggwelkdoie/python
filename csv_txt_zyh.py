def process_sleep_data_v2(csv_file_path, txt_file_path):
    """
    Processes the sleep data from a CSV file and writes it to a TXT file with updated logic.
    Each state with its start and end time is written in the TXT file.
    The start of a new state is the end of the previous state.

    :param csv_file_path: Path to the input CSV file.
    :param txt_file_path: Path to the output TXT file.
    """
    # State mappings
    state_mappings = {
        0: "Wake",
        1: "NonREM1",
        2: "NonREM2",
        3: "NonREM3",
        4: "REM"
    }

    try:
        with open(csv_file_path, 'r') as file:
            lines = file.readlines()

        # Initialize variables
        current_state = None
        start_time = 0
        output_lines = []

        # Process each line in the CSV file
        for i, line in enumerate(lines):
            state = int(line.strip())
            if state != current_state:
                # Record the previous state's end time and add to output
                if current_state is not None:
                    output_lines.append(f"{state_mappings[current_state]}\t{start_time * 30}\t{i * 30}")

                # Update current state and start time
                current_state = state
                start_time = i

        # Add the last state to the output
        output_lines.append(f"{state_mappings[current_state]}\t{start_time * 30}\t{len(lines) * 30}")

        # Write to TXT file
        with open(txt_file_path, 'w') as file:
            for line in output_lines:
                file.write(line + "\n")

        return "Data processing complete. Output written to " + txt_file_path

    except Exception as e:
        return f"An error occurred: {e}"


# Running the updated function with the uploaded CSV file
# txt_file_path_v2 = '/mnt/data/processed_sleep_data_v2.txt'
# process_result_v2 = process_sleep_data_v2(csv_file_path, txt_file_path_v2)
#
# # Output result
# process_result_v2, txt_file_path_v2
if __name__ == '__main__':
    csv_file_path = r'E:\zyhGraduation\data\EEGdata\edfs\CLA041_all.csv'
    txt_file_path = r'E:\zyhGraduation\data\EEGdata\edfs\CLA041_all.txt'
    process_sleep_data_v2(csv_file_path, txt_file_path)
