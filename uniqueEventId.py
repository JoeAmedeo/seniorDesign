
import glob
headers = list()
eventIDs = list()
for filename in glob.glob('StormEvents_details*'):
    print(filename)
    with open(filename, 'r', encoding='windows-1252') as f:
        text = f.read()
        lines = text.split('\n')
        for line in lines[1::]:
            if len(line.split(',')) > 7:
                eventIDs.append(int(line.split(',')[7].strip()))


print('size of event ids list: ' + str(len(eventIDs)))
print('size of event ids set: ' + str(len(set(eventIDs))))

    
