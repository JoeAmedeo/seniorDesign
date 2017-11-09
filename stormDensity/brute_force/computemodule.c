#include<gsl/gsl_statistics.h>
#include<gsl/gsl_rstat.h>
#include<pthread.h>
#include<stdio.h>
#include<math.h>
#include<fenv.h>
#include<string.h>
#include<stdlib.h>
#define NUM_THREADS 4
#define NUM_TEMP_SCORES 1000
#define EARTHS_RADIUS 6371.000
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
  /* So, we have the variable points_calculated that we increase when we go to update the quantiles variable. */
  size_t* points_calculated;
  size_t total_num_points;
  /* When you update the quantiles, you need to get a mutex lock on it */
  pthread_mutex_t* mutex;
};

double haversine(double z){
  return sin(z/2)*sin(z/2);
}

double invHaversine(double z){
  return 2*asin(sqrt(z));
}

double distance(double lat_one, double lon_one, double lat_two, double lon_two, double radius){
  return radius*invHaversine(haversine(lat_one - lat_two) + cos(lat_one)*cos(lat_two)*haversine(lon_one - lon_two));
}


/* Pass in a ThreadData struct */
void* computeScoresOnThread(void* void_data){
  ThreadData* thread_data = (ThreadData*) void_data;
  size_t i,j;

  //Store NUM_TEMP_SCORES scores before depositing them into the quantiles calculators
  double temp_scores[NUM_TEMP_SCORES];
  int temp_scores_index = 0;
  int k, m;
  //we store the result of dividing event weight by distance squared. Then we do some error checking.
  double temp_temp_score;
  double latitude,longitude, temp_score, point_event_distance;
  double event_latitude, event_longitude, event_weight;
  for(i = 0; i < thread_data->num_points; i++){
    latitude = thread_data->points[i].latitude;
    longitude = thread_data->points[i].longitude;
    temp_score = 0.0;

    for(j = 0; j < thread_data->num_events; j++){
      event_latitude = thread_data->events[j].latitude;
      event_longitude = thread_data->events[j].longitude;
      event_weight = thread_data->events[j].weight;

      //we add 0.01 km to the event distance, so as to prevent a divide by zero.
      point_event_distance = distance(event_latitude, event_longitude, latitude, longitude, EARTHS_RADIUS) + 0.000001;

      feclearexcept(FE_ALL_EXCEPT);
      temp_temp_score = event_weight/(point_event_distance*point_event_distance);
      //now we need to check for underflow, overflow, and divide by zero errors.
      if(fetestexcept(FE_DIVBYZERO)){
	printf("Divide by zero error\n");
	exit(-1);
      }
      if(fetestexcept(FE_OVERFLOW)){
	printf("Overflowed\n");
	exit(-1);
      }
      if(fetestexcept(FE_UNDERFLOW)){
	printf("Underflowed\n");
	exit(-1);
      }
      temp_score += temp_temp_score;
    }


    temp_scores[temp_scores_index] = temp_score;
    thread_data->points[i].score = temp_score;
    if(temp_scores_index = NUM_TEMP_SCORES - 1 || i == thread_data->num_points - 1){
      //lock the quantiles mutex
      while(pthread_mutex_lock(thread_data->mutex) != 0){}
      thread_data->points_calculated += (1 + temp_scores_index);
      printf("\rIn progress %f", (1.0**thread_data->points_calculated)/thread_data->total_num_points);
      
      for(k = 0; k <=temp_scores_index; k++){
	for(m = 0; m < thread_data->num_quantiles; m++){
	  gsl_rstat_quantile_add((const double) temp_scores[k], thread_data->quantiles[m]);
	}
      }
      temp_scores_index = 0;
      pthread_mutex_unlock(thread_data->mutex);
    }else{
      temp_scores_index++;
    }
  }
  
}


unsigned long* computeScores(Event* events, size_t num_events, Point* points, size_t num_points, unsigned long num_colors){
 ThreadData data[NUM_THREADS];
 pthread_t threads[NUM_THREADS];
 int i;

 gsl_rstat_quantile_workspace** quantiles = (gsl_rstat_quantile_workspace**) malloc((num_colors - 1)*sizeof(gsl_rstat_quantile_workspace*));
 unsigned long j;
 for(j = 0; j < num_colors-1; j++){
   quantiles[j] = gsl_rstat_quantile_alloc((const double) 1.0*(j + 1)/num_colors);
 }
 size_t num_points_per_thread = num_points/NUM_THREADS;
 pthread_mutex_t* lock = (pthread_mutex_t*)malloc(sizeof(pthread_mutex_t));
 size_t* points_calculated = (size_t*)malloc(sizeof(size_t));
 *points_calculated = 0;
 pthread_mutex_init(lock, NULL);
 int rc;
 for(i = 0; i < NUM_THREADS; i++){
   data[i].events = events;
   data[i].num_events = num_events;
   data[i].points = &points[i*num_points_per_thread];
   if(i == NUM_THREADS - 1){
     data[i].num_points = num_points_per_thread + (num_points % NUM_THREADS);
   }else{
     data[i].num_points = num_points_per_thread;
   }
   data[i].quantiles = quantiles;
   data[i].num_quantiles = num_colors - 1;
   data[i].mutex = lock;
   data[i].points_calculated = points_calculated;
   data[i].total_num_points = num_points;
   rc = pthread_create(&threads[i], NULL, computeScoresOnThread, &data[i]);
 }
 for(i = 0; i < NUM_THREADS; i++){
   pthread_join(threads[i], NULL);
 }


 size_t k;
 unsigned long quantile_index = 0;
 double score;
 double* quantile_boundaries = (double*) malloc((num_colors - 1)*sizeof(double));
 
 for(quantile_index = 0; quantile_index < num_colors - 1; quantile_index++){
   quantile_boundaries[quantile_index] = gsl_rstat_quantile_get(quantiles[quantile_index]);
 }
 unsigned long* colors = (unsigned long*) malloc(sizeof(unsigned long)*num_points);
 for(k = 0; k < num_points; k++){
   quantile_index = 0;
   score = points[k].score;

   /* 
      Suppose there are 100 colors. Then there are 99 quantile boundaries. 
      Suppose our index gets to 99, then 99 < 99 is false, so we fall out of the while loop.
    */
   while(quantile_index < num_colors - 1 && score > quantile_boundaries[quantile_index]){
     quantile_index++;
   }
   colors[k] = quantile_index;

 }
 
 free(lock);
 free(quantiles);
 return colors;
}


/*
int main(int argc, char *argv[]){
  We will have several arguments:
    events file, a CSV file consisting of latitude,longitude,weight; items.
    points file, a CSV file consisting of latitude,longitude; items.
    Unsigned long, the number of colors
    Output file, where to put the output
  if(argc == 5){
    char* events_file = argv[1];
    char* points_file = argv[2];
    long num_colors = atol(argv[3]);
    char* output_file = argv[4];
    
  }else{
    printf("usage: compute events_file points_file num_colors output_file\n")
  }
}
*/
