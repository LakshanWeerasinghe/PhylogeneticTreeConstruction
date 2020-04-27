import csv
import os
import pandas as pd

# Output to CSV Conversion


def text_to_csv(DSK_Path, CSV_Path):
    outputFileList = os.listdir(DSK_Path)

    for outputFile in outputFileList:
        with open(DSK_Path + outputFile, 'r') as in_file:
            print(outputFile + " Started Conversion...")
            stripped = (line.strip() for line in in_file)
            lines = (line.split(" ") for line in stripped if line)
            with open(CSV_Path + outputFile + '.csv', 'w') as out_file:
                writer = csv.writer(out_file)
                writer.writerow(('Kmer', 'Count'))
                writer.writerows(lines)
        print(outputFile + " Ended Conversion...")
