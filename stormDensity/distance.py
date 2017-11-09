
import math

def mapDistance(radius, point_one, point_two):
    return radius*math.acos(math.sin(point_one[0])*math.sin(point_two[0]) + math.cos(point_one[0])*math.cos(point_two[0])*math.cos(point_two[1] - point_one[1]))

#this is just me trying out a few examples to make sure this actually works.
#radius is radius of sphere, left is (phi, lambda) lower left hand corner, right is (phi, lambda) LRH
#point is (phi, lambda)
def toCartesian(radius, left, right, point):
    left_dist = mapDistance(radius, left, point)
    right_dist = mapDistance(radius, right, point)
    fixed_dist = mapDistance(radius, left, right)
    x = (left_dist*left_dist + fixed_dist*fixed_dist - right_dist*right_dist)/(2*fixed_dist)
    y = math.sqrt(left_dist*left_dist - x*x)
    return (x, y)

radius = 1.
left = (0., 0.05)
right = (0., 1.5)
first_point = (0.2, 0.8)
second_point = (0.9, 1.3)
print('distance between points on map:')
print(mapDistance(radius, first_point, second_point))
print('x-y of first point:')
x_one, y_one = toCartesian(radius, left, right, first_point)
print(str(x_one) + ', ' + str(y_one))
x_two, y_two = toCartesian(radius, left, right, second_point)
print('xy of the second point')
print(str(x_two) + ', ' + str(y_two))
print('distance between points in cartesian')
print(math.sqrt(math.pow(x_two - x_one, 2) + math.pow(y_two - y_one, 2)))
