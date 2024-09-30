import csv

with open('scalesplus/textfiles/output1.csv','r',newline='') as infile, open('scalesplus/textfiles/output not empty row.csv','w',newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        if any(field.strip() for field in row):
            writer.writerow(row)
