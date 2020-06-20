project : test.o heap.o manager.o
	cc test.o heap.o manager.o -o project
manager.o : manager.c manager.h
	cc -c manager.c -Wall
heap.o : heap.c heap.h manager.h
	cc -c heap.c -Wall
test.o : test.c heap.h
	cc -c test.c -Wall

