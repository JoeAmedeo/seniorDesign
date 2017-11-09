## This is the database API
## Contains functions relavent to the database

# Note(Guerra): import * is inefficient 
from sqlalchemy import *
from Database.orm import *
from sqlalchemy import *
from sqlalchemy.orm import *
import sys

## Engine:
# Creates and returns a new engine:
def engine_start():
    engine = create_engine('mysql+mysqlconnector://atr1@localhost:3306/stormTest', echo = False)
    return engine
    
# Connects to the engine:
def engine_connect(engine):
    engine.connect()

## Session:
# Starts and returns a session
def session_start(engine):
    Session = sessionmaker()
    session_bind(Session, engine)
    session = Session()
    return session

# Binds the engine to the session
def session_bind(session, engine):
    session.configure(bind = engine)

# Closes the session
def session_close(session):
    session.close()

    
#########################################################################
############################# General Query #############################
#########################################################################

# Query function
def query_db(engine, data):
    session = session_start(engine)
    select = data['select']
    where = data['where']
    query_dict = query_dictionary(session, where)
    for table in where:
        query_dict[table] = query_filter(query_dict[table], where[table])
    result = query_join(query_dict)
    print(result)
    return result.all(), select
        
# Return a dictionary of query objects, one for each table
def query_dictionary(session, data):
    query_dict = {}
    for table in data:
        orm_table = find_table(table)
        query = query_new(session, orm_table)
        query_dict[table] = query
    return query_dict

# Return a new query object
def query_new(session, table):
    query = session.query(table)
    return query

# Filter out query for a table
def query_filter(query, table_constraints):
    if table_constraints:
        for constraint_obj in table_constraints:
            constraint_list, flag = constraint_parse(constraint_obj)
            if flag:
                query = query_and(query, constraint_list)
            else:
                query = query_or(query, constraint_list)
    return query
        
# Parse out constraint
def constraint_parse(constraint_obj):
    field = constraint_obj['name'] # Name of the field
    flag = constraint_obj['flag'] # Flag of field ( 1 = AND, 0 = OR )
    constraint_obj_list = constraint_obj['list']
    constraint_list = []
    for index in range(len(constraint_obj_list)): # Iterate over items in the list of constraints
        value = constraint_obj_list[index]['value'] # Value of field
        con = constraint_obj_list[index]['constraint'] # Constraint of field
        constraint = field + con + value
        constraint_list.append(constraint)
    return constraint_list, flag

# Filters AND query
def query_and(query, constraint_list):
    constraint_list = constraint_combine(constraint_list)
    query = query.filter(*constraint_list)
    return query
    
# Filters OR query
def query_or(query, constraint_list):
    constraint_list = constraint_combine(constraint_list)
    query = query.filter(or_(*constraint_list))
    return query
    
# Return table name
def find_table(table):
    if table == "episode_details":
        return episode_details
    elif table == "event_details":
        return event_details
    elif table == "fatalities":
        return fatalities
    elif table == "location":
        return location
    else:
        return 0

# Return all results
def ret_all(query):
    return query.all()

# Return one result
def ret_one(query):
    return query.one()

def query_join(query_dict):
    query = query_dict['event_details']
    for table in query_dict:
        if table != "event_details":
            subquery = query_dict[table].subquery()
            query = query.join(subquery);
    return query


#######################################################################
############################# Graph Query #############################
#######################################################################


# Query API call for graph querying
def graph_query(engine, data):
    session = session_start(engine)
    sql_select = data['select']
    sql_where = data['where']
    sql_group_by = data['group_by']
    query_dict = graph_dictionary(session, sql_where)
    for table in query_dict:
        query_dict[table] = query_filter(query_dict[table], sql_where[table])
    result = graph_query_join(query_dict)
    result = query_group(result, sql_group_by)
    return result.all(), sql_select
    
## Temporary
def graph_query_join(query_dict):
    query = query_dict['event_details']
    for table in query_dict:
        if table != "event_details":
            subquery = query_dict[table].subquery()
            query = query.join(subquery);
    return query

# Creates a dicationary of columns
def graph_dictionary(session, sql_where):
    query_dict = {}
    for table in sql_where:
        orm_table = find_table(table)
        if table == "event_details":
            query = graph_query_new(session, orm_table)
        else:
            query = query_new(session, orm_table)
        query_dict[table] = query
    return query_dict

# Return a new query object
def graph_query_new(session, orm_table):
    query = session.query(orm_table, func.count())
    return query

# Groups the result query
def query_group(query, group_by):
    for column in group_by:
        query = query.group_by(column)
    #query = query.group_by(event_details.year)
    #query = query.group_by(event_details.event_type)
    return query

# Creates and returns a new count
def query_count(query):
    count = query.count()
    return count

# Return a dictionary of queries
def graph_query_dictionary(session, columns):
    query_dict = {}
    for table in columns:
        orm_table = find_table(table)
        query = graph_query_new(session, orm_table)
        query_dict[table] = query
    return query_dict


##############################################################
##############################################################
##############################################################

