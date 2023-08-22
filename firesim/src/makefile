# makefile for fireSim, a sample fire behavior simulator using fireLib
# Collin D. Bevins, October 1996
#

# The following rules work for UnixWare 2.0.
CC = cc
CFLAGS = -g -DNDEBUG
LIBS = -lm

fireSim: fireSim.o fireLib.o fireLib.h
	$(CC) $(CFLAGS) fireSim.c fireLib.c -o fireSim $(LIBS)

# End of makefile
