
from JSON.json_api import *
from Database.database_api import *

path = "newgraphquery.json"

data = json_load(path)
    
# engine = engine_start()

#data = json_parse(data)

query = create_graph_count(data, True)

#print(query)

#result = return_rows(query, 0, 2)

#print(result)

#result = data_pack(result)

#answer = data_pack(result)

#for index in range(0, len(answer[0])):
#    print(answer[0][index], answer[1][index])

#print(dir(answer[1][22]))

#print(answer[1][22].episode_id)

#for item in query:
#    event = item[1]
#    print(event.fatality_sex)

#if worked:
#    print("Join Success")
#else:
#    print("Did not work")
        

#result, columns = graph_query(engine, data)

#build_rows_count(result, columns)

#for item in result:
#    obj = item[0]
#    count = item[1]
#    print(obj.year, obj.event_type, count)


#result = build_rows(result, columns)

#result, columns = query_db2(engine, data)

#result = build_rows(result, columns)

#json_pack(result)

#for row in result:
#    for episode in row.episode_details:
#        print(episode)

#engine = engine_start()
#engine_connect(engine)

#result = query_db(engine, and_dict, or_dict)
#result = query_test(engine)

#print(result.episode_id)

#output = json_pack(data)
