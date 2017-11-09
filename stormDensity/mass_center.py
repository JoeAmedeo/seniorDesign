"""

I'm just trying different things to see what works. I think using the Haversine distance and initial bearing actually works quite well, and makes more sense than the rhumb lines. 

I'm suprised that using numerical root solving works so well. Next, I'm going to compute the Jacobian (probably using Mathematica, or an online reference) to make this even better.

"""

import math
import itertools
import functools
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize
def deltaPsi(point_one, point_two):
    print('point one: ' + str(point_one))
    print('point two: ' + str(point_two))
    numerator = math.tan(math.pi/4 + point_two[0]/2)
    print('numerator: ' + str(numerator))
    denom = math.tan(math.pi/4 + point_one[0]/2)
    print('denominator: ' + str(denom))
    d_psi =  math.log(numerator/denom)
    return d_psi

def rhumbDistance(point_one, point_two, R):
    d_psi = deltaPsi(point_one, point_two)
#    print('d psi: ' + str(d_psi))
    q = (point_two[0] - point_one[0])/d_psi if abs(d_psi) > 10e-12 else math.cos(point_one[0])
    return R*math.sqrt(math.pow(point_two[0] - point_one[0], 2) + math.pow(q, 2)*math.pow(point_two[1] - point_one[1], 2))

def rhumbBearing(point_one, point_two):
    return (point_two[1] - point_one[1], deltaPsi(point_one, point_two))

"""
Return a vector, of the form (x, y)
"""
def bearing(point_one, point_two):
    y = math.sin(point_two[1] - point_one[1])*math.cos(point_two[0])
    x = math.cos(point_one[0])*math.sin(point_two[0]) - math.sin(point_one[0])*math.cos(point_two[0])*math.cos(point_two[1] - point_one[1])
    return (x, y)
#    return math.atan2(math.sin(point_two[1] - point_one[1])*math.cos(point_two[0]), math.cos(point_one[0])*math.sin(point_two[0]) - math.sin(point_one[0])*math.cos(point_two[0])*math.cos(point_two[1] - point_one[1]))


