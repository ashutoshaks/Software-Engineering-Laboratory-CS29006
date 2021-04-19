#include "Book.hpp"

Book::Book(const string &filename_, const string &fullFileName_, const string &type_) : fileName(filename_), fullFileName(fullFileName_), type(type_)
{}

Book::~Book()
{}

// Standard get functions
string Book::getFileName()
{
    return fileName;
}

string Book::getFullFileName()
{
    return fullFileName;
}

string Book::getType()
{
    return type;
}

string Book::getTitle()
{
    return title;
}

string Book::getAuthor()
{
    return author;
}

string Book::getReleaseDate()
{
    return releaseDate;
}

string Book::getLanguage()
{
    return language;
}

// Function to display the contents of the book line-by-line, 50 lines at a time
void Book::displayBook()
{
    ifstream myfile(fullFileName);
    cout << "\n*** DISPLAYING CONTENTS OF THE SELECTED BOOK ***\n\n";
    string line;
    string headerEnd = "START OF THIS PROJECT GUTENBERG EBOOK";
    int lno = 0, choice;
    bool found = 0;
    while(getline(myfile, line))
    {
        if(!found)
        {
            if(line.find(headerEnd) != string::npos)
                found = 1;
            continue;
        }
        cout << line << endl;
        lno++;
        if(lno % 50 == 0)
        {
            cout << "\n\nDo you want to view more? Enter 1 to continue or 0 to quit:\n";
            cin >> choice;
            while(choice != 1 && choice != 0)
            {
                cout << "Invalid choice! Please enter your choice again:\n";
                cin >> choice;
            }
            if(!choice)
                break;
            cout << endl;
        }
    }
    myfile.close();
    cout << "\n*** FINISHED DISPLAYING CONTENTS OF THE BOOK ***\n\n";
}

// Function to parse the header
// It extracts the title, author's name, release date and language
void Book::parseHeader()
{
    string headerEnd = "START OF THIS PROJECT GUTENBERG EBOOK"; // signifies end of the header, no need to parse after this
    string title_ = "Title:";
    string author_ = "Author:";
    string releaseDate_ = "Release Date:";
    string language_ = "Language:";

    ifstream myfile(fullFileName);
    string line, s;
    while(getline(myfile, line))
    {
        if(line.find(title_) == 0)
            this -> title = line.substr(title_.length() + 1);
        else if(line.find(author_) == 0)
            this -> author = line.substr(author_.length() + 1);
        else if(line.find(releaseDate_) == 0)
            this -> releaseDate = line.substr(releaseDate_.length() + 1);
        else if(line.find(language_) == 0)
            this -> language = line.substr(language_.length() + 1);
        else if(line.find(headerEnd) != string::npos)
            break;
    }
    myfile.close();
}