#include <math.h>

long double score_at_point(Node* node, double x, double y, double theta){
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
