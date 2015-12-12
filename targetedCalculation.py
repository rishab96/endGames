# !/usr/bin/env python

import numpy as np
import chess

import helperMethods
from helperMethods import *

# print flag.
pflag = False




# default depth = 5. Might want to try different values there.
def targetedCalculation(board, white_moves, black_moves, getScore, isEnd, depth=10):
    
    
    # if condition met, ie. won the pawn --> +10.
    # else -10?
    

    def V_opt(board, depth, visited_W):
    
        # create a new board before ever executing a legal new move.
        
        # will have conditions checking against the targets.
        if isEnd(board): 
            
            if pflag:
                print 'is End returned true'
            if pflag:
                print board
            return getScore(board)
            
        elif depth == 0:
            if pflag:
                print board
                print 'depth over'
            return getScore(board)
        
        # maximizing agent.
        # Generate the moves with the custom function.

        elif board.turn == chess.WHITE:
            
            # from this set, we need to consider only the situations that
            # have the least moves to target.
            scores = []
            
            # white_moves returns all the boards after the new moves.
            new_boards = white_moves(board)
            
         #   if pflag:
         #       print 'new options are'
         #       for b in new_boards:
         #           print b[0]

            for b2 in new_boards:
                # add this particular move to visited_W
                if b2[1] in visited_W:
                    continue

                if pflag:
                    print(b2[0])
                visited_W.append(b2[1]) 
             #   scores.append(V_opt(b2[0], depth, list(visited_W)))
                score = V_opt(b2[0], depth, list(visited_W))
                if score > 0:
                    return score
                

                ## dunno if i should do this or not --- fucking annoying.
                ## Important --> only need it added for this path.
                # for the next move to start, we don't want this to be added?
                #newV = list(visited_W)
                #newV.append(b2[1]) 
                #scores.append(V_opt(b2[0], depth, newV))
            return -1
            
        # this part is irrelevant for now.
            if not len(scores) == 0:
                return max(scores)
            else:
                return -1
            

            
        # basically black's turn --> minimizing agent.
        
        else:
            
            scores = []
            
            # white_moves returns all the boards after the new moves.
            new_boards = black_moves(board)
            
            if len(new_boards) == 0:
                return 1

            for b2 in new_boards:
                # don't need to add visited for black.
                # At least not in king pawn endgames?
            #    if b2[1] in visited_W:
            #        continue
                # dunno if I should be doing this or not./     
            #    visited_W.append(b2[1]) 
                # check.
                if pflag:
                    print(b2[0])
                    print depth
           #     scores.append(V_opt(b2[0], depth-1, list(visited_W)))
                score = V_opt(b2[0], depth-1, list(visited_W))
                if score < 0:
                    return score

            return 1

            if not len(scores) == 0:
                return min(scores)
            else:
                return 1

            # all options:
#            A = []
#            scores = []
            # first check only legalMoves of the king.
#            legalMoves = board.generate_legal_moves(pawns=False)
            
            # consider pawn moves first.
#            pawnMoves = board.generate_legal_moves(king=False, pawns=True)
#            for m in pawnMoves:
#                b2 = createNewBoard(board)
#                b2.push(m)
#                scores.append(V_opt(b2, depth, visited_W))
            
            
 #           for m in legalMoves:
 #               b2 = createNewBoard(board)
 #               b2.push(m)
                # add m-to the list of visited_W squares.
                # time to check if b2 improves the situation.
  #              A.append((b_heuristic(b2), b2))
            
 #           best_d = min(A)[0]
            
            # CHECK --- do I really want this for most cases?
            # adding relaxed_d considerably increases runtime here.
  #          relaxed_d = best_d

   #         for option in A:
    #            if option[0] <= relaxed_d:
    #                if pflag:
     #                   print option[1]
    #                    print depth
     #               scores.append(V_opt(option[1], depth-1, list(visited_W)))
            
            # consider all possible pawn moves.

           #     if improves(board, b2):
           #         A.append(V_opt(b2, depth-1))
             
   #         return min(scores)
    
    # just for the king squares --> so it doesn't repeat
    # in one particular branch of the recursion tree.
    
    # we care only about white not re-visiting squares.
    #
    # UPDATE DEPTH HERE: if K <--> p distance is more than 5, then 
    # depth = 5 is stupid. Also, check if it's king pawn endgame, only then.

    visited_W = []
    V = V_opt(board, depth, visited_W)
    return V
