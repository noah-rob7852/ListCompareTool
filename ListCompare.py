import os
import csv
import argparse

"""
USAGE:
"python ListCompare.py -f1 testfile.csv -f1c Email -f2 testfile2.csv -f2c User principal name"

-f1 - Name of the first file.
-f2 - Name of the second file.
-f1c - Column(s) to use from file one if file one is a csv file
-f2c - Column(s) to use from file two if file two is a csv file

If you want to use more than one column from a csv (not as tested, but theoretically should still work), type the column
names after the argument with commas (no spaces) separating the column names.

Script will write the common entries and missing entries to an output.txt file
"""


def read_file(input_file, csv_columns=None):
    get_path = input_file
    data = []
    if get_path.endswith(".csv"):
        with open(get_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            if csv_columns:
                columns = [column.strip() for column in csv_columns.split(',')]
                for row in reader:
                    extracted_data = {col: row[col] for col in columns if col in row}
                    data.append(extracted_data)
            else:
                for row in reader:
                    extracted_data = {col: row[col] for col in row}
                    data.append(extracted_data)
    elif get_path.endswith(".txt"):
        with open(input_file) as txt_file:
            reader = txt_file.readlines()
            data = [x.strip() for x in reader]
    else:
        print(f"The file is not a CSV or TXT file: {get_path}")
    return data


def compare(input_file_1, input_file_2):
    match_return_list = []
    no_match_return_list = []

    # Create a set of exact values from input_file_2 (case-insensitive)
    input_file_2_values = set()
    for item in input_file_2:
        if isinstance(item, dict):
            for value in item.values():
                input_file_2_values.add(value.lower())
        else:
            input_file_2_values.add(item.lower())

    for line in input_file_1:
        if isinstance(line, dict):
            for value in line.values():
                if value.lower() in input_file_2_values:
                    match_return_list.append(line)
                    break  # No need to check other values if one matches
                else:
                    no_match_return_list.append(line)
        else:
            if line.lower() in input_file_2_values:
                match_return_list.append(line)
            else:
                no_match_return_list.append(line)

    return match_return_list, no_match_return_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--fileone", help="First file to search")
    parser.add_argument("-f2", "--filetwo", help="Second file to search")
    parser.add_argument("-f1c", "--fileonecolumns", required=False, help="CSV Column header(s) for file one.")
    parser.add_argument("-f2c", "--filetwocolumns", required=False, help="CSV Column header(s) for file two.")

    args = parser.parse_args()

    file_one = read_file(args.fileone, args.fileonecolumns)
    file_two = read_file(args.filetwo, args.filetwocolumns)

    f1_matches, f1_no_matches = compare(file_one, file_two)
    f2_matches, f2_no_matches = compare(file_two, file_one)

    matches = f1_matches + f2_matches
    with open('output.txt', 'w') as output_file:
        output_file.writelines(f'{'-'*10}MATCHES: {'-'*10}\n')
        for line in matches:
            output_file.writelines(f'{line}\n')

        output_file.writelines(f'\n{'-'*10}END OF MATCHES{'-'*10}\n\n{'-'*10}START OF NOT MATCHED {args.filetwo}: {'-'*10}\n')
        for line in f1_no_matches:
            output_file.writelines(f'{line}\n')
        output_file.writelines(f'\n{'-'*10}END OF NOT MATCHED {args.filetwo}{'-'*10}\n')

        output_file.writelines(f'\n{'-'*10}START OF NOT MATCHED {args.fileone}: {'-'*10}\n')
        for line in f2_no_matches:
            output_file.writelines(f'{line}\n')
        output_file.writelines(f'{'-'*10}END OF NOT MATCHED {args.fileone}{'-'*10}')
