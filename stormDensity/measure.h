/*
This file has functions that measure the Haversine distance between objectsi, and the bearing.
 */

double haversine(double z);

double invHaversine(double z);



double distance(double lat_one, double lon_one, double lat_two, double lon_two, double radius);

double distanceDerivLat(double lat_one, double lon_one, double lat_two, double lon_two, double radius);

double distanceDerivLon(double lat_one, double lon_one, double lat_two, double lon_two, double radius);



typedef struct BearingVector BearingVector;
struct BearingVector{
  double dist;
  double x;
  double y;
};

typedef struct MeanMass MeanMass;


BearingVector calculateBearingVector(double lat_one, double lon_one, double lat_two, double lon_two, double radius);




