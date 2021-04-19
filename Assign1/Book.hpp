#ifndef BOOK_H
#define BOOK_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <algorithm>
#include <regex>
using namespace std;

class Book
{
protected:
    string fileName; // only the filename
    string fullFileName; // filename along with the path
    string type;
    string title;
    string author;
    string releaseDate;
    string language;

public:
    Book(const string &filename_, const string &fullFileName_, const string &type_);
    virtual ~Book();

    string getFileName();
    string getFullFileName();
    string getType();
    string getTitle();
    string getAuthor();
    string getReleaseDate();
    string getLanguage();
    void displayBook();
    void parseHeader();

    // These functions are overriden in Novel.cpp and Play.cpp
    virtual void parseBook(){};
    virtual void query(){};
};

#endif