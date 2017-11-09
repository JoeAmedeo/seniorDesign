"""
Here's what this script does:

It goes through all of the headers in the files, and outputs those for which all values are empty.
"""
import random
import glob
from collections import Counter
import sys
import json
import os
import re
"""
this will be used to capture between commas in the  lines. Sometimes we can have commas within quotes.

How do we handle single quotes? Especially since they're often used as part of regular grammar (like I just did there!)
"""
lineRegex = '([^,\"]*(?:\"[^\"]*\")*[^,\"]*),{0,1}'
lineRE = re.compile(lineRegex)

fileREDict = {"details":"StormEvents_details-ftp.*\.csv", "fatalities":"StormEvents_fatalities-ftp.*\.csv", "locations":"StormEvents_locations-ftp.*\.csv", "areas":"ugc_areas.csv"}



class CSVFileSet:
    def __init__(self):
        self.headers = []
        self.rows = []
    def setHeaders(self, headers):
        self.headers = headers
    def getHeaders(self):
        return self.headers
    def addRow(self, row):
        self.rows.append(row)
    def getRows(self):
        return self.rows
    def getFieldValues(self, columnName):
        print(self.headers)
        columnIndex = self.headers.index(columnName)
        values = list(map(lambda x: x[columnIndex].strip(), self.rows))
        return values

def calculateDistribution( values):
    c = Counter(values)
    valuesLength = len(values)
    items = c.items()
    sortedItems = sorted(items, key=lambda x, y: y)
    distribution = list(map(lambda value,count: (value, (100.0*count/valuesLength)), sortedItems))
    return distribution
        

    
def getFileNames(fileRE):
    files = list(filter(lambda x: os.path.isfile(x), os.listdir('.')))
    filesMatchingRE = list(filter(lambda x: re.fullmatch(fileRE, x) != None, files))
    return filesMatchingRE

    
if len(sys.argv) != 3:
    print('usage: python show_empty_fields.py')

else:
    for fileRE in fileREDict.values():
        mapCSVFilesToData = dict()
        print('fileRE: ' + fileRE)
        
        headerCategories = []
        rowSet = CSVFileSet()            
        for filename in getFileNames(fileRE):
            print('filename: ' + filename)
            with open(filename, 'r', encoding='windows-1252') as csvFile:
                lines = csvFile.read().split('\n')
                header = lines[0]
                fileHeaderCategories = list(map(lambda x: x.strip(), lineRE.findall(header)))
                if len(headerCategories) == 0:
                    headerCategories = fileHeaderCategories
                    rowSet.setHeaders(headerCategories)
                    if len(fileHeaderCategories) != len(headerCategories):
                        print('ERROR! header length different in file: ' + filename)
                        sys.exit()
                    else:
                        for i in range(0, len(fileHeaderCategories)):
                            if headerCategories[i] != fileHeaderCategories[i]:
                                print('ERROR! Headers different in file: ' + filename + ' header index: ' + str(i))
                                sys.exit()
                                #we've checked that the categories have not changed, so let's add the rows.
                        for line in lines[1::]:
                            #we need to chunk up the line in the CSV file
                            chunks = list(map(lambda x: x.strip(), lineRE.findall(line)))
                            if len(chunks) > 0:
                                rowSet.addRow(chunks)
        for header in headerCategories:
            values = rowSet.getFieldValues(header)
            if all(len(item) == 0 for item in values):
                print('column is empty: ' + header)
