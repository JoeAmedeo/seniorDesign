#include "shape.h"
#include "grid.h"
#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include "barnes_hut.h"
double min(const double *numbers, size_t array_size){
  size_t i;
  double min = numbers[0];
  for(i = 1; i < array_size; i++){
    if(numbers[i] < min){
      min = numbers[i];
    }
  }
  return min;
}


double max(const double *numbers, size_t array_size){
  size_t i;
  double max = numbers[0];
  for(i = 1; i < array_size; i++){
    if(numbers[i] > max){
      max  = numbers[i];
    }
  }
  return min;
}

/* This will calculate the area of the polygon
I used the formula from Wolfram MathWorld found here:  http://mathworld.wolfram.com/PolygonArea.html
 */
double polygonArea(const CartesianPolygon polygon){
  double area = 0;
  size_t i;
  CartesianPoint point_one;
  CartesianPoint point_two;
  for(i = 0; i < polygon.num_points - 1; i++){
    point_one = polygon.points[i];
    point_two = polygon.points[i + 1];
    area += 0.5*(point_one.x*point_two.y - point_two.x*point_one.y);
  }
  point_one = polygon.points[polygon.num_points - 1];
  point_two = polygon.points[0];
  area += 0.5*(point_one.x*point_two.y - point_two.x*point_one.y);
  return fabs(area);
}



/* We need to take in the polygon, a cell width, and a cell height. Then, 
   return the grid, which will contain the points with unfilled scores */
ScoreGrid initScoreGrid(const CartesianPolygon polygon, const double cell_width, const double cell_height){
  unsigned int num_points = 0;

  // compute the max x, max y, min x, and min y.
  double min_x = polygon.points[0].x;
  double min_y = polygon.points[0].y;
  double max_x = min_x;
  double max_y = min_y;
  size_t i;
  CartesianPoint point;
  for(i = 1; i < polygon.num_points; i++){
    point = polygon.points[i];
    if(min_x > point.x){
      min_x = point.x
    }
    if(max_x < point.x){
      max_x = point.x;
    }
    if(min_y > point.y){
      min_y = point.y;
    }
    if(max_y < point.y){
      max_y = point.y;
    }
  }
  //we add these to accomodate the cells that are outside of the polygon, but may overlap with the polygon.
  min_x -= cell_width;
  max_x += cell_width;
  min_y -= cell_height;
  max_y += cell_height;
  //we set the initial capacity to the area of the polygon divided by the area of a cell. 
  size_t capacity = polygonArea(polygon)/(cell_width*cell_height);
  size_t num_points = 0;
  size_t i = 0;
  ScorePoint* points = (ScorePoint*) malloc(capacity*sizeof(ScorePoint));
  size_t row = 1;
  size_t col = 0;
  CartesianRect cell;
  cell.width = cell_width;
  cell.height = cell_height;
  CartesianPoint point;
  /* move up one row at a time */
  while(row*cell_height + min_y <= max_y){
    while((col + 1)*cell_width + min_x <= max_x){
      point.x = min_x + col*cell_width;
      point.y = min_y + row*cell_height;
      cell.point = point;
      if(doesRectIntersectPolygon(rect, polygon)){
	if(num_points == capacity){
	  /* We're probably pretty close, so expand by 10% */
	  points = realloc(points, 1.1*capacity*sizeof(ScorePoint));
	  if(points){
	    capacity = 1.1*capacity;
	  }else{
	    printf("Could not realloc when creating the list of points to score at. Aborting");
	    exit(EXIT_FAILURE);
	  }
	}
	points[i].x = point.x + 0.5*cell_width;
	points[i].y = point.y - 0.5*cell_height;
	points[i].score = 0;
	num_points++;
	i++;
      }

      
      col ++;
    }
    col = 0;
    row++;
  }
  if(capacity > num_points){
    /*realloc to shrink capacity */
    points = realloc(points, num_points*sizeof(ScorePoint));
    if(points){}else{
      printf("Could not realloc to shrink list of points to score at. Aborting");
      exit(EXIT_FAILURE);	
    }
  }
  ScoreGrid grid;
  grid.score_points = points;
  grid.num_points = num_points;
  return grid;
  
}


ScoreGrid scoreTree(Node* tree, CartesianPolygon polygon, double cell_width, double cell_height, double theta){

  ScoreGrid grid = initScoreGrid(polygon, cell_width, cell_height);
  size_t i;
  for(i = 0; i < grid.score_points; i++){
    grid.score_points[i].score = score_at_point(tree, grid.score_points[i].x, grid.score_points[i].y, theta);
  }
  return grid;


}
