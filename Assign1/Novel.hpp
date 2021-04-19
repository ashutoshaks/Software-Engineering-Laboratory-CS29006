#ifndef NOVEL_H
#define NOVEL_H

#include "Book.hpp"
typedef vector<string> paragraph;

// A chapter has a number, a name and many paragraphs
// A paragraph is implemented as a vector of strings 
class Chapter
{
public:
    int chapNo;
    string chapName;
    vector<paragraph> paragraphs;
};

// A novel is a vector of chapters
class Novel : public Book
{
private:
    vector<Chapter> chapters; 
    
public:
    Novel(const string &filename_, const string &fullFileName_);
    void parseBook();
    void query();
};

#endif