def haversine_distance(point_one, point_two, R):
    a = math.pow(math.sin((point_two[0] - point_one[0])/2.0), 2) + math.cos(point_one[0])*math.cos(point_two[0])*math.pow(math.sin((point_two[1] - point_one[1])/2), 2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R*c

#returns a tuple of the form (x, y) -> this is vector from point one to point two
def equirectangular(point_one, point_two, R):
    phi_m = (point_two[0] + point_one[0])/2.0
    x = (point_two[1] - point_one[1])*math.cos(phi_m)
    y = point_two[0] - point_one[0]
    print('x in equi: ' + str(x))
    print('y in equi: ' + str(y))
    d = R*math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    print('distance in equirectangular: ' + str(d))
    return (d*x, d*y)

"""
point is of the form (lat, lon, mass)
"""
def getVector(reference_point, point, R):
    x, y = equirectangular(reference_point, (point[0], point[1]), R)
    print('doing equirectangular: ')
    print('x: ' + str(x))
    print('y: ' + str(y))
    return (point[2]*x, point[2]*y)

"""
This uses the equirectangular approximation. 

Given a bunch of points, we calculate the vector from the reference point to each point. Then, we use the formula for center of mass.

Each point in points is of the form (latitude, longitude, mass). 
"""
def centerOfMass(points, reference_point, R):
    total_mass = sum(map(lambda x: x[2], points))
    vectors = list(map(lambda x: getVector(reference_point, x, R), points))
    com_vector = functools.reduce(lambda current, vector: (current[0] + vector[0], current[1] + vector[1]), vectors)
  #  print('com vector')
  #  print(com_vector)
    com_y = com_vector[1]/total_mass
    com_x = com_vector[0]/total_mass
 #   print('com y ' + str(com_y))
  #  print('com x ' + str(com_x))
    phi = com_y + reference_point[0]
    lamb = reference_point[1] + com_x/math.cos((phi + reference_point[0])/2)
    return (phi, lamb)


#calculates average mass at point using haversine
def averageMass(point, points):
    """
    For each point, we calculate the distance between that point and point. Then, we use the initial bearing to provide a vector from the point given
    in parameters, to the current point.
    """
    total = [0, 0]
    R = 6371.0
    for lat, lon, mass in points:
        distance = haversine_distance(point, (lat, lon), R)
        direction = bearing(point, (lat, lon))
#        distance = rhumbDistance(point, (lat, lon), R)
#        direction = rhumbBearing(point, (lat, lon))
        total[0] += mass*distance*direction[0]
        total[1] += mass*distance*direction[1]
    return np.array(total)

def rootCOM(points, R):
    avg_lat = np.mean(list(map(lambda x: x[0], points)))
    avg_lon = np.mean(list(map(lambda x: x[1], points)))
    sol = optimize.root(averageMass, args=(points), x0 = np.array([avg_lat, avg_lon]), method='hybr', jac=False)
    return sol

def samplePoints(points, R):
    max_lat = max(map(lambda x: x[0], points))
    min_lat = min(map(lambda x: x[0], points))
    max_lon =  max(map(lambda x: x[1], points))
    min_lon = min(map(lambda x: x[1], points))
    fig, (ax0, ax1) = plt.subplots(ncols=2)
    x_scores = list()
    y_scores = list()
    zeros = list()
    for lat in np.linspace(min_lat, max_lat, num = 200):
        for lon in np.linspace(min_lon, max_lon, num = 200):
            x_score, y_score = averageMass((lat, lon), points)
            x_scores.append(x_score)
            y_scores.append(y_score)
            if abs(x_score) < 10e-6 and abs(y_score) < 10e-6:
                zeros.append((x_score, y_score))
    num_bins = 100
    print('max x score: ' + str(max(x_scores)))
    print('min x score: ' + str(min(x_scores)))
    print('max y score: ' + str(max(y_scores)))
    print('min y score: ' + str(min(y_scores)))
    print('zeros: ')
    print(zeros)
    n0, bins0, patches0 = ax0.hist(x_scores, num_bins)
    ax0.set_title('x scores')
    n1, bins1, patches1 = ax1.hist(y_scores, num_bins)
    ax1.set_title('y scores')
    plt.show()

#points_degrees = [(44.136899, -70.362084, 10.0), (39.802394,  -90.791414, 50.0), (32.908264, -85.874078, 20.0), (36.219548, -77.857003, 75.0)]
#points_degrees = [( 40.629053, -79.528944, 10.0), ( 40.636062, -79.519204, 20.0), ( 40.623944, -79.491735, 25.0)]
#reference_point_degrees = ( 40.628496, -79.511296)
reference_point_degrees = (40.596183, -79.503784)
range_difference = 40.0
num_points = 10
min_mass = 5.0
max_mass = 50000.0
points_degrees = list()
for x in range(0, num_points):
    lat = np.random.triangular(reference_point_degrees[0] - range_difference, reference_point_degrees[0] + 5.0, reference_point_degrees[0] + range_difference)
    lon = np.random.triangular(reference_point_degrees[1] - range_difference, reference_point_degrees[1] + 7.0, reference_point_degrees[1] + range_difference)
    mass = np.random.uniform(min_mass, max_mass)
    points_degrees.append((lat, lon, mass))

#points_degrees = [(1.0, 1.0, 1.0), (181.0, 1.0, 1.0)]
points_radians = list(map(lambda x: (x[0]*math.pi/180, x[1]*math.pi/180, x[2]), points_degrees))
#print('points radians')
#print(points_radians)
reference_point_radians = (reference_point_degrees[0]*math.pi/180, reference_point_degrees[1]*math.pi/180)
radius = 6371.0
#lat, lon = centerOfMass(points_radians, reference_point_radians, radius)
root = rootCOM(points_radians, radius)
lat = root.x[0]
lon = root.x[1]
print('root')
print(root)
print('center of mass latitude: ' + str(lat))
print('center of mass longitude: ' + str(lon))

print('max latitude: ' + str(max(map(lambda x: x[0], points_radians))))
print('min latitude: ' + str(min(map(lambda x: x[0], points_radians))))
print('max longitude: ' + str(max(map(lambda x: x[1], points_radians))))
print('min longitude: ' + str(min(map(lambda x: x[1], points_radians))))
x_mass, y_mass = averageMass((lat, lon), points_radians)
print('x mass: ' + str(x_mass))
print('y mass: ' + str(y_mass))
samplePoints(points_radians, radius)

#(latitude, longitude)
"""
point_one = (1.930619261192, 0.030189344044)
point_two = (0.550447751439, 0.999845791203)


bx = math.cos(point_two[0])*math.cos(point_two[1] - point_one[1])
by = math.cos(point_two[0])*math.sin(point_two[1] - point_one[1])
phi_m = math.atan2(math.sin(point_one[0]) + math.sin(point_two[0]), math.sqrt(math.pow(math.cos(point_one[0]) + bx, 2) + math.pow(by, 2)))

theta_m = point_one[1] + math.atan2(by, math.cos(point_one[0]) + bx)
print('phi: ' + str(phi_m*180/math.pi))
print('theta: ' + str(theta_m*180/math.pi))
print('bearing center to point 1: ' + str(bearing((phi_m, theta_m), point_one)*180/math.pi))
print('bearing center to point 2: ' + str(bearing((phi_m, theta_m), point_two)*180/math.pi))
"""
