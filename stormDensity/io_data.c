#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "io_data.h"

/* This returns the text of the file as a string 
   This exits with an error if we can't read the file for some reason. I do this,
   since not being able to read one of these files renders the program useless. 
*/
char* readFile (char* filename){
  FILE* file;
  file = fopen(filename, "r");
  if(file == NULL){
    fclose(file);
    Error("Unable to open file: %s", filename);
  }else{
    // get the size of the file, and use this for the string.
    struct stat file_statistic;

    /* Probably not a major issue, but I figured I'd take a hint from this:

       https://www.securecoding.cert.org/confluence/display/c/FIO19-C.+Do+not+use+fseek%28%29+and+ftell%28%29+to+compute+the+size+of+a+regular+file

       :) 
    */
    if(fstat(file, &file_statistic) < 0){
      fclose(file);
      Error("Unable to measure size of file: %s", filename);
    }else{
      off_t size = file_statistic.st_size;
      char* file_contents = (char*) malloc(size);
      if(file_contents == NULL){
	fclose(file);
	Exit("Unable to reserve space to hold file: %s", filename);
      }else{
	if(fgets(file_contents, size, file) != NULL){
	  if(file_contents[size - 1] != '\0'){
	    fclose(file);
	    Exit("File is not null terminated: %s", filename);
	  }else{
	    fclose(file);
	    return file_contents;
	  }
	}else{
	  fclose(file);
	  Exit("Unable to read the file: %s", filename);
	}
      }
      
    }
  }
}

/* counts the number of times character c occurs in the string */
size_t count(char* string, char c){
  size_t i = 0;
  size_t num = 0;
  while(string[i] != '\0'){
    if(string[i] == c){
      num++;
    }
    i++;
  }
  return num;
}
MapPolygon readPolygon(char* filename){
  char* file_text = readFile(filename);
  /* Now that we have the text in an easy to work with form, we first want to get the number of 
     points. We can simply count the number of semi-colons. The number of semicolons plus one 
  is the number of points in the polygon. */
  size_t num_points = count(file_text, ';') + 1;
  MapPoint* points = (MapPoint*) malloc(num_points*sizeof(MapPoint));
  size_t i, j;
  char* text_pointer = file_text;
  double lat, lon;
  int n;
  for(i = 0; i < num_points; i++){
    sscanf(text_pointer, "%lf , %lf ;%n", &lat, &lon, &n);
    text_pointer += n;
    points[i].lat = lat;
    points[i].lon = lon;
  }
  MapPolygon polygon;
  polygon.points = points;
  polygon.num_points = num_points;
  return polygon;
}

BodyCollection readBodies(char* filename){
  char* file_text = readFile(filename);

  size_t num_points = count(file_text, ';') + 1;
  Body* points = (Body*) malloc(num_points*sizeof(Body));
  size_t i, j;
  char* text_pointer = file_text;
  double lat, lon, weight;
  int n;
  for(i = 0; i < num_points; i++){
    sscanf(text_pointer, "%lf , %lf , %lf ;%n", &lat, &lon, &weight, &n);
    text_pointer += n;
    points[i].lat = lat;
    points[i].lon = lon;
    points[i].weight = weight;
  }
  BodyCollection collection;
  collection.bodies = points;
  collection.num_bodies = num_points;
  return collection;
}

void writeScoreGrid(ScoreGrid scores, char* filename){
  FILE* file = fopen(filename, "w");
  if(file == NULL){
    Exit("Could not open file for writing: %s", filename);
  }
  size_t i;
  for(i = 0; i < scores.num_scores; i++){
    fprintf(file, "%lf, %lf, %lld;", scores[i].x, scores[i].y, scores[i].score);
  }
  fclose(file);
}
