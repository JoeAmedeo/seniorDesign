from tqdm import tqdm
import glob
import sys
import json
import gc
import pdb
from sqlalchemy import create_engine, MetaData, Table, exc
from sqlalchemy.exc import IntegrityError
import os
import contextlib
from collections import Counter
engine = create_engine('mysql+mysqlconnector://root:jordan@localhost:3306/stormTest', echo=False)
connection = engine.connect()
meta = MetaData()
meta.bind = engine
import re
"""
this will be used to capture between commas in the  lines. Sometimes we can have commas within quotes.

How do we handle single quotes? Especially since they're often used as part of regular grammar (like I just did there!)
"""
lineRegex = '([^,\"]*(?:\"[^\"]*\")*[^,\"]*),{0,1}'
lineRE = re.compile(lineRegex)

class DummyTqdmFile(object):
    """Dummy file-like that will write to tqdm"""
    file = None
    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)

@contextlib.contextmanager
def stdout_redirect_to_tqdm():
    save_stdout = sys.stdout
    try:
        sys.stdout = DummyTqdmFile(sys.stdout)
        yield save_stdout
    # Relay exceptions
    except Exception as exc:
        raise exc
    # Always restore sys.stdout if necessary
    finally:
        sys.stdout = save_stdout



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
        #make sure all of the rows have the same length. Kick out any ones that don't, but let the user know.
        lengths = list(map(len, self.rows))
        if len(lengths) > 1:
            """Sometimes we get rows of length 0 or 1, etc. They're probably anomylies due to the parsing. Let's ignore those.
            If we get rows being ignored that are length 20 (for example), then something has seriously done wrong """
            lengthDistribution = calculateDistribution(lengths)
            strongestLength = lengthDistribution[-1][0]
            for x in lengthDistribution[0:-2]:
                print('had to kick out rows of length ' + str(x[0]))                
            self.rows = filter(lambda x: len(x) == strongestLength, self.rows)

        return self.rows


def calculateDistribution(values):
    c = Counter(values)
    valuesLength = len(values)
    items = c.items()
    sortedItems = sorted(items, key=lambda x: x[1])
    distribution = list(map(lambda x: (x[0], (100.0*x[1]/valuesLength)), sortedItems))
    return distribution

def dictionariesDifferent(dictionary_one, dictionary_two, fieldsToCheck):
    for field in fieldsToCheck:
        if dictionary_one[field] != dictionary_two[field]:
            return False
    return True

