#define EARTHS_RADIUS 3958.7613

typedef struct MapPoint MapPoint;
/* hold the point in (latitude, longitude), lat and lon in degrees. */
struct MapPoint{
  double lat;
  double lon;
};



  
typedef struct BoundingBox BoundingBox;
struct BoundingBox{

  /*
    Lower left hand corner*/
  MapPoint pointOne;
  /* Lower right hand corner */
  MapPoint pointTwo; 
  /* width and height in miles */
  double width;
  double height;
};


typedef struct CartesianPoint CartesianPoint;
struct CartesianPoint{
  double x;
  double y;
};

typedef struct VerticalLine VerticalLine;
struct VerticalLine{
  /* the x coordinate of the vertical line, the max y value of the endpoints, and the min y of the
     endpoints*/
  double x;
  double y_min;
  double y_max;
};



typedef struct MapPolygon MapPolygon;
struct MapPolygon{
  /* an array of points */
  MapPoint* points;
  size_t num_points;
};


/* Use the haversine formula to calculate distance between two points.
We approximate the earth as a sphere.

Got information from here: http://www.movable-type.co.uk/scripts/latlong.html
 */
double distance(MapPoint point_one, MapPoint point_two);
/* Make a bounding box that surrounds the polygons, and the points */
BoundingBox makeBoundingBox(MapPolygon* polygons, unsigned int num_polygons, MapPoint* points, unsigned long long num_points);


CartesianPoint toCartesian(MapPoint point, BoundingBox* box);

MapPoint cartesianToMapPoint(CartesianPoint point, BoundingBox* box);

/* We want to perform our calculations in cartesian, so let's re-create 
   analogous structs for cartesian objects */


typedef struct CartesianPolygon CartesianPolygon;
struct CartesianPolygon{
  CartesianPoint* points;
  size_t num_points;
};

/* I'm going to assume that we can simply convert all of the points in the polygon into cartesian points */
CartesianPolygon toCartesianPolygon(MapPolygon mapPolygon);

typedef struct CartesianRect CartesianRect;
struct CartesianRect{
  CartesianPoint upper_left;
  double width;
  double height;
};

typedef struct struct SlopeInterceptLine SlopeInterceptLine;
struct SlopeInterceptLine {
  double m;
  double b;
};
SlopeInterceptLine makeIntoLine(CartesianPoint one, CartesianPoint two);




char doesVerticalLineIntersectPolygon(CartesianPoint top, double height, CartesianPolygon polygon);
char doesHorizontalLineIntersectPolygon(CartesianPoint left, double width, CartesianPolygon polygon); 
/* This returns 1 if the |R \cap P| > 0 */
char doesRectIntersectPolygon(CartesianRect rect, CartesianPolygon polygon);






