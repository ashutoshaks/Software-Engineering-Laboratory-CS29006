CC = g++ -std=c++11

lms: Book.o Novel.o Play.o Main.o
	$(CC) Book.o Novel.o Play.o Main.o -o lms

Book.o: Book.cpp
	$(CC) -c Book.cpp

Novel.o: Novel.cpp
	$(CC) -c Novel.cpp

Play.o: Play.cpp
	$(CC) -c Play.cpp

Main.o: Main.cpp
	$(CC) -c Main.cpp

clean: 
	rm *.o lms