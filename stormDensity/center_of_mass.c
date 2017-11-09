#include "measure.h"
#include<math.h>
#include "center_of_mass.h"

#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_multiroots.h>

int measure_f(gsl_vector *lat_lon, void *p, gsl_vector *f){
  COMParams* params = (COMParams*) p;
  size_t num_points = params->num_points;
  const double radius = params->radius;
  const double* masses = params->masses;
  const double* latitudes = params->latitudes;
  const double* longitudes = params->longitudes;

  const double lat = gsl_vector_get(lat_lon, 0);
  const double lon = gsl_vector_get(lat_lon, 1);
  double x = 0;
  double y = 0;
  size_t i;
  double dist;
  BearingVector bVector;
  double lat_deriv, lon_deriv;
  for(i = 0; i < num_points; i++){
    bVector = calculateBearingVector(lat, lon, latitudes[i], longitudes[i], radius);
    dist = bVector.dist;
    x += masses[i]*bVector.x;
    y += masses[i]*bVector.y;
  }

  gsl_vector_set(f, 0, x);
  gsl_vector_set(f, 1, y);

  return GSL_SUCCESS; 
}


int measure_df(gsl_vector *lat_lon, void *p,  gsl_matrix *J){
  COMParams* params = (COMParams*) p;
  size_t num_points = params->num_points;
  const double radius = params->radius;
  const double* masses = params->masses;
  const double* latitudes = params->latitudes;
  const double* longitudes = params->longitudes;

  const double lat = gsl_vector_get(lat_lon, 0);
  const double lon = gsl_vector_get(lat_lon, 1);
  double x_lat = 0;
  double y_lat = 0;
  double x_lon = 0;
  double y_lon = 0;
  double x = 0;
  double y = 0;
  size_t i;
  double dist;
  BearingVector bVector;
  double lat_deriv, lon_deriv;
  for(i = 0; i < num_points; i++){
    dist = distance(lat, lon, latitudes[i], longitudes[i], radius);
    lat_deriv = distanceDerivLat(lat, lon, latitudes[i], longitudes[i], radius);
    lon_deriv = distanceDerivLon(lat, lon, latitudes[i], longitudes[i], radius);
    x_lat += masses[i]*(
			(cos(lat)*sin(latitudes[i])
			 - sin(lat)*cos(latitudes[i])*cos(lon - longitudes[i]))
			*lat_deriv
			+ (cos(lat)*cos(latitudes[i])*(-1.0*cos(lon - longitudes[i]))
			   - sin(lat)*sin(latitudes[i]))
			*dist
			);
    x_lon += masses[i]*(
			(cos(lat)*sin(latitudes[i])
			 - sin(lat)*cos(latitudes[i])*cos(lon - longitudes[i]))
			* lon_deriv
			+ sin(lat)*cos(latitudes[i])*sin(lon - longitudes[i])*dist
			);
    y_lat += masses[i]*(
			-1.0*cos(latitudes[i])*sin(lat - latitudes[i])*lat_deriv
			);
    y_lon += masses[i]*(
			cos(latitudes[i])*(-1.0*cos(lon - longitudes[i]))*dist
			- cos(latitudes[i])*sin(lon - longitudes[i])*lon_deriv
			);
  }

  gsl_matrix_set(J, 0, 0, x_lat);
  gsl_matrix_set(J, 0, 1, x_lon);
  gsl_matrix_set(J, 1, 0, y_lat);
  gsl_matrix_set(J, 1, 1, y_lon);
  return GSL_SUCCESS; 
}


