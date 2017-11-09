#include "qsc.h"
#include<stdio.h>
#include<proj_api.h>
#include <stddef.h>
#include <stdint.h>
#include<math.h>
/*
This uses the proj4 API to convert latitude and longitude into y, x, respectively. This changes the latitudes and longitudes array!


latitudes and longitudes should be in degrees. 
*/
void forwardProjection(double* latitudes, double* longitudes, size_t num_coordinates, CubeSide face){

  projPJ qsc;
  projPJ latlong;
  char* qsc_command;
  
  switch(face){
  case FRONT: qsc_command = "+proj=qsc +ellps=WGS84 +units=m +lat_0=0 +lon_0=0"; break;
  case RIGHT: qsc_command = "+proj=qsc +ellps=WGS84 +lat_0=0 +lon_0=90"; break;
  case BACK: qsc_command = "+proj=qsc +ellps=WGS84 +lat_0=0 +lon_0=180"; break;
  case LEFT: qsc_command = "+proj=qsc +ellps=WGS84 +lat_0=0 +lon_0=-90"; break;
  case TOP: qsc_command = "+proj=qsc +ellps=WGS84 +lat_0=90"; break;
  case BOTTOM: qsc_command = "+proj=qsc +ellps=WGS84 +lat_0=-90"; break;
  }
  if(!(qsc = pj_init_plus(qsc_command))){
    exit(1);
  }
  if(!(latlong = pj_init_plus("+proj=latlong +ellps=WGS84"))){
    exit(1);
  }
  size_t i;
  /* We need to convert degrees to radians */
  for(i = 0; i < num_coordinates; i++){
    latitudes[i] = latitudes[i]*DEG_TO_RAD;
    longitudes[i] = longitudes[i]*DEG_TO_RAD;
  }
  int p = pj_transform(latlong, qsc, num_coordinates, 1, longitudes, latitudes, NULL);
}

/*Both longitude and latitude are in degrees */
CubeSide computeCubeSide(double longitude, double latitude){
  /* See page 23 of this PDF: http://www.atnf.csiro.au/people/mcalabre/WCS/ccs.pdf


     I'm pretty sure that equations 160 (for l, m, and n) use theta as latitude. 
     My reasoning is this: Suppose theta is longitude. Assume that the "front" face has center longitude 0. Then the back face would have center longitude 180. None of the faces in table 4 have a theta_c of 180, so theta cannot be longitude. Therefore, theta is latitude.

Just a note, that I found out later: according to this: https://en.wikipedia.org/wiki/N-vector, l,m and n form the n-vector.
   */
  double lat_rad = DEG_TO_RAD*latitude;
  double lon_rad = DEG_TO_RAD*longitude;
  double l = cos(lat_rad)*cos(lon_rad);
  double m  =cos(lat_rad)*sin(lon_rad);
  double n= sin(lat_rad);
  double zetas[6] = {n, l, m, -1*l, -1*m, -1*n};
  char i = 0;
  double max_zeta = zetas[0];
  char face = 0; 
  for(i = 1; i < 6; i++){
    if(zetas[i] > max_zeta){
      face = i;
      max_zeta = zetas[i];
    }
  }
  CubeSide side;
  switch(face){
  case 1: side = FRONT; break;
  case 0: side = TOP; break;
  case 5: side = BOTTOM; break;
  case 2: side = RIGHT; break;
  case 3: side = BACK; break;
  case 4: side = LEFT; break;
  }
  return side;

}

int main(int argc, char *argv[]){
  double latitudes[] = {37};
  double longitudes[] = {45};
  CubeSide side= computeCubeSide(longitudes[0], latitudes[0]);
  printf("%d\n", side);
  forwardProjection(latitudes, longitudes, 1, FRONT);
  printf("%.2f\t%.2f\n", latitudes[0], longitudes[0]);
}

