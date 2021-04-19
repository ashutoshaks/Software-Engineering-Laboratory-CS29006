#include "Book.hpp"
#include "Novel.hpp"
#include "Play.hpp"

#include <dirent.h>
#include <sys/types.h>
using namespace std;

// Function to check if a string ends with another given string
bool endsWith(const string &fullString, const string &ending)
{
    if (fullString.length() >= ending.length())
        return (fullString.substr(fullString.length() - ending.length(), ending.length()) == ending);
    else
        return false;
}

// Function to check if a string is a substring of another (case-insensitive)
bool searchSubstr(string str, string searchStr)
{
    transform(str.begin(), str.end(), str.begin(), ::tolower);
    transform(searchStr.begin(), searchStr.end(), searchStr.begin(), ::tolower);
    return (str.find(searchStr) != string::npos);
} 

// Function to display all books present
map<int, int> listAllBooks(const vector<Book*> bookList)
{
    map<int, int> index;
    int i;
    if(bookList.empty())
    {
        cout << "\n*** NO BOOKS ARE CURRENTLY PRESENT ***\n\n";
        exit(1);
    }
    cout << "\n*** DISPLAYING ALL BOOKS ***\n\n";
    for(i = 0; i < (int)bookList.size(); i++)
    {
        index[i + 1] = i;
        cout << i + 1 << ". Filename - " << bookList[i] -> getFileName() << endl;
        cout << "   Title - " << bookList[i] -> getTitle() << endl;
        cout << "   Author's Name - " << bookList[i] -> getAuthor() << endl;
        cout << endl;
    }
    cout << "*** ALL BOOKS DISPLAYED ***\n\n";
    return index;
}

// Function to search for a book based on title or author's name
map<int, int> searchBook(const vector<Book*> bookList)
{
    int i, choice, nos = 1, id;
    cout << "\nEnter 1 to search by title, and 2 to search by author's name:\n";
    cin >> choice;
    while(choice != 1 && choice != 2)
    {
        cout << "Invalid choice! Please enter your choice again:\n";
        cin >> choice;
    }
    string searchStr;
    if(choice == 1)
        cout << "\nEnter title to be searched:\n";
    else
        cout << "\nEnter author's name to be searched:\n";
    cin >> searchStr;
    map<int, int> index;
    for(i = 0; i < (int)bookList.size(); i++)
    {
        if(choice == 1)
        {
            if(searchSubstr(bookList[i] -> getTitle(), searchStr))
                index[nos++] = i;
        }
        else
        {
            if(searchSubstr(bookList[i] -> getAuthor(), searchStr))
                index[nos++] = i;
        }
    }
    
    if(index.empty())
    {
        cout << "\n*** NO MATCHES FOUND ***\n";
        return index;
    }
    cout << "\n*** DISPLAYING FOUND MATCHES ***\n\n";
    for(auto val : index)
    {
        id = val.second;
        cout << val.first << ". Filename - " << bookList[id] -> getFileName() << endl;
        cout << "   Title - " << bookList[id] -> getTitle() << endl;
        cout << "   Author's Name - " << bookList[id] -> getAuthor() << endl;
        cout << endl;
    }
    cout << "*** ALL MATCHES DISPLAYED ***\n\n";
    return index;
}

// Function to implement use case 3 to perform queries
void useCase3(Book *bookPtr)
{
    int choice = 1;
    bookPtr -> parseBook();
    while(choice)
    {
        cout << "Do you want to perform a query? Enter 1 to proceed or 0 to exit:\n";
        cin >> choice;
        while(choice != 0 && choice != 1)
        {
            cout << "Invalid choice! Please enter your choice again:\n";
            cin >> choice;
        }
        if(choice == 0)
            return;
        bookPtr -> query();
    }
}

// Function to implement various parts of use case 2
void useCase2(const vector<Book*> bookList)
{
    int choice = 1, id, c;
    map<int, int> index;
    while(choice)
    {
        cout << "\nEnter 1 to display all books, 2 to search a book by title or author's name, or 0 to exit:\n";
        cin >> choice;
        while(choice < 0 || choice > 2)
        {
            cout << "Invalid choice! Please enter your choice again:\n";
            cin >> choice;
        }
        if(choice == 0)
        {
            cout << "\n*** THANK YOU ***\n\n";
            exit(0);
        }
        else if(choice == 1)
            index = listAllBooks(bookList);
        else
            index = searchBook(bookList);

        if(index.empty())
            continue;
        cout << "Enter a book index from this list which you want to select for displaying and querying:\n";
        cin >> id;
        while(id < 1 || id > (int)index.size())
        {
            cout << "Invalid index. Please enter the index again:\n";
            cin >> id;
        }

        cout << "\nDo you want to view the contents of the selected book? Enter 1 for YES, or 0 for NO:\n";
        cin >> c;
        while(c != 1 && c != 0)
        {
            cout << "Invalid choice! Please enter your choice again:\n";
            cin >> c;
        }
        if(c)
            bookList[index[id]] -> displayBook();
        else
            cout << endl;

        // Use Case 3
        useCase3(bookList[index[id]]);
    }
}

// Function to implement use case 1 - the directory and file management part
map<string, string> useCase1(const char *path)
{
    map<string, string> prevFiles, currFiles;
    ifstream infile("index.txt");
    string line, currName;
    int lno = 1, choice;
    if(infile.is_open())
    {
        while(getline(infile, line))
        {
            if(lno & 1)
                currName = line;
            else
                prevFiles[currName] = line;
            lno++;
        }
        infile.close();
    }
    else
    {
        cout << "\n*** UNABLE TO FIND THE \"index.txt\" FILE ***\n\n";
        exit(1);
    }

    struct dirent *entry;
    DIR *dir = opendir(path);
    if(dir == NULL)
    {
        cout << "\n*** NO SUCH DIRECTORY EXISTS ***\n\n";
        exit(1);
    }

    cout << "\n*** SCANNING THE DIRECTORY TO RETRIEVE ALL FILES ***\n";
    while ((entry = readdir(dir)) != NULL)
    {
        currName = entry -> d_name;
        if(!endsWith(currName, ".txt"))
            continue;
        if(prevFiles.count(currName))
            currFiles[currName] = prevFiles[currName];
        else
        {
            cout << "\n*** NEW FILE NAMED " << "\"" << currName << "\" HAS BEEN FOUND ***\n";
            cout << "Enter 1 if it is a Novel or 2 if it is a Play:\n";
            cin >> choice;
            while(choice != 1 && choice != 2)
            {
                cout << "Invalid choice! Please enter your choice again:\n";
                cin >> choice;
            }
            currFiles[currName] = ((choice == 1) ? "Novel" : "Play");
        }
    }
    closedir(dir);

    ofstream outfile("index.txt");
    for(auto files : currFiles)
        outfile << files.first << endl << files.second << endl;
    cout << "\n*** ALL FILES RETRIEVED AND index.txt UPDATED ***\n";
    return currFiles;
}

// Pass the directory where the books are present as a command line input
int main(int argc, char *argv[])
{
    // Use Case 1
    string path = argv[1], filename;
    map<string, string> currFiles = useCase1(argv[1]);
    vector<Book*> bookList;
    for(auto files : currFiles)
    {
        filename = files.first;
        if(files.second == "Novel")
            bookList.emplace_back(new Novel(filename, path + "/" + filename));
        else
            bookList.emplace_back(new Play(filename, path + "/" + filename));
    }
    int i;
    for(i = 0; i < (int)bookList.size(); i++)
        bookList[i] -> parseHeader();

    // Use Case 2
    useCase2(bookList);
}