import re
import sys
import datetime
import pdb
monthAbrevToNumber = {'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}
def convertDateTime(csv_datetime):
    dateTimeRegex = '(?P<day>\d+)-(?P<month>[a-zA-Z]+)-(?P<year>\d+)\s+(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)'
  #  print('csv datetime: ' + csv_datetime)
   # print('re')
   # print(re)
   # pdb.set_trace()
    dateTimeRegexResult = re.search(dateTimeRegex, csv_datetime)
#    print('datetime regex:')
 #   print(dateTimeRegexResult)
 #   print('globals')
 #   print(globals())
 #   print('locals')
 #   print(locals())

#    sys.stdout.flush()
    year = int(dateTimeRegexResult.group('year'))
#    print('year')
#    print(year)
#    sys.stdout.flush()
    
    if year < 51:
        year += 2000
    else:
        year += 1900
    dateTime = datetime.datetime(year, monthAbrevToNumber[dateTimeRegexResult.group('month')], int(dateTimeRegexResult.group('day')), int(dateTimeRegexResult.group('hour')), int(dateTimeRegexResult.group('minute')), int(dateTimeRegexResult.group('second')))
    return dateTime.isoformat(' ')
    
def convertFatalityDateTime(csv_fatality_datetime):
    print('csv fatality datetime: ' + csv_fatality_datetime)
    dateTimeRegex = '(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)\s+(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)'
    dateTimeRegex = re.search(dateTimeRegex, csv_fatality_datetime)
    if dateTimeRegex is None:
        return ''
    print('datetime regex: ')
    print(dateTimeRegex)
 #   sys.stdout.flush()
    dateTime = datetime.datetime(int(dateTimeRegex.group('year')), int(dateTimeRegex.group('month')), int(dateTimeRegex.group('day')), int(dateTimeRegex.group('hour')), int(dateTimeRegex.group('minute')), int(dateTimeRegex.group('second')))
    return dateTime.isoformat(' ')

def convertDamage(damage):
    regex = re.compile('\"(?P<thousand>\d*\.?\d*)(?=K)|(?P<million>\d*\.?\d*)(?=M)|(?P<billion>\d*\.?\d*)(?=B)|(?P<dollar>\d*\.?\d*)(?=$)\"')
    damage_match = regex.match(damage)
    if damage_match is not None:
        if damage_match.group('dollar'):
            return float(damage_match.group('dollar'))
        elif damage_match.group('thousand'):
            return float(damage_match.group('thousand'))*1000
        elif damage_match.group('million'):
            return float(damage_match.group('million'))*1000000
        elif damage_match.group('billion'):
            return float(damage_match.group('billion'))*1000000000
        else:
            return 0.0
    else:
        return 0.0
        
        
