#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void writeFENToFile(int men);
void writeIterations(string chosenPieces[], int numPieces, int men, string[8][8], ofstream*);
void recurse_helper(string,string);
void recurse(string);

int main() {
    //abcdef
    //which include the word cab
    writeFENToFile(3);
    return 0;
}

void writeFENToFile(int men) {
    //number of possible pieces
    int numPieces = 6;
    
    //all possibilities of pieces
    string possiblePiecesWhite[] = {
        "K", "P", "N", "B", "R", "Q"
    };
    
    string possiblePiecesBlack[] = {
        "k","p", "n", "b", "r", "q"
    };
    
    //currently only made for 3
    string chosenPiecesThree[3];
    
    //choosing kings
    chosenPiecesThree[0] = "K";
    chosenPiecesThree[1] = "k";
    int curPosThree = 2;
    
   ofstream* file = new ofstream("data.txt");
    
    //finding possible pieces for 3 men
    for (int i = 1; i < numPieces; i++) {
        string isFilled[8][8];
        chosenPiecesThree[curPosThree] = possiblePiecesWhite[i];
        writeIterations(chosenPiecesThree, men, men, isFilled, file);
    }
    
    
}


void writeIterations(string chosenPieces[], int numPiecesLeft, int numPieces, string isFilled[8][8], ofstream* file) {
    if (numPiecesLeft == 0)
    {
        string final = "";
        for (int i = 0; i < 8; i++) {
            int curCounter = 0;
            for (int j = 0; j < 8; j++) {
                if (isFilled[i][j] != "") {
                    if(curCounter != 0) {
                        final += to_string(curCounter);
                        final += isFilled[i][j];
                        curCounter = 0;
                    }
                    
                    else {
                        final += isFilled[i][j];
                    }
                }
                
                else if (j == 7) {
                    curCounter++;
                    if(curCounter != 0) {
                        final += to_string(curCounter);
                    }
                }
                
                else {
                    curCounter++;
                }
            }
            
            if (i != 7) {
                final += "/";
            }
            
            
        }
        
        *file<<final<<endl;
        return;
    }
    
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j<8; j++) {
            
            if (isFilled[i][j] != "") {
            continue;
            }
        
            isFilled[i][j] = chosenPieces[numPieces-numPiecesLeft];
        
            writeIterations(chosenPieces, numPiecesLeft-1, numPieces, isFilled, file);
        
            isFilled[i][j] = "";
        }
        
    }
    
    

    
    
    
    
    
}