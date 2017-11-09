/*

This implements the CSC projection, see here: http://www.atnf.csiro.au/people/mcalabre/WCS/ccs.pdf (refered to as COBE document from now-on). There's a ruby implementation here: https://github.com/cix/QuadSphere/tree/master/lib/quad_sphere


 */



/*
This holds the face (0 - 5), chi, and psi
 */
typedef struct TangentialInfo TangentialInfo;
struct TangentialInfo{
  char face;
  double chi;
  double psi;
  double phi_c;
  double theta_c;
};
typedef struct CSCInfo CSCInfo;
struct CSCInfo{
  char face;
  double x;
  double y;
};


TangentialInfo computeTangentialInfo(double phi, double theta);

CSCInfo computeCSCInfo(TangentialInfo info);
