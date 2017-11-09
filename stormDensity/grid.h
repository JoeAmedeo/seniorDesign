/* This is simply a collection of points with scores associated with them. */

#include "shape.h"
#include "barnes_hut.h"

typedef struct ScorePoint ScorePoint;
struct ScorePoint{
  double x;
  double y;
  long long score;
};

typedef struct ScoreGrid ScoreGrid;

struct ScoreGrid {
  ScorePoint* score_points;
  size_t num_points;
  
};

ScoreGrid initScoreGrid(CartesianPolygon polygon, double cell_width, double cell_height);

/* This takes in the root of a barne-hut tree, and a polygon, and a cell size, and computes the scores of cells in the tree */
ScoreGrid scoreTree(Node* tree, CartesianPolygon polygon, double cell_width, double cell_height);