def putInTable(tableName, columnMappings, csvFileSet, globalsTemp, primaryKey = False):
    with stdout_redirect_to_tqdm() as save_stdout:
        rows = list(csvFileSet.getRows())


        headers = csvFileSet.getHeaders()


        #rowDicts will be a list of dictionaries that map the table field to the value that should go into it 
        rowDicts = list()
        #connect to the table.
        table = Table(tableName, meta, autoload=True, autoload_with=engine)
        i = 0
        primaryKeysLookedAt = set()
        fieldsToCheck = list()
        processRow = True
        for x in columnMappings:
            fieldsToCheck.extend(x[0:-1])
        keys = set()
        for row in tqdm(rows, file=save_stdout, dynamic_ncols = True):
            i += 1
            processRow = True
             #convert from a list of headers, and a list of column values to a dictionary mapping the header to the column
            rowMapping = dict(zip(headers, row))
            rowDict = dict()
            doIt = True
            pk = -1
            primary_key_not_null = False
            if primaryKey:
                try:
                    if len(rowMapping[primaryKey].strip()) > 0:
                        pk = int(rowMapping[primaryKey].strip())
                        primary_key_not_null = True
                        if pk in primaryKeysLookedAt:
                            doIt = False
                    else:
                        doIt = False

                except ValueError:
                    print("couldn't get the primary key. Here's the row:")
                    print(str(rowMapping).encode('ascii', 'ignore'))
                    print(str(row).encode('ascii', 'ignore'))
                    pdb.set_trace()
                    sys.exit()

            if doIt:
                if primaryKey and primary_key_not_null:
                    primaryKeysLookedAt.add(pk)
                for columnMap in columnMappings:
                    """columnMap is a list of one of two forms:
                [csvColumnName, tableColumnName]
                OR

                ['csvColumnName1',...,'lambda ...: do something', 'tableColumnName']
                the lambda statement is evaluated within the context of the globalsTemp and 
                localTemps dictionaries (see right after opening of specs file)
                """
                    if len(columnMap) == 2:
                        if columnMap[0] in rowMapping.keys() and len(rowMapping[columnMap[0]]) > 0:
                            rowDict[columnMap[1]] = rowMapping[columnMap[0]]
                    elif len(columnMap) > 2:
                        tableFieldName = columnMap[-1]

                        expression = eval(columnMap[-2], globalsTemp)
                        csvFieldNames = columnMap[0:-2]
                        #Do all of the fields needed to calculate the answer exist?
                        allFieldsExist = True
                        for fieldName in csvFieldNames:
                            if fieldName not in rowMapping.keys():
                                allFieldsExist = False
                                break
                            elif len(rowMapping[fieldName]) == 0:
                                allFieldsExist = False
                                break
                        if allFieldsExist:
                            csvFieldValues = list(map(lambda x: rowMapping[x], csvFieldNames))
                            rowDict[tableFieldName] = expression(*csvFieldValues)
                            
                    else:
                        print("ERROR!")
                        sys.exit()
                if i % 1000 == 0 or not (set(rowDict.keys()).issubset(keys) and set(rowDict.keys()).issuperset(keys)):
                    try:
                        connection.execute(table.insert(), rowDicts)
                    except IntegrityError:
                        for x in rowDicts:
                            try:
                                connection.execute(table.insert(), [x])
                            except IntegrityError as err:
                                print(str(err).encode('ascii', 'ignore'))
                    del rowDicts
                    rowDicts = list()
                    keys = set(rowDict.keys())
                
                rowDicts.append(rowDict)
                    

 
def getFileNames(fileRE):
    files = list(filter(lambda x: os.path.isfile(x), os.listdir('.')))
    filesMatchingRE = list(filter(lambda x: re.fullmatch(fileRE, x) != None, files))
    return filesMatchingRE

    
if len(sys.argv) != 2:
    print('usage: python import_files.py specification.json')
else:
    specsFile = sys.argv[1]
    mapCSVFilesToData = dict()
    with open(specsFile, 'r') as f:
        print('specsFile: ' + specsFile)
        jsonCode = f.read()
        specs = json.loads(jsonCode)
        """ First, we may need to execute a python script to set up an environment to run certain needed statements in."""
        globalsTemp = dict()
        if 'pythonEnv' in specs:
            with open(specs['pythonEnv'], 'r') as s:
                fileText = s.read()
                exec(fileText, globalsTemp) 
                #now we have the execution environment set up
        """This for loop simply grabs the data from the CSV files, so we can process it later"""
        items = specs['csvMaps'].items()
        itemsSorted = sorted(items, key = lambda x: x[1]['order'])

        for fileRE, tablesDict in itemsSorted:
            headerCategories = []
            del tablesDict['order']
            tableOrder = False
            if 'tableOrder' in tablesDict.keys():
                print('tableOrder!')
                tableOrder = tablesDict['tableOrder']
                del tablesDict['tableOrder']
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
                            rowSet.addRow(chunks)
                                    
            
            tables  = tablesDict.keys()
            if tableOrder:
                print('table order is true!')
                tables = tableOrder
            for tableName in tables:
                columnMappings = tablesDict[tableName]
                print('tablename: ' + tableName)
                if isinstance(columnMappings, list):
                    putInTable(tableName, columnMappings, rowSet, globalsTemp)
                else:
                    putInTable(tableName, columnMappings['fields'], rowSet, globalsTemp, columnMappings['primaryKey'])
            del rowSet
            gc.collect()
"""        for fileRE, tablesDict in specs['csvMaps'].items():
            for tableName, columnMappings in tablesDict.items():
                columnMappings maps a column of a CSV file to a column in the DB table, or it maps 1 or more 
                CSV columns to a lambda function, which is executed using the values of the CSV column(s) as arguments,
                and this output is then mapped to a table column
                print('going to put in table')
                putInTable(tableName, columnMappings, mapCSVFilesToData[fileRE], globalsTemp)"""
                
connection.close()
