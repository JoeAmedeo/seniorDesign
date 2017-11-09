#include "shape.h"
#include <math.h>

double degreesToRadians(double degrees){
  double one_eighty = (double) 180.0;
  return degrees*M_PI/one_eighty;
}

double minDouble(double x, double y){
  if(x < y){
    return x;
  }else{
    return y;
  }
}

double maxDouble(double x, double y){
  if(x > y){
    return x;
  }else{
    return y;
  }
}

double distance(MapPoint point_one, MapPoint point_two){
  double lat_one = point_one.lat;
  double lon_one = point_one.lon;
  double lat_two = point_one.lat;
  double lon_two = point_two.lat;
  double a = pow(sin(degreesToRadians((lat_two - lat_one))/2.0), 2.0) + cos(degreesToRadians(lat_one))*cos(degreesToRadians(lat_two))*pow(sin(degreesToRadians(lon_two - lon_one)/2.0, 2.0));
  return 2*EARTHS_RADIUS*asin(minDouble(1.0, sqrt(a)));
}

BoundingBox makeBoundingBox(MapPolygon* polygons, unsigned int num_polygons, MapPoint* points, size_t num_points){
  double min_lat = 1000;
  double max_lat = -1000;
  double min_lon = 1000;
  double max_lon = -1000;
  size_t i = 0;
  MapPoint point;
  char keepGoing = 1;
  // polygon index
  unsigned int p = 0;
  //point index in polygon
  unsigned int j = 0;
  while(keepGoing){
    if(i == num_points){
      if(p == num_polygons){
	keepGoing = 0;
      }else{
	if(j == polygons[p].num_points){
	  p++;
	  j = 0;
	}else{
	  point = polygons[p].points[j];
	  j++;
	}
      }
    }else{
      point = points[i];
      i++;
    }
    if(point->lat < min_lat){
      min_lat = point->lat;
    }
    if(point->lat > max_lat){
      max_lat = point->lat;
    }
    if(point->lon < min_lon){
      min_lon = point->lon;
    }
    if(point->lon > max_lon){
      max_lon = point->lon;
    }

  }
  BoundingBox box;
  MapPoint lower_left;
  lower_left.lat = min_lat;
  lower_left.lon = min_lon;
  box.pointOne = lower_left;
  MapPoint lower_right;
  lower_right.lat = min_lat;
  lower_right.lon = max_lon;
  box.pointTwo = lower_right;
  box.width = distance(lower_left, lower_right);
  MapPoint upper_right;
  upper_right.lat = max_lat;
  upper_right.lon = max_lon;
  box.height = distance(lower_right, upper_left);
  return box;
}



CartesianPoint toCartesian(MapPoint point, BoundingBox* box){
  /* We calculate the distance between the point and the 
lower left hand corner of the bounding box, and the lower right hand corner.

We then use the law of cosines to compute the angle of the line between the LLH corner and the point. Call this angle alpha.

alpha = arccos((d1^2 + w^2 - d2^2)/(2*d1*w))
y = d_{1}*sin(alpha)
x = d_{1}*cos(alpha) 
  */

  MapPoint* lower_left = box->pointOne;
  MapPoint* lower_right = box->pointTwo;
  double distance_left = distance(lower_left, point);
  double distance_right = distance(lower_right, point);
  double alpha = acos((pow(distance_left, 2.0) + pow(box->width, 2.0) - pow(distance_right, 2.0))/(2*distance_left*box->width));
  double y = distance_left*sin(alpha);
  double x = distance_left*cos(alpha);
  CartesianPoint p;
  p.x = x;
  p.y = y;
  return p;
}

MapPoint cartesianToMapPoint(CartesianPoint point, BoundingBox* box){

  
}
CartesianPolygon toCartesianPolygon(MapPolygon map_polygon, BoundingBox* box){
  CartesianPoint* points = (CartesianPoint*) malloc(map_polygon.num_points*(sizeof(CartesianPoint)));
  unsigned int i;
  for( i = 0; i < map_polygon.num_points; i++){
    points[i] = toCartesian(map_polygon.points[i], box);
  }
  CartesianPolygon polygon;
  polygon.points = points;
  polygon.num_points = map_polygon.num_points;
  return polygon;
}

SlopeInterceptLine makeIntoLine(CartesianPoint one, CartesianPoint two){
  double m = (two.y - one.y)/(two.x - one.x);
  double b = one.y - m*one.x;
  SlopeInterceptLine line;
  line.m = m;
  line.b = b;
  return line;
}



