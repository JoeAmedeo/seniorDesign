swig -python compute.i
gcc -c -g -fpic computemodule.c compute_wrap.c -I/usr/include/python3.6m
gcc -shared computemodule.o compute_wrap.o -lgsl -lcblas -lpthread -o _compute.so
