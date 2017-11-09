import matplotlib
from sqlalchemy import *
from sqlalchemy.orm import *

import numpy as np
from shapely.geometry import Polygon as shapelyPolygon
from matplotlib.patches import Polygon as patchPolygon
from matplotlib.collections import PatchCollection
import compute
import math
import geopandas as gpd
import matplotlib.pyplot as plt
from Database.orm import *
def haversine(z):
    return math.pow(math.sin(z/2.0), 2.0)
def invHaversine(z):
    return 2*math.asin(math.sqrt(z))

def distance(lat_one, lon_one, lat_two, lon_two, radius):
    return radius*invHaversine(haversine(lat_one - lat_two) + math.cos(lat_one)*math.cos(lat_two)*haversine(lon_one - lon_two))


"""
This returns a list of tuples, of the form (latitude_top, latitude_middle, latitude_bottom)
"""
def sampleLatitudes(earths_radius, square_width, min_latitude, max_latitude):
    latitudes = []
    latitude_top = min_latitude + square_width/earths_radius
    latitude_middle = min_latitude + 0.5*square_width/earths_radius
    latitude_bottom = min_latitude
    i = 1
    #along a meridian, we can use the equirectangular approximation exactly
    while latitude_bottom <= max_latitude:
        latitudes.append((latitude_top, latitude_middle, latitude_bottom))
        i += 1
        latitude_bottom = min_latitude + (i - 1)*square_width/earths_radius
        latitude_middle = (i - 0.5)*square_width/earths_radius + min_latitude
        latitude_top = min_latitude + i*square_width/earths_radius
    return latitudes



def calculateLongitude(distance, latitude, min_longitude, earths_radius):
    return min_longitude + invHaversine(haversine(distance/earths_radius)/(math.pow(math.cos(latitude), 2.0)))
    
"""
Returns a list of lists. Each internal list is of the form: [latitude_top, latitude_middle, latitude_bottom, (longitude_left_top, longitude_left_bottom, longitude_right_top, longitude_right_bottom, longitude_middle)...]
"""
def sampleLongitudes(earths_radius, square_width, min_longitude, max_longitude, latitudes):
    longitudes = []
    for lat_top, lat_middle, lat_bottom in latitudes:
        keepGoing = True
        temp_longitudes = [math.degrees(lat_top), math.degrees(lat_middle), math.degrees(lat_bottom)]
        i = 0
        while keepGoing:
            lon_left_top = calculateLongitude(i*square_width, lat_top, min_longitude, earths_radius)
            lon_left_bottom = calculateLongitude(i*square_width, lat_bottom, min_longitude, earths_radius)
            lon_right_top = calculateLongitude((i + 1.0)*square_width, lat_top, min_longitude, earths_radius)
            lon_right_bottom = calculateLongitude((i + 1.0)*square_width, lat_bottom, min_longitude, earths_radius)
            lon_middle = calculateLongitude((i + 0.5)*square_width, lat_middle, min_longitude, earths_radius)
            true_distance = distance(lat_middle, min_longitude, lat_middle, lon_middle, earths_radius)
            percent_error = 100.0*abs((true_distance - (i + 0.5)*square_width)/((i + 0.5)*square_width))
            if percent_error > 1.0:
                print('There was percent error {0} \% with latitude: {1} and longitude: {2}, measured distance: {3}, theoretical distance: {4}'.format(percent_error, math.degrees(latitude), math.degrees(longitude), true_distance, d))
            if lon_left_bottom <= max_longitude or lon_left_top <= max_longitude:
                temp_longitudes.append((math.degrees(lon_left_top), math.degrees(lon_left_bottom), math.degrees(lon_right_top), math.degrees(lon_right_bottom), math.degrees(lon_middle)))
                i += 1
            else:
                keepGoing = False
        longitudes.append(temp_longitudes)
    return longitudes

def createSamplePoints(polygon, square_width, earths_radius):
    min_latitude = math.radians(polygon.bounds[1])
    max_latitude = math.radians(polygon.bounds[3])
    print('min latitude: {0}, max latitude: {1}'.format(math.degrees(min_latitude), math.degrees(max_latitude)))
    latitudes = sampleLatitudes(earths_radius, square_width, min_latitude, max_latitude)
    min_longitude = math.radians(polygon.bounds[0])
    max_longitude = math.radians(polygon.bounds[2])
    print('min longitude: {0}, max longitude: {1}'.format(math.degrees(min_longitude), math.degrees(max_longitude)))
    samples = sampleLongitudes(earths_radius, square_width, min_longitude, max_longitude, latitudes)
    return samples



"""
Give events in degrees, we'll convert them to radians later.
"""
def scoreMap(polygon, events, square_width):
    samples = createSamplePoints(polygon, square_width, 6371.0)
    points = []
    num_colors = 400
    radian_events = [(math.radians(lat), math.radians(lon), weight) for lat,lon,weight in events]
    for sample in samples:
        latitude = sample[1]
        for a, b, c, d, lon_middle in sample[3::]:
            points.append((math.radians(latitude),math.radians( lon_middle)))
    scores = compute.computeScores(radian_events, len(radian_events), points, len(points), num_colors)
    scores_list = compute.unsignedLongArray_frompointer(scores)
    patches = []
    i = 0
    colors = list()
    x,y = polygon.exterior.xy
    for sample in samples:
        lat_top = sample[0]
        lat_middle = sample[1]
        lat_bottom = sample[2]
        
        for lon_left_top, lon_left_bottom, lon_right_top, lon_right_bottom, lon_middle in sample[3::]:
            temp_polygon = [(lon_left_top, lat_top), (lon_right_top, lat_top), (lon_right_bottom, lat_bottom), (lon_left_bottom, lat_bottom)]
            sPoly = shapelyPolygon(temp_polygon)
            if polygon.contains(sPoly) or polygon.intersects(sPoly):
                patches.append(patchPolygon(temp_polygon, True))
                score = scores_list[i]
                colors.append(score*(100.0/num_colors))
            i+= 1
                
                
    patch_collection = PatchCollection(patches, cmap=matplotlib.cm.plasma, alpha=1.0)

    patch_collection.set_array(np.array(colors))
    figure, axis = plt.subplots()

    axis.add_collection(patch_collection)
    plt.plot(x, y)
    plt.show()

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
us = world[world.name == 'United States']
us_continental = list(sorted(us.geometry[168], reverse = True, key = lambda x: x.area))[0]

engine = create_engine('mysql+mysqlconnector://atr1@localhost:3306/stormTestTwo', echo=False)
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
results = session.query(event_details, location).filter(event_details.damage_property > 0).all()
events = list()
for x in results:
    e_details = x[0]
    location = x[1]
    if location.latitude != None and location.longitude != None and e_details.damage_property != None:
        events.append((location.latitude, location.longitude, e_details.damage_property))
print('number of events: {0}'.format(len(events)))
scoreMap(us_continental, events, 10.0)

"""
a = compute.computeScores([(1.0, 2.0, 100000)], 1, [(1.0, 1.99), (0.0, 0.0), (0.5, 1.3), (0.95, 1.9), (0.8, 2.5), (1.0, 2.0), (1.1, 2.5)], 7, 3)
b = compute.unsignedLongArray_frompointer(a)
print(b[0])
print(b[1])
"""
