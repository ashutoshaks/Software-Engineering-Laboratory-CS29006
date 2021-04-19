#include "Novel.hpp"

Novel::Novel(const string &filename_, const string &fullFileName_) : Book(filename_, fullFileName_, "Novel")
{}

// Function to parse the novel to extract chapter names, paragraphs, etc.
void Novel::parseBook()
{
    ifstream myfile(fullFileName);
    string line;
    bool found = 0;
    Chapter ch;
    int cnt = 1;
    paragraph currPara;

    while(getline(myfile, line))
    {
        if(line.substr(0, 7) == "CHAPTER")
        {
            if(found)
            {
                chapters.push_back(ch);
                ch.paragraphs.clear();
            }
            found = 1;
            ch.chapNo = cnt++;
            int ind = line.find('.') + 2;
            ch.chapName = line.substr(ind, line.length() - ind - 1);
            continue;
        }
        if(!found)
            continue;
        if(line == "")
        {
            ch.paragraphs.push_back(currPara);
            currPara.clear();
            continue;
        }
        currPara.push_back(line);
    }
    chapters.push_back(ch);
}

// Function to count the number of occurrences of a word in a sentence
int countMatches(string s, string word)
{
    stringstream cs(s);
    string str;
    int c = 0;
    while(getline(cs, str, ' '))
    {
        if (word == str) 
            c++;
        else if(str.back() == ',' ||str.back() == '.' || str.back() == ';' || str.back() == '?' || str.back() == '!')
        {
            if(str.substr(0, str.size() - 1) == word)
                c++;
        }
    }
    return c;
}

// Function to perform the required query
// Using a priority queue, we maintain the top-k chapters or paragraphs at any point of time
void Novel::query()
{
    string word, temp;
    int k, i, j, choice, count;
    cout << "\nEnter the word for which you want to find where it appears most number of times :\n";
    cin >> word;
    transform(word.begin(), word.end(), word.begin(), ::tolower);

    cout << "\nEnter the value of k for which you want to view top-k chapters / paragraphs :\n";
    cin >> k;
    cout << "\nTo view top-k chapters enter 1, else, to view top-k paragraphs enter 2 :\n";
    cin >> choice;
    while(choice != 1 && choice != 2)
    {
        cout << "Invalid choice! Please enter your choice again :\n";
        cin >> choice;
    }
    if(choice == 1) // for chapters
    {
        // For example, in pair<int, int> p, p.first is the numbr of occurences and p.second is the chapter number
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> topChapters;
        vector<pair<int, int>> topIds;
        for(i = 0; i < (int)chapters.size(); i++)
        {
            count = 0;
            for(paragraph currPara : chapters[i].paragraphs)
            {
                for(string s : currPara)
                {
                    temp = s;
                    transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
                    count += countMatches(temp, word);
                }
            }
            if((int)topChapters.size() < k || count > topChapters.top().first)
                topChapters.push({count, i});
            if((int)topChapters.size() > k)
                topChapters.pop();
        }

        while(!topChapters.empty())
        {
            if(topChapters.top().first != 0)
                topIds.push_back(topChapters.top());
            topChapters.pop();
        }
        int foundChaps = (int)topIds.size();
        if(foundChaps < k)
            cout << "\n*** SORRY, THERE ARE ONLY " << foundChaps << " CHAPTER(S) WITH THIS WORD ***\n";
        cout << "\n*** DISPLAYING THE TOP-" << foundChaps << " CHAPTERS ***\n\n";
        for(i = foundChaps - 1; i >= 0; i--)
        {
            cout << "*** NUMBER - " << (int)topIds.size() - i << " ***\n";
            cout << "*** CHAPTER " << chapters[topIds[i].second].chapNo << " - " << chapters[topIds[i].second].chapName << " ***\n";;
            cout << "*** NUMBER OF OCCURRENCES - " << topIds[i].first << " ***\n";
            cout << endl;
        }
        cout << "*** TOP-" << foundChaps << " CHAPTERS DISPLAYED ***\n\n";
    }

    else // for paragraphs
    {
        // For example, in pair<int, pair<int, int>> p, p.first is the numbr of occurences, p.second.first is the chapter number and p.second.second is the paragraph number
        priority_queue<pair<int, pair<int, int>>, vector<pair<int, pair<int, int>>>, greater<pair<int, pair<int, int>>>> topParagraphs;
        vector<pair<int, pair<int, int>>> topIds;
        for(i = 0; i < (int)chapters.size(); i++)
        {
            for(j = 0; j < (int)chapters[i].paragraphs.size(); j++)
            {
                count = 0;
                for(string s : chapters[i].paragraphs[j])
                {
                    temp = s;
                    transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
                    count += countMatches(temp, word);
                }
                if((int)topParagraphs.size() < k || count > topParagraphs.top().first)
                    topParagraphs.push({count, {i, j}});
                if((int)topParagraphs.size() > k)
                    topParagraphs.pop();
            }
        }

        while(!topParagraphs.empty())
        {
            if(topParagraphs.top().first != 0)
                topIds.push_back(topParagraphs.top());
            topParagraphs.pop();
        }
        int foundParas = (int)topIds.size();
        if(foundParas < k)
            cout << "\n*** SORRY, THERE ARE ONLY " << foundParas << " PARAGRAPH(S) WITH THIS WORD ***\n";
        cout << "\n*** DISPLAYING THE TOP-" << foundParas << " PARAGRAPHS ***\n\n";
        for(i = foundParas - 1; i >= 0; i--)
        {
            cout << "*** NUMBER - " << (int)topIds.size() - i << " ***\n";
            cout << "*** CHAPTER - " << topIds[i].second.first + 1 << ", PARAGRAPH - " << topIds[i].second.second + 1 << " ***\n";
            cout << "*** NUMBER OF OCCURRENCES - " << topIds[i].first << " ***\n\n";
            for(string s : chapters[topIds[i].second.first].paragraphs[topIds[i].second.second])
                cout << s << endl;
            cout << endl;
        }
        cout << "*** TOP-" << foundParas << " PARAGRAPHS DISPLAYED ***\n\n";
    }
}