#Splits query into tables
def table_create(data):
    #List of table fields
    event_table = table_map(event_details())
    episode_table = table_map(episode_details())
    fatalities_table= table_map(fatalities())
    location_table = table_map(location())

    #Hold table constraints
    t0 = []                  #event_details
    t1 = []                  #episode_details
    t2 = []                  #fatalities
    t3 = []                  #location
    
    for item in data:
        if field_exists(item['name'], event_table):
            t0.append(item)
        elif field_exists(item['name'], episode_table):
            t1.append(item)
        elif field_exists(item['name'], fatalities_table):
            t2.append(item)
        elif field_exists(item['name'], location_table):
            t3.append(item)
        else:
            #Note: add error code
            print("Field not in database")
              
    #Hold a dictionary of the table constraints
    table_cons = {}
    table_cons['event_details'] = t0
    table_cons['episode_details'] = t1
    table_cons['fatalities'] = t2
    table_cons['location'] = t3

    #List of each parsed constraint
    c0 = []                       #event_details
    c1 = []                       #episode_details
    c2 = []                       #fatalities
    c3 = []                       #location
    
    for constraint in t0:
        c0.append(parse_constraint(constraint, event_details))

    for constraint in t1:
        c1.append(parse_constraint(constraint, episode_details))

    for constraint in t2:
        c2.append(parse_constraint(constraint, fatalities))

    for constraint in t3:
        c3.append(parse_constraint(constraint, locations))

    engine = engine_start()
    session = session_start(engine)

    #query = session.query(event_details)
    #query = apply_constraints(query, c0)

    #query2 = session.query(fatalities)
    #query2 = apply_constraints(query2, c2)
    #query2 = query2.subquery()
    
    #query = query.join(query2)
    
    #print(query)

    query = session.query(event_details, episode_details, fatalities, location).join(episode_details).join(fatalities).join(location)
    #query = session.query(event_details).join(episode_details).join(fatalities).join(location)
    #field = getattr(fatalities, 'fatality_sex')
    #stmt = text(str(field) + " ='\"M\"'")
    #query = query.filter(stmt)
    #query = query.filter(getattr(fatalities, 'fatality_sex') == '"M"')

    query = apply_constraints(query, c0)
    query = apply_constraints(query, c1)
    query = apply_constraints(query, c2)
    query = apply_constraints(query, c3)
    
    return query
            
#Creates a list of column names
def table_map(table):
    result = []
    for item in dir(table):
        if not (item.startswith('__') or item.startswith('_')):
            result.append(item)
    return result

#Determines whether a column exists in a given table
def field_exists(item, table):
    for field in table:
        if (item == field):
            return True
    return False

#Builds the constraint from a given table, returning a constraint
def parse_constraint(constraint, table):
    con_name = constraint['name']
    con_field = getattr(table, con_name)
    if 'params' in constraint:
        result = []
        for item in constraint['params']:
            con_type = item['type']
            con_value = check_type(item['value'])
            con = str(con_field) + con_type + con_value
            result.append(con)
    else:
        con_type = constraint['type']
        con_value = check_type(constraint['value'])
        result = str(con_field) + con_type + con_value
    return result

#Checks whether value is of type int, if it is returns a string
def check_type(value):
    if isinstance(value, int):
        return str(value)
    else:
        return value

#Filters the query based on the given list of constraints
def apply_constraints(query, constraints):
    for constraint in constraints:
        if isinstance(constraint, list):
            fixed_cons = constraint_combine(constraint)
            query = query.filter(or_(*fixed_cons))
        else:
            query = query.filter(text(constraint))
    return query

# Combines constraints in list into one constraint
def constraint_combine(constraint_list):
    result = []
    for index in range(len(constraint_list)):
        result.append(text(constraint_list[index]))
    return result

#Limits the number of rows returned
def return_rows(query, page, page_size):
    result = query.offset(page * page_size)
    result = result.limit(page_size)
    return result


############################################################
############################################################
############################################################



#Entry point of Graph querying
def create_graph_count(data, debug = False):
    #List of table fields
    event_table = table_map(event_details())
    episode_table = table_map(episode_details())
    fatalities_table= table_map(fatalities())
    location_table = table_map(location())

    columns = data['columns']
    data = data['query']
    
    #Hold table constraints
    t0 = []                  #event_details
    t1 = []                  #episode_details
    t2 = []                  #fatalities
    t3 = []                  #location

    for item in data:
        if field_exists(item['name'], event_table):
            t0.append(item)
        elif field_exists(item['name'], episode_table):
            t1.append(item)
        elif field_exists(item['name'], fatalities_table):
            t2.append(item)
        elif field_exists(item['name'], location_table):
            t3.append(item)
        else:
            #Note: add error code
            print("Field not in database")

    #List of each parsed constraint
    c0 = []                       #event_details
    c1 = []                       #episode_details
    c2 = []                       #fatalities
    c3 = []                       #location
    
    for constraint in t0:
        c0.append(parse_constraint(constraint, event_details))

    for constraint in t1:
        c1.append(parse_constraint(constraint, episode_details))

    for constraint in t2:
        c2.append(parse_constraint(constraint, fatalities))

    for constraint in t3:
        c3.append(parse_constraint(constraint, locations))

    if debug:
        print(c0)
        print(c1)
        print(c2)
        print(c3)

    #Querying the Database
    engine = engine_start()
    session = session_start(engine)

    query = session.query(func.count(), event_details, episode_details, fatalities, location).join(episode_details).join(fatalities).join(location)

    query = apply_constraints(query, c0)
    query = apply_constraints(query, c1)
    query = apply_constraints(query, c2)
    query = apply_constraints(query, c3)

    query = query_group(query, columns)
    
    if debug:
        print(query)
    
    return query
