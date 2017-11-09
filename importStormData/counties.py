from collections import Counter
from tqdm import tqdm
from sqlalchemy import create_engine, MetaData, Table, exc
import sys
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
engine = create_engine('mysql+mysqlconnector://atr1@localhost:3306/stormTest', echo=False)
connection = engine.connect()                                                                                                                
meta = MetaData()                                                                                                                                  
meta.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

table = Table('event_details', meta, autoload=True, autoload_with=engine)
state_zone_type_combos = dict()

num_rows = session.query(table).count()
print('num rows: ' + str(num_rows))
count = 0
with tqdm(total=num_rows) as pbar:
    for row in session.query(table):
        state = row.state
        area_type = row.cz_type
        area_name = row.cz_name
        if state is None or area_type is None or area_name is None:
            tqdm.write('state, type or area is None: ' + str(row))
        else:
            state = state.strip('"')
            area_type = area_type.strip('"')
            area_name = area_name.strip('"')
            if area_type not in ['Z', 'M', 'C']:
                tqdm.write('area type not recognized')
                tqdm.write(str(area_type))
                tqdm.write(str(row))
                sys.exit()
                area_name = row.cz_name.strip('"')
            if state not in state_zone_type_combos:
                state_zone_type_combos[state] = {}
                state_zone_type_combos[state]['Z'] = list()
                state_zone_type_combos[state]['C'] = list()
                state_zone_type_combos[state]['M'] = list()
            if area_name not in state_zone_type_combos[state][area_type]:
                state_zone_type_combos[state][area_type].append(area_name)

        pbar.update(1)


    json_info_string = json.dumps(state_zone_type_combos)
    with open('counties.json', 'w') as f:
        f.write(json_info_string)
