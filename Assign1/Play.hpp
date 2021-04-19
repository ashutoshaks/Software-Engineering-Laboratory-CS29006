#ifndef PLAY_H
#define PLAY_H

#include "Book.hpp"
typedef set<string> scene; 

// A play is stored as a vector of scenes
// Each scene is a set of strings which contains all the characters present in that scene
class Play : public Book
{
private: 
    vector<scene> scenes;
    
public:
    Play(const string &filename_, const string &fullFileName_);
    void parseBook();
    void query();
};

#endif