This is the Final Project of CS221 by Rishab Mehra and Parimarjan Negi.

The goal is to solve chess end games as efficiently and accurately as possible. Chess Endgames can be solved with a 100% accuracy using Tablebases, but they require a lot of hard drive space (5 pieces itself requires several GBs of storage, while 6 piece endgames require over 1 TB). The goal is to achieve a 90%+ accuracy, using a feature extractor and simplified minimax. The accuracy of our program is tested using the output from the solved table bases.

Files and their functions:

1. userTest.py - This is the file a user can use to test individual chess board layouts and see what the actual outcome is of that board (whether its a winning board or a draw) and see what our feature extractor predicts about the board. This is the best way to test and see our complex features in action.

2. features.py/features2P.py/featuresRook.py - These files are the feature extractors for 3 piece, 4 piece and 5 piece end games respectively. They currently solve a single (yet one of the hardest) engame in each category. 3 piece solves KPvk. 4 piece solves KPvskp and 5 piece solves KPRvskp. There are helper files for these feature extractors, which include helperMethods.py (general helper methods), targettedCalculation.py (specialized minimax), and util.py (helper for stochastic gradient descent).

3. TestAndTrain.py - This file can be used to Test and Train weight vectors. The use SGD techniques using our feature extractors and the actual output from the tablebases to give weight vectors, which are then used in userTest.py. To see this is action import the 3 piece dataset data3.txt in the same folder as the code (and also four-men tablebases, which should already be there). Then you can test and see the output weight vector and error over the test set. For 3 pieces we generate and test all the positions. The 4 piece dataset could not be included as it is over the size limit - 350 mb for all positions and 35 mb for 1/10th positions, which we used as our training set.

The ThreePieceTrain.py and FourPieceTrain.py are helper files for TestAndTrain.py

4. C++ - this includes a main.cpp, which is a simple recursive backtracking way of generating required datasets. Currently its calibered for generating 1/10th random positions for KPvskp endgames (a 35 mb file), but can be easily modified to generate any required dataset.