#include "Play.hpp"

Play::Play(const string &filename_, const string &fullFileName_) : Book(filename_, fullFileName_, "Play")
{}

// Function to parse the play to extract all characters in each scene
void Play::parseBook()
{
    ifstream myfile(fullFileName);
    string line;
    scene currScene;
    bool found = false;

    regex r("^[A-Z]+\\s{0,1}[A-Z]*\\.");
    while(getline(myfile, line))
    {
        if(line.substr(0, 5) == "SCENE")
        {
            found = 1;
            if(!currScene.empty())
            {
                scenes.push_back(currScene);
                currScene.clear();
            }
            continue;
        }
        if(!found)
            continue;

        auto words_begin = sregex_iterator(line.begin(), line.end(), r);
        auto words_end = sregex_iterator();
        for(auto it = words_begin; it != words_end; it++)
        {
            smatch m = *it;
            string character = m.str();
            currScene.insert(character.substr(0, character.length() - 1));
        }
    }
    if(!currScene.empty())
    {
        scenes.push_back(currScene);
        currScene.clear();
    }
}

// Function to perform the required query
void Play::query()
{
    string charName;
    cout << "\nEnter the name of a character:\n";
    cin >> charName;
    transform(charName.begin(), charName.end(), charName.begin(), ::toupper);
    scene characterSet;
    for(auto currScene : scenes)
    {
        if(currScene.count(charName))
            characterSet.insert(currScene.begin(), currScene.end());
    }
    if(characterSet.empty())
        cout << "\n*** NO CHARACTERS APPEAR WITH THIS CHARACTER IN ANY SCENE ***\n\n";
    else
    {
        cout << "\n*** DISPLAYING CHARACTERS APPEARING WITH THE GIVEN CHARACTER IN ATLEAST ONE SCENE ***\n\n";
        characterSet.erase(charName);
        for(auto character : characterSet)
            cout << character << endl;
        cout << "\n*** ALL APPROPRIATE CHARACTERS DISPLAYED ***\n\n";
    }  
}