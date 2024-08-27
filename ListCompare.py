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
-em - Exclude matches. Yes/True for exclusion, No/False/dont use argument for including
-enm - Exclude non-matches. Yes/True for exclusion, No/False/dont use argument for including
-on - Ouput name. String for name of text file

If you want to use more than one column from a csv (not as tested, but theoretically should still work), type the column
names after the argument with commas (no spaces) separating the column names.

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
                    break
                else:
                    no_match_return_list.append(line)
        else:
            if line.lower() in input_file_2_values:
                match_return_list.append(line)
            else:
                no_match_return_list.append(line)

    return match_return_list, no_match_return_list

def ensure_unique_values(input_list: list):
    seen_values = set()
    unique_data = []

    for item in input_list:
        value = list(item.values())[0]

        if value not in seen_values:
            seen_values.add(value)
            unique_data.append(item)

    print(unique_data)
    return unique_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", "--fileone", help="First file to search")
    parser.add_argument("-f2", "--filetwo", help="Second file to search")
    parser.add_argument("-f1c", "--fileonecolumns", required=False, help="CSV Column header(s) for file one.")
    parser.add_argument("-f2c", "--filetwocolumns", required=False, help="CSV Column header(s) for file two.")
    parser.add_argument("-em", "--excludematches", required=False, help="Exclude matches to Output file")
    parser.add_argument("-enm", "--excludenotmatched", required=False, help="Exclude non-matches to Output file")
    parser.add_argument("-on", "--outputname", required=False, help="Specify file name")


    args = parser.parse_args()

    file_one = read_file(args.fileone, args.fileonecolumns)
    file_two = read_file(args.filetwo, args.filetwocolumns)
    f1_matches, f1_no_matches = compare(file_one, file_two)
    f2_matches, f2_no_matches = compare(file_two, file_one)
    unmodified_matches = f1_matches + f2_matches
    matches = ensure_unique_values(unmodified_matches)

    if args.outputname:
        filename = args.outputname
    else:
        filename = 'output.txt'

    with open(filename, 'w') as output_file:

        if not args.excludematches or str(args.excludenotmatched).casefold() in ['no', 'false']:
            output_file.writelines(f'{'-'*10}MATCHES{'-'*10}\n')
            for line in matches:
                output_file.writelines(f'{line}\n')
            output_file.writelines(f'\n{'-'*10}END OF MATCHES{'-'*10}\n\n')

        if not args.excludenotmatched or str(args.excludenotmatched).casefold() in ['no', 'false']:
            output_file.writelines(f'{'-'*10}{args.fileone} MISSING FROM {args.filetwo}{'-'*10}\n')
            for line in f1_no_matches:
                output_file.writelines(f'{line}\n')
            output_file.writelines(f'\n{'-'*10}END OF {args.fileone} MISSING FROM {args.filetwo}{'-'*10}\n')

            output_file.writelines(f'\n{'-'*10}{args.filetwo} MISSING FROM {args.fileone}{'-'*10}\n')
            for line in f2_no_matches:
                output_file.writelines(f'{line}\n')
            output_file.writelines(f'{'-'*10}END OF {args.filetwo} MISSING FROM {args.fileone}{'-'*10}')
