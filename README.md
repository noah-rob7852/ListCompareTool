# ListCompareTool
Compare CSV/TXT files and output matches, missing values from file 1, and missing values from file 2


USAGE:
"python ListCompare.py -f1 testfile.csv -f1c Email -f2 testfile2.csv -f2c User principal name"


-f1 - Name of the first file.

-f2 - Name of the second file.

-f1c - Column(s) to use from file one if file one is a csv file

-f2c - Column(s) to use from file two if file two is a csv file

-em - Exclude matches. Yes/True for exclusion, No/False/dont use argument for including

-enm - Exclude non-matches. Yes/True for exclusion, No/False/dont use argument for including

-on - Output name. String name for text file


If you want to use more than one column from a csv (not as tested, but theoretically should still work), type the column
names after the argument with commas (no spaces) separating the column names.

Script will write the common entries and missing entries to an output.txt file
