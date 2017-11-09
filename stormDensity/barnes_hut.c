#include<math.h>
#include <stdio.h>
#include<limits.h>
#include<stdlib.h>
#include "shape.h"
#include "grid.h"
#include "barnes_hut.h"
#include "qsc.h"
/*
  Returns 1 if the point is within the quadrant. Returns 0 if the point is not within the quadrant.
 */
int inside_quadrant(unsigned int x, unsigned int y, Quadrant* quadrant){
  if((x < quadrant->x) || (y < quadrant-> y)){
    return 0;
  }else if((x <= (quadrant->x + quadrant->width)) && (y <= (quadrant-> y + quadrant->height))){
    return 1;
  }else{
    return 0;
  }
}


/*
Given a point and a quadrant, this returns 1 if the point is in the north-west region of the quadrant.
Returns 2 if the point is in the north-east region
returns 3 if the point is in the south-east region
returns 4 if the point is in the south-west region

Returns 0 if the point isn't in the quadrant
 */
char get_region(unsigned int x,  unsigned int y, Quadrant* quad){

  /* 
     As of 1/26/17, the following is an old comment. But still somewhat relevant.
I actually thought we would need to handle the fact that quad->size/2 rounds down if quad->size is an odd number.

     We do not need to.

     Suppose size is an even number. Then, we don't need to do anything, since dividing by 2 doesn't result in loss of precision.

     Suppose size is an odd number. If x < z + floor(y/2), then x < z + z/2.
     If x = z + floor(y/2), then x < z + y/2.
  */
 
  if(inside_quadrant(x, y, quad)){
    /* This is if we're finding the region of a point in an empty quadrant. */
    unsigned int center_x = quad->center_x;
    unsigned int center_y = quad->center_y;
    if(center_x == 0 && center_y == 0){
      center_x = quad->x + quad->width/2;
      center_y = quad->y + quad->height/2;
    }
      if(x <= center_x){
	if(y <= center_y ){
	  return 4;
	}else{
	  return 1;
	}
      }else{
	if(y <= center_y){
	  return 3;
	}else{
	  return 2;
	}
      }

  }else{
    return 0;
  }
}

/* This returns 0 if the addition will not overflow, it returns 1 if the addition will overflow */
char add_overflows(unsigned long long x, unsigned long long y){
  if(x > ULLONG_MAX - y){
    return 1;
  }else{
    return 0;
  }
}

/* This returns 0 if the multiplication will not overflow, it returns 1 if the multiplication WILL overflow */
char mult_overflows(unsigned long long x, unsigned long long y){
  if(x > ULLONG_MAX/y){
    return 1;
  }else{
    return 0;
  }
}

/* Returns 0 if there is no overflow, returns 1 if there is overflow
 Since the IntegerBody struct only consists of three parts, pass in an array of 
 IntegerBody structs, not an array of pointers */
char has_overflow(IntegerBody* bodies, unsigned long num_bodies, uint exp){
  unsigned long long sum_x = 0;
  unsigned long long sum_y = 0;
  unsigned long i = 0;
  while(i < num_bodies){
    /* We can divide by 2^exp by bit shiting exp bits to the right */
    unsigned long long weight_scaled = bodies[i].mass >> exp;
    //I don't want any weight to go to zero. 
    if(weight_scaled == 0){
      weight_scaled = 1;
    }
    if(mult_overflows(weight_scaled, (unsigned long long) bodies[i].x)){
      return 1;
    }
    if(mult_overflows(weight_scaled, (unsigned long long)  bodies[i].y)){
      return 1;
    }
    unsigned long long x_mult = bodies[i].x*weight_scaled;
    unsigned long long y_mult = bodies[i].y*weight_scaled;
    if(add_overflows(x_mult, sum_x)){
      return 1;
    }
    if(add_overflows(y_mult, sum_y)){
      return 1;
    }
    sum_x += x_mult;
    sum_y += y_mult;
  }
  return 0;
}

/* This function should try to find a good 2^n value that we can divide our weights by, so as to avoid overflow when computing the numerator of the 
   center of mass.
*/
uint scaling_factor(IntegerBody* bodies, unsigned long num_bodies){
  if(has_overflow(bodies, num_bodies, 0)){
    uint largest_overflow = 0;
    uint smallest_no_overflow = 0;
    uint exp = 5;
    char keepGoing = 1;
    while(keepGoing){
      if(has_overflow(bodies, num_bodies, exp)){
	largest_overflow = exp;
	if(smallest_no_overflow == 0){
	  exp += 5;
	}else{
	  //average the current exponent with the smallest exponent that we've found so far that prevents overflow.
	  exp = (exp + smallest_no_overflow)/2;
	}
	
      }else if(exp == largest_overflow + 1){
	return exp;
      }else{
	smallest_no_overflow = exp;
	exp = (exp + largest_overflow)/2;
      }
    }
  }else{
    return 0;
  }
}

