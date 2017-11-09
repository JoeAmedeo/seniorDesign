import json, urllib


# Gets a JSON file from a url
def getData(url):
    response = urllib.urlopen(url)
    data = json.loads(response.read)
    return data

# Loads a json file specified by string path into memory
def json_load(path):
    f = open(path)
    data = json.load(f)
    return data

# Packages the data into a JSON file 'JSON/export_json.json'
def json_pack(data):
    f = open('JSON/export_json.json', 'w')
    json.dump(data, f)

# Packages up an object for the JSON file, specifying which columns
def build_rows(result, columns):
    list_of_rows = []
    for row in result:
        rowlist = []
        for column in columns:
            rowlist.append(getattr(row, column))
        list_of_rows.append(rowlist)
    result = {}
    result["columns"] = columns
    result["rows"] = list_of_rows
    return result

# Packages up an object for the JSON file, does not specify columns
def build_rows_count(result, columns):
    list_of_rows = []
    for row in result:
        obj = row[0]
        count = row[1]
        rowlist = []
        for column in columns:
            rowlist.append(getattr(obj, column))
        rowlist.append(count)
        list_of_rows.append(rowlist)
    result = {}
    result["columns"] = columns
    result["rows"] = list_of_rows
    return result

# Parse out the input file
def json_parse(data):
    return data['query']

# Pckage query result intro JSON format
def data_pack(result, debug = False):
    result_list = []
    
    #Extract column names
    row = result[0]
    column_list = []
    
    for table in row:
        for item in dir(table):
            if not (item.startswith('__') or item.startswith('_')):
                if not (item == 'episode' or item == 'fatalities1' or item == 'locations' or item == 'events' or item == 'event'):
                    column_list.append(item)

    column_set = list(set(column_list))
    result_list.append(column_set)

    #Extract data
    for row in result:
        row_list = []
        event = row[0]
        episode = row[1]
        fatality = row[2]
        location = row[3]

        for field in column_set:
            if hasField(event, field):
                row_list.append(getattr(event, field))
            elif hasField(episode, field):
                row_list.append(getattr(episode, field))
            elif hasField(fatality, field):
                row_list.append(getattr(fatality, field))
            elif hasField(location, field):
                row_list.append(getattr(location, field))
                
        result_list.append(row_list)
            
    #Debug code for finding duplicates
    if (debug == True):
        column = result_list[0]
        row = result_list[1]
        
        count1 = 0
        for item in column:
            count1 = count1 + 1
        print("There are ", count1, "column items")

        count2 = 0
        for item in row:
            count2 = count2 + 1
        print("There are ", count2, "row items")

        if count1 == count2:
            print("There are no duplicates")

            for index in range(0, len(column)):
                print(column[index], row[index])
                
    return result_list

#Helper function tests if field is in table
def hasField(table, field):
    for item in dir(table):
        if field == item:
            return True
    return False
