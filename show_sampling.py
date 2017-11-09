"""
Here's what this script does:

Given the set of files to sample, and a column, it collects all values of that collumn.

If they are all empty, it says so. By empty, I mean there is no value to it (,, in CSV file), or the value is only whitespace.

If not, and there are 10 or fewer unique values in them, then in shows the percentage of each unique value.

If there are more than 10 unique fields, then it outputs a random sampling of 20 field values. It will also say how often the field is empty.
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
        print('columnIndex')
        print(columnIndex)
        lengths = list(map(len, self.rows))
        if len(lengths) > 1:
            """Sometimes we get rows of length 0 or 1, etc. They're probably anomylies due to the parsing. Let's ignore those.
            If we get rows being ignored that are length 20 (for example), then something has seriously done wrong """
            lengthDistribution = calculateDistribution(lengths)
            strongestLength = lengthDistribution[-1][0]
            for x in lengthDistribution[0:-2]:
                print('had to kick out rows of length ' + str(x[0]))                
            self.rows = filter(lambda x: len(x) == strongestLength, self.rows)
        values = list(map(lambda x: x[columnIndex].strip(), self.rows))
        return values

def calculateDistribution(values):
    c = Counter(values)
    valuesLength = len(values)
    items = c.items()
    print('items')
    print(items)
    sortedItems = sorted(items, key=lambda x: x[1])
    distribution = list(map(lambda x: (x[0], (100.0*x[1]/valuesLength)), sortedItems))
    return distribution
        

    
def getFileNames(fileRE):
    files = list(filter(lambda x: os.path.isfile(x), os.listdir('.')))
    filesMatchingRE = list(filter(lambda x: re.fullmatch(fileRE, x) != None, files))
    return filesMatchingRE

    
if len(sys.argv) != 4:
    print('usage: python show_sampling.py fileSetName columnName showAll')
    print('these are the mappings for the fileSetName:')
    for key,value in fileREDict.items():
        print(key + ': ' + value)
else:
    mapCSVFilesToData = dict()
    """This for loop simply grabs the data from the CSV files, so we can process it later"""
    fileSetName = sys.argv[1]
    fileRE = fileREDict[fileSetName]
    print('fileRE: ' + fileRE)
    columnName = sys.argv[2]
    showAll = int(sys.argv[3])
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
                    else:
                        print('chunks equals zero')

    values = rowSet.getFieldValues(columnName)
    if all(len(item) == 0 for item in values):
        print('After striping outer whitespace, all field values appear to be empty')
    else:            
        uniqueItems = set(values)
        if showAll:
            for x in values:
                print(x)
        else:
            if len(uniqueItems) <= 10:
                distribution = calculateDistribution(values)
                for value, percent in distribution:
                    print('value: ' + value + ' is present in this field: ' + str(percent) + ' % of the time')
            else:
                print('there are too many unique values, so we\'ll print a sampling of 10 (non empty) values')
                nonEmptyValues = set(filter(lambda x: len(x) > 0, uniqueItems))
                sample = random.sample(nonEmptyValues, 10)
                for x in sample:
                    print('value:')
                    print(x)
                    print('\n')
                
