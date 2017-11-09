#include "csc.h"
#include<math.h>

TangentialInfo computeTangentialInfo(double phi, double theta){
  /* We get the face number and chi and psi using procedure on page 1099
     from here: http://www.atnf.csiro.au/people/mcalabre/WCS/ccs.pdf (note: this is page 23 of the PDF itself). 

  */
  double l = cos(theta)*cos(phi);
  double m = cos(theta)*sin(phi);
  double n= sin(theta);
  double zetas[6] = {n, l, m, -1*l, -1*m, -1*n};
  double ksis[6] = {m, m, -1*l, -1*m, l, m};
  double etas[6] = {-1*l, n, n, n, n, l};
  double phi_cs[6] = {0, 0, 90.0, 180.0, 270.0, 0};
  double theta_cs[6] = {90.0, 0, 0, 0, 0, -90.0};
  char i = 0;
  double max_zeta = zetas[0];
  double ksi = ksis[0];
  double eta = etas[0];
  double phi_c = phi_cs[0];
  double theta_c = theta_cs[0];
  char face = 0; 
  for(i = 1; i < 6; i++){
    if(zetas[i] > max_zeta){
      face = i;
      max_zeta = zetas[i];
      ksi = ksis[i];
      eta = etas[i];
      phi_c = phi_cs[i];
      theta_c = theta_cs[i];
    }
  }
  TangentialInfo t_info;
  t_info.face = face;
  t_info.chi = ksi/max_zeta;
  t_info.psi = eta/max_zeta;
  t_info.phi_c = phi_c;
  t_info.theta_c = theta_c;
  return t_info;
  
}

CSCInfo computeCSCInfo(TangentialInfo info){
  /* Equation 172 of document: http://www.atnf.csiro.au/people/mcalabre/WCS/ccs.pdf*/
  
  
}
