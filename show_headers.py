
import glob
headers = list()
for filename in glob.glob('*.csv'):
    print(filename)
    with open(filename, 'r', encoding='windows-1252') as f:
        text = f.read()
        lines = text.split('\n')
        header = lines[0]
        headers.append(header)

headerSet = set(headers)
for header in list(headerSet):
    print(header)
    
