#include<stddef.h>

typedef enum {FRONT = 0, RIGHT = 1, BACK = 2, LEFT = 3, TOP = 4, BOTTOM= 5} CubeSide;

typedef struct QSCCoordinates QSCCoordinates;
struct QSCCoordinates{
  double x;
  double y;
};



void forwardProjection(double* latitudes, double* longitude, size_t num_coordinates, CubeSide face);
/*Both longitude and latitude are in degrees */
CubeSide computeCubeSide(double longitude, double latitude);