int measure_fdf(gsl_vector *lat_lon, void *p, gsl_vector *f,  gsl_matrix *J){
  COMParams* params = (COMParams*) p;
  size_t num_points = params->num_points;
  const double radius = params->radius;
  const double* masses = params->masses;
  const double* latitudes = params->latitudes;
  const double* longitudes = params->longitudes;

  const double lat = gsl_vector_get(lat_lon, 0);
  const double lon = gsl_vector_get(lat_lon, 1);
  double x_lat = 0;
  double y_lat = 0;
  double x_lon = 0;
  double y_lon = 0;
  double x = 0;
  double y = 0;
  size_t i;
  double dist;
  BearingVector bVector;
  double lat_deriv, lon_deriv;
  for(i = 0; i < num_points; i++){
    bVector = calculateBearingVector(lat, lon, latitudes[i], longitudes[i], radius);
    dist = bVector.dist;
    x += masses[i]*bVector.x;
    y += masses[i]*bVector.y;
    lat_deriv = distanceDerivLat(lat, lon, latitudes[i], longitudes[i], radius);
    lon_deriv = distanceDerivLon(lat, lon, latitudes[i], longitudes[i], radius);
    x_lat += masses[i]*(
			(cos(lat)*sin(latitudes[i])
			 - sin(lat)*cos(latitudes[i])*cos(lon - longitudes[i]))
			*lat_deriv
			+ (cos(lat)*cos(latitudes[i])*(-1.0*cos(lon - longitudes[i]))
			   - sin(lat)*sin(latitudes[i]))
			*dist
			);
    x_lon += masses[i]*(
			(cos(lat)*sin(latitudes[i])
			 - sin(lat)*cos(latitudes[i])*cos(lon - longitudes[i]))
			* lon_deriv
			+ sin(lat)*cos(latitudes[i])*sin(lon - longitudes[i])*dist
			);
    y_lat += masses[i]*(
			-1.0*cos(latitudes[i])*sin(lat - latitudes[i])*lat_deriv
			);
    y_lon += masses[i]*(
			cos(latitudes[i])*(-1.0*cos(lon - longitudes[i]))*dist
			- cos(latitudes[i])*sin(lon - longitudes[i])*lon_deriv
			);
  }

  gsl_vector_set(f, 0, x);
  gsl_vector_set(f, 1, y);

  gsl_matrix_set(J, 0, 0, x_lat);
  gsl_matrix_set(J, 0, 1, x_lon);
  gsl_matrix_set(J, 1, 0, y_lat);
  gsl_matrix_set(J, 1, 1, y_lon);
  return GSL_SUCCESS; 
}

Point startGuess(COMParams* params){
  size_t i;
  double latitude_total = 0;
  double longitude_total = 0;
  for(i = 0; i < params->num_points; i++){
    latitude_total += params->latitudes[i];
    longitude_total += params->longitudes[i];
  }
  Point point;
  point.longitude = longitude_total/params->num_points;
  point.latitude = latitude_total/params->num_points;
  return point;
}

Point calculateCOM(COMParams* params){
  const gsl_multiroot_fdfsolver_type *hybrid = gsl_multiroot_fdfsolver_hybridsj;
  gsl_multiroot_fdfsolver* solver = gsl_multiroot_fdfsolver_alloc(hybrid, 2);
  gsl_multiroot_function_fdf fdf;
  fdf.f = &measure_f;
  fdf.df = &measure_df;
  fdf.fdf = &measure_fdf;
  fdf.n = 2;
  fdf.params = params;
  int max_iterations = 1000;
  Point start = startGuess(params);
  gsl_vector *initial_values  = gsl_vector_alloc(2);
  gsl_vector_set(initial_values, 0, start.latitude);
  gsl_vector_set(initial_values, 1, start.longitude);
  gsl_multiroot_fdfsolver_set(solver, &fdf, initial_values);
  int num_iterations = 0;
  int status;
  do{
    num_iterations++;
    status = gsl_multiroot_fdfsolver_iterate(solver);
    if(status)
      break;
    status = gsl_multiroot_test_residual(s->f, 1e-7);
  }while(status == GSL_CONTINUE && num_iterations < max_iterations);
  start.latitude = gsl_vector_get(solver->x, 0);
  start.longitude = gsl_vector_get(solver->x, 1);
  return start;
}