/* 

Pass in an array of Body structs.
The economic damage can be huge, so we may need to scale it to prevent overflow when we calculate the numerator of the center of mass



This returns a pointer to an array of IntegerBody structs. This does NOT free bodies.


*/
IntegerBody* scale_bodies(Body* bodies, unsigned long num_bodies){
  IntegerBody* int_bodies = (IntegerBody*) malloc(num_bodies*sizeof(IntegerBody));
  if(int_bodies == NULL){
    printf("Couldn't reserve memory for creating the scale bodies");
    exit(EXIT_FAILURE);
  }else{
    /* This was relevant when we were working with miles for our (x, y) coordinate.
       Our projection should use meters for this. 
    unsigned long i;
    for(i = 0; i < num_bodies; i++){
      int_bodies[i].x = 10*bodies[i].x;
      int_bodies[i].y = 10*bodies[i].y;
      int_bodies[i].mass = (unsigned long long) bodies[i].mass;
    }
    */
    //now that we have the int bodies, we should figure out the scaling factor for the mass.
    uint factor = scaling_factor(int_bodies, num_bodies);
    if(factor == 0){
      printf("Scaling was unecessary\n");
      return int_bodies;
    }else{
      for(i = 0; i < num_bodies; i++){
	int_bodies[i].mass = int_bodies[i].mass >> factor;
	if(int_bodies[i].mass == 0){
	  int_bodies[i].mass = 1;
	}
      }
      return int_bodies;
    }
  }
}





/* quad_x and quad_y are the coordinates of the lower left hand corner of the quadrant */
Node* init_node(unsigned int quad_width, unsigned int quad_height, unsigned int quad_x, unsigned int quad_y){
  Node* node = (Node*)malloc(sizeof(Node));
  node->total_mass = 0;
  node->cm_x_num = 0;
  node->cm_y_num = 0;
  Quadrant* quad = (Quadrant*)malloc(sizeof(Quadrant));
  quad->x = quad_x;
  quad->center_x = 0;
  quad->y = quad_y;
  quad->center_y = 0;
  quad->width = quad_width;
  quad->height = quad_height;
  node->quad = quad;
  node->nw = NULL;
  node->ne = NULL;
  node->se = NULL;
  node->sw = NULL;
  return node;
}


/* 
When you call this, you need to pass in a parent to the pointer node. You also need to pass in the region as a char.
1 is nw, 2 is ne, 3 is se, 4 is sw.
We use the quadrant information from parent_node to specify quadrant_size, quad_x and quad_y when we call init_node.

I've decided that this function should also add the external node to the parent. I'm doing this because we may need to also set some things in the parent's quadrant. 


Returns a pointer to this new external node.
*/
Node* init_add_external_node(Node* parent_node, char region, unsigned long long mass, unsigned int x,  unsigned int y){
  Quad* quad = parent_node->quad;
  unsigned int new_x = 0;
  unsigned int new_y = 0;
  if(region == 1 || region == 4){
    new_x = x;
  }
  if(region == 3 || region == 4){
    new_y = y;
  }
  unsigned int new_width = 0;
  unsigned int new_height = 0;
  if(quad->center_x == 0 && quad->center_y == 0){
    if(quad->width % 2 == 0){
      new_width = quad->width/2;
    }else{
      new_width = quad->width/2 + 1;
    }
    if(quad->height % 2 == 0){
      new_height = quad->height/2;
    }else{
      new_height = quad->height/2 + 1;
    }
    if(region == 1 || region == 4){
      quad->center_x = quad->x + new_width;
    }else{
      quad->center_x = quad->x + quad->width - new_width;
    }
    if(region == 3 || region == 4){
      quad->center_y = quad->y + new_width;
    }else{
      quad->center_y = quad->y + quad->height - new_height;
    }
  }else{
    /* Then the center has already been set */
    if(region == 1 || region == 4){
      new_width = quad->center_x - quad->x;
    }else{
      new_width = quad->width - (quad->center_x - quad->x);
    }
    if(region == 3 || region == 4){
      new_height = quad->center_y - quad->y;
    }else{
      new_height = quad->height - (quad->center_y - quad->y);
    }
  }
  if(region == 2 || region == 3){
    new_x = quad->center_x;
  }
  if(region == 1 || region == 2){
    new_y = quad->center_y;
  }
  Node* new_node = init_node(new_width, new_height, new_x, new_y);
  new_node->cm_x_num = x*mass;
  new_node->cm_y_num = y*mass;
  new_node->total_mass = mass;
  return new_node;
}


void convert_external_node_to_internal(Node* node){
  unsigned int x = (unsigned int) (node->cm_x_num/node->total_mass);
  unsigned int y = (unsigned int) (node->cm_y_num/node->total_mass);
  char region = get_region(x, y, node->quad);
  /* We need to make an external node, and then attach that external node to the current node */
  Node* new_node = init_external_node(node, region, node->total_mass, x, y);
  if(region == 1){
    node->nw = new_node;
  }else if(region == 2){
    node->ne = new_node;
  }else if(region == 3){
    node->se = new_node;
  }else if(region == 4){
    node->sw = new_node;
  }
}