char doesVerticalLineIntersectLine(CartesianPoint top, double height, CartesianPoint point_one, CartesianPoint point_two){
  /* calculate the y value of where the vertical line (if you extended it out to infinity) would intersect the line formed by the t
     two cartesian points */
  SlopeInterceptLine line = makeIntoLine(point_one, point_two);
  double y = line.m*top.x + line.b;
  //check if the y value is in both line segments.
  if(y <= top.y && y >= (top.y - height) && y  <= maxDouble(point_one.y, point_two.y) && y >= minDouble(point_one.y, point_two.y)){
    return 1;
  }else{
    return 0;
  }

}

char doesVerticalLineIntersectPolygon(CartesianPoint top, double height, CartesianPolygon polygon){
  unsigned int i;
  for(i = 0; i < polygon.num_points - 1; i++){
    if(doesVerticalLineIntersectLine(top, height, polygon.points[i], polygon.points[i + 1])){
      return 1;
    }
  }
  return 0;
}

char doesHorizontalLineIntersectLine(CartesianPoint left, double width, CartesianPoint point_one, CartesianPoint point_two){
  /* calculate the x value of where the horizontal line (if you extended it out to infinity) would intersect the line formed by the t
     two cartesian points */
  SlopeInterceptLine line = makeIntoLine(point_one, point_two);
  double x = (left.y - line.b)/line.m;
  //check if the x value is in both line segments.
  if(x >= left.x && x <= (left.x + width) && x  <= maxDouble(point_one.x, point_two.x) && x >= minDouble(point_one.x, point_two.x)){
    return 1;
  }else{
    return 0;
  }

}



char doesVerticalLineIntersectPolygon(CartesianPoint top, double height, CartesianPolygon polygon){
  unsigned int i;
  for(i = 0; i < polygon.num_points - 1; i++){
    if(doesVerticalLineIntersectLine(top, height, polygon.points[i], polygon.points[i + 1])){
      return 1;
    }
  }
  return 0;
}

char doesHorizontalLineIntersectPolygon(CartesianPoint left, double width, CartesianPolygon polygon){
  unsigned int i;
  for(i = 0; i < polygon.num_points - 1; i++){
    if(doesHorizontalLineIntersectLine(left, width, polygon.points[i], polygon.points[i + 1])){
      return 1;
    }
  }
  return 0;
}

unsigned int howManyTimesDoesHorizontalLineIntersectPolygon(CartesianPoint left, double width, CartesianPolygon polygon){
  unsigned int i;
  unsigned int num_intersections = 0;
  for(i = 0; i < polygon.num_points - 1; i++){
    if(doesHorizontalLineIntersectLine(left, width, polygon.points[i], polygon.points[i + 1])){
      num_intersections++;
    }
  }
  return num_intersections;
}

char doesRectIntersectPolygon(CartesianRect rect, CartesianPolygon polygon){
  /* First check if any of the sides intersect the polygon */
  CartesianPoint lower_left;
  lower_left.x = rect.upper_left.x;
  lower_left.y = rect.upper_left.y - rect.height;
  CartesianPoint upper_right;
  upper_right.x = rect.upper_left.x + rect.width;
  upper_right.y = rect.upper_left.y;
  if(doesHorizontalLineIntersectPolygon(rect.upper_left, rect.width, polygon) ||
     doesVerticalLineIntersectPolygon(rect.upper_left, rect.height, polygon) ||
     doesHorizontalLineIntersectPolygon(lower_left, rect.width, polygon) ||
     doesVerticalLineIntersectPolygon(rect.upper_right, rect.height, polygon)){
    return 1;
  }else{
    /* either the rectangle is completely contained in the polygon, or there is no intersection */
    /* So, we draw a ray between the upper left hand corner, out to the right to infinity.

       Since each line in the polygon intersects this ray 0 or 1 times, we can simply check how many of the lines in the polygon intercept this ray.
       If an odd number of lines intercept this ray, then the upper left hand corner is contained in the polygon, so the whole rectangle is in the polygon.*/
    unsigned int i;
    double max_x = 0;
    for(i = 0; i < polygon.num_points; i++){
      if(max_x < polygon.points[i].x){
	max_x = polygon.points[i].x;
      }
    }
    unsigned int num_intersections = howManyTimesDoesHorizontalLineIntersectPolygon(rect.upper_left, max_x + 0.1 - rect.upper_left.x, polygon);
    if(num_intersections % 2 == 1){
      return 1;
    }else{
      return 0;
    } 
    
  }

				      
}
