#include "shape.h"
#include "barnes_hut.h"
/* This library
should have a function that will take in the polygon file, and return a MapPolygon object from shape.h,
and a function that will take in an events file, and return a BodyCollection (from barnes_hut.h) */ 

/* The polygon file should contain the points in the following way:

lat1, lon1; lat2, lon2; lat3, lon3; ...; latN, lonN;

*/



MapPolygon readPolygon(char* filename);

/* The bodies/events file should contain points with weights in the following way:

lat1, lon1, weight1; lat2, lon2, weight2; ... ; latN, lonN, weightN;
*/

BodyCollection readBodies(char* filename);

/* This function will take in a ScoreGrid, and a filename, and output the score grid in the following way:

lat1, lon1, score1; lat2, lon2, score2; ... ; latN, lonN, scoreN;

*/
void writeScoreGrid(ScoreGrid scores, char* filename);
