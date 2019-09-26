import csv
from pprint import pprint
kampagne_file ="tdk_Kampagne.csv"
with open(kampagne_file,encoding='utf-8') as csvfile:
    for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
        str = line[1]
        str = str.split('.')
        if len(str) != 3:
            raise ValueError
        str = str[2] + "-" + str[1] + "-" + str[0]
        line[1] = str
        str = line[2]
        str = str.split('.')
        if len(str) != 3:
            raise ValueError
        str = str[2] + "-" + str[1] + "-" + str[0]
        line[2] = str
        for i in range(len(line)):

            if line[i].find("/") != -1:
                line[i] = line[i].split("/")
        pprint(line)

