CC = gcc
CFLAGS = -std=c99 -pedantic -Wall

qsc: qsc.c qsc.h
	${CC} ${CFLAGS} -o qsc qsc.c qsc.h -lm -lproj

clean:
	rm qsc