/* Returns 0 if the body is not within the node's quadrant, or if the mass of the body is zero.

   If it is successful, it returns 1.
*/
int add_body(Node* node, IntegerBody* body){
  if(inside_quadrant(body->x, body->y, node->quad)){
    char region = get_region(body->x, body->y, node->quad);
    if(region == NULL){
      return 0;
    }else{
      Node** region_node;
      if(region == 1){
	region_node = &(node->nw);
      }else if(region == 2){
	region_node = &(node->ne);
      }else if(region == 3){
	region_node = &(node->se);
      }else if(region == 4){
	region_node = &(node->sw);
      }
      /* update the center of mass of the node */
      node->cm_x_num += body->x*body->mass;
      node->cm_y_num += body->y*body->mass;
      node->total_mass += body->mass;
      /* We need to make sure that if we reach a node in which either the width or height of the quadrant is equal to 1, that we simply add the body to the node without creating any child nodes, since we cannot cut this quadrant into sub-quadrants. */
      if(node->quad->width > 1 && node->quad->height > 1){
	if(**region_node == NULL){

	  /* Need to initialize the region */
	  init_add_external_node(node, region, body->mass, body->x, body->y);
	  return 1;
	}else{
	  /* The region already has one or more points in it.
	     If there is only one point, then we need to move that point into the proper child node.
	  */
	  if(*region_node->nw == NULL && *region_node->ne == NULL && *region_node->se == NULL && *region_node->sw == NULL){
	    /* Then the node only contains 1 point. Move that point into proper child node*/
	    convert_external_node_to_internal(*region_node);
	  }
	  return add_body(*region_node, body);
	}
      }
    }
  }
}else{
    return 0;
  }
}

CubeSide computeSide(Body body){
  return computeCubeSide(body.longitude, body.latitude);
}

/* Returns NULL if something goes wrong
*/
Node* build_trees(Body* bodies, size_t num_bodies){

  /*  set the face of each. */
  size_t i;
  CubeSide face;

  /* compute the width and heights .
Order in arrays: front, right, back, left, top, bottom
   */
  double* latitudes[6] = {0, 0, 0, 0, 90, -90};
  double* longitudes[6] = {0, 90, 180, -90, 0, 0};
  CubeSide* faces[6] = {FRONT, RIGHT, BACK, LEFT, TOP, BOTTOM};
  int i;
  for(i = 0; i < 6; i++){
    forwardProjection(&latitudes[i], &longitudes[i], 1, faces[i]);
  }
  for(i = 0; i < num_bodies; i++){
    face = computeSide(bodies[i]);
    
  }
  
  IntegerBody* int_bodies = scale_bodies(bodies, num_bodies);
  /* get the smallest and largest x, y values */
  unsigned long i = 0;
  unsigned int smallest_x = int_bodies[0].x;
  unsigned int largest_x = int_bodies[0].x;
  unsigned int smallest_y = int_bodies[0].y;
  unsigned int largest_y = int_bodies[0].y;
  for(i = 1; i < num_bodies; i++){
    if(int_bodies[i].x < smallest_x){
      smallest_x = int_bodies[i].x;
    }
    if(int_bodies[i].x > largest_x){
      largest_x = int_bodies[i].x;
    }
    if(int_bodies[i].y < smallest_y){
      smallest_y = int_bodies[i].y;
    }
    if(int_bodies[i].y > largest_y){
      largest_y = int_bodies[i].y;
    }
  }
  unsigned int x = smallest_x;
  if(smallest_x > 0){
    x--;
  }
  unsigned int y = smallest_y;
  if(smallest_y > 0){
    y--;
  }
  
  Node* root = init_node(largest_x - smallest_x + 2, largest_y - smallest_y + 2, x, y);
  unsigned long i = 0;
  for(i = 0; i < num_bodies; i++){
    if(add_body(root, int_bodies[i]) == 0){
      return 0;
    }
  }
  return root;
}

long long score_at_point(Node* node, double x, double y, double theta){                                                                            
  double node_cm_x = node->cm_x_num/node->total_mass;                                                                                                
  double node_cm_y = node->cm_y_num/node->total_mass;                                                                                                
  double distance_squared = pow(x - node_cm_x, 2) + pow(y - node_cm_y, 2);                                                                           
  double distance = sqrt(distance_squared);                                                                                                          
  double mass = node->total_mass;                                                                                                                    
  double size = node->quad->size;                                                                                                                    
  if(( node->nw == NULL && node->ne == NULL && node->se == NULL && node->sw == NULL) || size/distance < theta){                                      
    return (long double) mass/distance_squared;                                                                                                      
  }else{                                                                                                                                             
    long double score = 0;                                                                                                                           
    if(node->nw != NULL){                                                                                                                            
      score += score_at_point(node->nw, x, y, theta);                                                                                                
    }                                                                                                                                                
    if(node->ne != NULL){                                                                                                                            
      score += score_at_point(node->ne, x, y, theta);                                                                                                
    }                                                                                                                                                
    if(node->se != NULL){                                                                                                                            
      score += score_at_point(node->se, x, y, theta);                                                                                                
    }                                                                                                                                                
    if(node->sw != NULL){                                                                                                                            
      score += score_at_point(node->sw, x, y, theta);                                                                                                
    }                                                                                                                                                
    return score;                                                                                                                                    
  }                                                                                                                                                  
} 


