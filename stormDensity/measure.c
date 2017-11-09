/*
This file has functions that measure the Haversine distance between objectsi, and the bearing.
 */
#include<math.h>
#include "measure.h"


double haversine(double z){
  return sin(z/2)*sin(z/2);
}

double invHaversine(double z){
  return 2*asin(sqrt(z));
}

double distance(double lat_one, double lon_one, double lat_two, double lon_two, double radius){
  return radius*invHaversine(haversine(lat_one - lat_two) + cos(lat_one)*cos(lat_two)*haversine(lon_one - lon_two));
}

/* Take derivative of distance with respect to lat_one */
double distanceDerivLat(double lat_one, double lon_one, double lat_two, double lon_two, double radius){
  double numerator = radius*(0.5*sin(lat_one - lat_two) - sin(lat_one)*cos(lat_two)*haversine(lon_one - lon_two));
  double denominator = sqrt((-1.0*cos(lat_one)*cos(lat_two)*havesine(lon_one - lon_two) - havesine(lat_one - lat_two) + 1)*(cos(lat_one)*cos(lat_two)*haversine(lon_one - lon_two) + haversine(lat_one - lat_two)));
  return numerator/denominator;
}


double distanceDerivLon(double lat_one, double lon_one, double lat_two, double lon_two, double radius){
  double numerator = radius*cos(lat_one)*cos(lat_two)*sin(lon_one - lon_two);
  double denom = 2*sqrt((-1.0*cos(lat_one)*cos(lat_two)*haversine(lon_one - lon_two) - haversine(lat_one - lat_two) + 1)*(cos(lat_one)*cos(lat_two)*haversine(lon_one - lon_two) + haversine(lat_one - lat_two)))
    return numerator/denom;
}


BearingVector calculateBearingVector(double lat_one, double lon_one, double lat_two, double lon_two, double radius){
  double dist = distance(lat_one, lon_one, lat_two, lon_two, radius);
  BearingVector vec;
  vec.x = dist*(cos(lat_one)*sin(lat_two) - sin(lat_one)*cos(lat_two)*cos(lon_two - lon_one));
  vec.y = dist*(sin(lon_two - lon_one)*cos(lat_two));
  vec.dist = dist;
  return vec;
}


