%module compute
%{
  #include<gsl/gsl_statistics.h>
#include<gsl/gsl_rstat.h>
#include<pthread.h>
#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define NUM_THREADS 4
#define NUM_TEMP_SCORES 100
#define EARTHS_RADIUS 3958.7613
typedef struct Event Event;
struct Event{
  double latitude;
  double longitude;
  double weight;
};

typedef struct Point Point;
struct Point{
  double latitude;
  double longitude;
  /* The score will be calculated and inserted later on */
  double score;
};

typedef struct ThreadData ThreadData;
struct ThreadData{
  Event* events;
  size_t num_events;
  Point* points;
  size_t num_points;
  gsl_rstat_quantile_workspace** quantiles;
  unsigned int num_quantiles;
  /* When you update the quantiles, you need to get a mutex lock on it */
  pthread_mutex_t* mutex;
};

extern  double haversine(double z);

extern double invHaversine(double z);

extern double distance(double lat_one, double lon_one, double lat_two, double lon_two, double radius);


/* Pass in a ThreadData struct */
 extern void* computeScoresOnThread(void* void_data);

 extern unsigned long* computeScores(Event* events, size_t num_events, Point* points, size_t num_points, unsigned long num_colors);
  %}

%include "carrays.i"
%array_class(unsigned long, unsignedLongArray);
typedef struct Event Event;
struct Event{
  double latitude;
  double longitude;
  double weight;
};

typedef struct Point Point;
struct Point{
  double latitude;
  double longitude;
  /* The score will be calculated and inserted later on */
  double score;
};

typedef struct ThreadData ThreadData;
struct ThreadData{
  Event* events;
  size_t num_events;
  Point* points;
  size_t num_points;
  gsl_rstat_quantile_workspace** quantiles;
  unsigned int num_quantiles;
  /* When you update the quantiles, you need to get a mutex lock on it */
  pthread_mutex_t* mutex;
};

%typemap(in) Point*{
  if(PyList_Check($input)){
    size_t length = PyList_Size($input);
    size_t i = 0;
    $1 = (Point*) malloc(length*sizeof(Point));
    for(i = 0; i < length; i++){
      PyObject* o =  PyList_GetItem($input, i);
      //pass in a tuple of the form (latitude, longitude)
      $1[i].latitude = PyFloat_AsDouble(PyTuple_GetItem(o, 0));
      $1[i].longitude = PyFloat_AsDouble(PyTuple_GetItem(o, 1));
      $1[i].score = 0.0;
    }
  }else{
    PyErr_SetString(PyExc_TypeError, "not a good object");
  }
 }
%typemap(freearg) Point*{
  free((Point*) $1);
 }
%typemap(in) Event*{
  if(PyList_Check($input)){
    size_t size = PyList_Size($input);
    size_t i = 0;
    $1 = (Event*) malloc(size*sizeof(Event));
    for(i = 0; i < size; i++){
      PyObject* o =  PyList_GetItem($input, i);
      //pass in a tuple of the form (latitude, longitude, weight)
      $1[i].latitude = PyFloat_AsDouble(PyTuple_GetItem(o, 0));
      $1[i].longitude = PyFloat_AsDouble(PyTuple_GetItem(o, 1));
      $1[i].weight = PyFloat_AsDouble(PyTuple_GetItem(o, 2));
    }
  }else{
    PyErr_SetString(PyExc_TypeError, "not a good object");
  }
 }
%typemap(freearg) Event*{
  free((Event*) $1);
 }


extern  double haversine(double z);

extern double invHaversine(double z);

extern double distance(double lat_one, double lon_one, double lat_two, double lon_two, double radius);


/* Pass in a ThreadData struct */
 extern void* computeScoresOnThread(void* void_data);


extern unsigned long* computeScores(Event* events, size_t num_events, Point* points, size_t num_points, unsigned long num_colors);
