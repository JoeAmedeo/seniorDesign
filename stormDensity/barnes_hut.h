#include "qsc.h"

typedef struct Body Body;
struct Body{
  double latitude;
   double longitude;
  double mass;
  /* Just an FYI, you don't need to set this when creating the Body.
     When I go to build the trees, I set this, and then run a sort function */
  CubeSide face;
};

typedef struct BodyCollection BodyCollection;
struct BodyCollection{
  Body* bodies;
  size_t num_bodies;
}


  
typedef struct IntegerBody IntegerBody;
struct IntegerBody{
  unsigned int x;
  unsigned int y;
  unsigned long long mass;
};
  
typedef struct bh_quad{
  //x value of the lower left hand corner
  unsigned int  x;
  unsigned int y;

  /* If we add a body to the quadrant, then we need to 
  unsigned int center_x;
  unsigned int center_y;
  /* It's actually not possible to make the quadrant a square.

     Suppose we have a squared quadrant of size 51. Since we're using integers to represent all this stuff, we 
     would have to set one sub-quadrant to be of size 25, and another of size 26. However, we would then need sub-quadrants of sizes:

     25x25, 25x26, 26x25, 26x26. 
  */
  unsigned int width;
  unsigned int height;
} Quadrant; 


typedef struct Node Node;
struct Node{
  /* We can compute the center of mass in the following way:

     x = (x1*m1 + x2*m2 + ... + xN*mN)/M

     M is total mass of all points.

     And y in the same fashion. We store the numerator of this equation, and the mass, seperately. */
   unsigned long long cm_x_num;
   unsigned long long cm_y_num;
   unsigned long long total_mass;
  /* If this is an internal node, we calculate the latitude and longitude from the center of mass using the QSC inverse functions. 
     If it is an external node, then we just keep the latitude and longitude we were given */
   double latitude;
  double longitude;
  Quadrant* quad;
  Node* nw;
  Node* ne;
  Node* se;
  Node* sw;
};

CubeSide computeSide(Body body);
Node* build_trees(Body* bodies, size_t num_bodies);
long long score_at_point(Node* node, double x, double y, double theta);

