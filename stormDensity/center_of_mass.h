#include "measure.h"
#include<math.h>

#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_multiroots.h>


typedef struct COMParams COMParams;

struct COMParams{
  size_t num_points;
  double radius;
  double* masses;
  double* latitudes;
  double* longitudes;
};

typedef struct Point Point;
struct Point{
  double latitude;
  double longitude;
};



int measure_f(gsl_vector *lat_lon, void *p, gsl_vector *f);


int measure_df(gsl_vector *lat_lon, void *p,  gsl_matrix *J);


int measure_fdf(gsl_vector *lat_lon, void *p, gsl_vector *f,  gsl_matrix *J);

Point startGuess(COMParams* params);

Point calculateCOM(COMParams* params);
