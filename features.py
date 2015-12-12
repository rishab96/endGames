# !/usr/bin/env python

import numpy as np
import chess


# board is a 2d grid.
#

# useful method.

def manhattanDistance( xy1, xy2 ):
  "Returns the Manhattan distance between points xy1 and xy2"
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )



def getNumber(row, column):
    return row*8 + column

def getRowAndColumn(num):
    
    row = num / 8
    column = num % 8
    return row,column

def getPiece(board, piece, color):
    
    results = []
    A = board.pieces(piece, color)
    for x in A:
        results.append(x)
    return results

def getPieceCoOrd(board, piece, color):

    res = getPiece(board, piece, color) 
         
    if len(res) != 0:
        num = res[0]
    else:
        return None
   
    row_k, col_k = getRowAndColumn(num)
    
    return row_k, col_k

# NEED TO CONSIDER THE EDGE CASE WHEN THE KING IS TOO FAR AHEAD,
# AND BLACK KING CAN MAYBE CATCH THE PAWN?


#### Features below:

## checks if after changing n+1,n-1
# etc, the new n should be somewhere
# around the old n.
# It could either go out of the board,
# or on the corner column - both are bad.

def outofRange(n):

    if n > 63 or n < 0:
        return True
    
    edge = n % 8
    if edge == 7 or edge == 0:
        return True

    return False

# will check if the white king can reach n or not.
# white king will only be able to reach n if it is
# attacking that, and the black king isn't.
# Just for KPvsk endgames

def canDefend(board, n):
    
    black_attack = board.is_attacked_by(chess.BLACK, n)
    white_attack = board.is_attacked_by(chess.WHITE, n) 
    
    if white_attack and not black_attack:
        return True
    
    return False

# Might test by increasing the feature value for black can capture/
def canBeCaptured_helper(board):
    


    # We know it's only one so far, so don't have to do anymore.
    move = board.turn == chess.WHITE
    

    # P is the position number of the pawn.
    P = getPiece(board,chess.PAWN, chess.WHITE)[0]
    black_attack = board.is_attacked_by(chess.BLACK, P)
    
    # if P is in the 2nd rank, then return False.
    
    if P <= 15:
        return False



    # just to reduce cases we need to check
    if not black_attack:
        return False

    white_attack = board.is_attacked_by(chess.WHITE, P) 
    
    if not move:
        if black_attack and not white_attack:
            return True

    else:
        # just make each case separately:
        
        # start from row above and then cover all three rows.
        N = P + 8
        for i in range(3):
            
            left = N - 1
            mid = N # Don't have to check this because no case when this will be accessible and others wont be.
            right = N + 1
            
            if not outofRange(left) and canDefend(board, left):
                return False
            
            if not outofRange(right) and canDefend(board, right):
                return False
    
            N -= 8

        # I guess second condition is redundant because if it were
        # true, then would have returned false already
        if black_attack and not white_attack:
            return True
        

def canBeCaptured(board):
    
    # We know it's only one so far, so don't have to do anymore.
    A = {}
    if canBeCaptured_helper(board):
        A['black_can_capture'] = 1
    
    return A

def isWhiteKingAhead(board):
   
    A = {}
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    if row_K > row_p:
        if abs(col_K - col_p) <= 1:
            A['white king ahead'] = 1
    
#    elif row_K < row_p:


    return A

def ishPawn(board):
    
    A = {}
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    if col_p == 7 or col_p == 0:
        A['h_pawn'] = 1

    return A

# needs to return who has the opposition as well.
# tupe - (true, BLACK)

def isOpposition(board):
    
    A = {}
    move = board.turn == chess.WHITE
    
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    pawn_can_move = False
    pawnMoves = board.generate_legal_moves(king=False)
    
    for x in pawnMoves:
        pawn_can_move = True

  #  K = (row_K, col_K) 
  #  P = (row_p, col_p)
  #  kingDistance(K, P)

    if row_p > row_K:
        return A

    if col_K == col_k:
        if row_K == row_k - 2:
            if move:
                if pawn_can_move:
                    A['white_opposition'] = 1
                else:
                    if row_p <= 4:
                        A['black_opposition'] = 1
            else:
                A['white_opposition'] = 1

    return A

## Need to decide whether we should keep minimum column 
# distance = 2 or not.

def wrongSide(board):
    
    A = {}

    K = getPieceCoOrd(board, chess.KING, chess.WHITE)         
    k = getPieceCoOrd(board, chess.KING, chess.BLACK) 
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    # K[1] is the column.
    
    # both on same side of the pawn:
    if K[1] > P[1] and k[1] > P[1]:
        
        # K[1] < k[1] means white king is closer.
        




        if K[1] < k[1]:
            
            A['black_king_wrong_side'] = 1

        elif K[1] > k[1]:

            A['white_king_wrong_side'] = 1
            
            if abs(K[0] - k[0]) <= 1:

                A['white_king_blocked'] = 1
    
   
    elif K[1] < P[1] and k[1] < P[1]:
        
        if K[1] < k[1]:

            A['white_king_wrong_side'] = 1
            
            if abs(K[0] - k[0]) <= 1:

                A['white_king_blocked_side'] = 1
                
        elif K[1] > k[1]:
            
            A['black_king_wrong_side'] = 1
     
    ## time to check the rows:
    # if black king is blocking the white king via
    # rows:
    
    if K[0] > P[0] and k[0] > P[0]:

        # if black king is blocking the white king:

        if abs(k[1] - P[1]) <= abs(K[1] - P[1]):

            if k[0] < K[0]:

                A['white_king_blocked_down'] = 1


#    if K[0] < P[0] and k[0] > P[0]:
#        A['white_king_behind'] = 1
#    elif K[0] > P[0] and k[0] < P[0]:
#        A['white_king_ahead'] = 1



    return A

## returns the dist k-P - K-P.
# So if it's positive, then it's a good thing for us, 
# while if it's negative, that's a bad thing.
# Weights should figure that out hopefully.

## Also, deal with pawn on 6th rank here.

# helper function, closer to winning square:
# Meh, make it later.

def move_distances(board):
    
    A = {}

    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    if row_P >= 5:
        if abs(col_K - col_P) <= 1:
            if row_K == row_P+1:
                A['white winning setup'] = 1


    # because the key square in this fight is the square right above the pawn.
    # Do we really need to do error checking for this?!
    row_P += 1


    assert(row_P != None)
    
    




    K1 = abs(row_K - row_P) 
    K2 = abs(col_K - col_P)
    K_d = max(K1, K2)

    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_d = max(k1, k2)
    
    if move:
        K_d -= 1
    else:
        k_d -= 1

    # less than equal to because if they both reach it at same time,
    # I guess we should consider white king closer?!
    
    ## Maybe should give this greater value?

    if K_d <= k_d:
        
        A['white_king_closer'] = 1

        

    else:

        A['black_king_closer'] = 1
    
    # Winning squares right above:

    col_P -= 1
    
    # so it's not an illegal square
    if col_P < 8 or col_P >= 0:
        
        ## A lot of repeated shit here:

        K1 = abs(row_K - row_P) 
        K2 = abs(col_K - col_P)
        K_d = max(K1, K2)

        k1 = abs(row_k - row_P) 
        k2 = abs(col_k - col_P)
        k_d = max(k1, k2)
        
        if move:
            K_d -= 1
        else:
            k_d -= 1

        # less than equal to because if they both reach it at same time,
        # I guess we should consider white king closer?!
        
        # Adding a return here, because then we don't even need to check the rest/.    
        if K_d <= k_d:
            
            A['white_king_closer_to_winning_square'] = 1
            return A

        else:

            A['black_king_closer_to_winning_square'] = 1



    # Winning square on the other side:

    col_P += 2
    
    # SHould really DECOMPOSE THIS IF I WASN"T AN IDIOT>
    # so it's not an illegal square

    if col_P < 8 or col_P >= 0:
        
        ## A lot of repeated shit here:

        K1 = abs(row_K - row_P) 
        K2 = abs(col_K - col_P)
        K_d = max(K1, K2)

        k1 = abs(row_k - row_P) 
        k2 = abs(col_k - col_P)
        k_d = max(k1, k2)
        
        if move:
            K_d -= 1
        else:
            k_d -= 1

        # less than equal to because if they both reach it at same time,
        # I guess we should consider white king closer?!

        if K_d <= k_d:
            
            A['white_king_closer_to_winning_square'] = 1

        else:

            A['black_king_closer_to_winning_square'] = 1
    
    return A
    


def canCatchPawn_helper(board):
    
    # getPieces, then find the co-ordinates
    # of those pieces.
    #
    
    # move should be true or false;
    move = board.turn == chess.WHITE
    res = getPiece(board, chess.KING, chess.BLACK) 
    


    if len(res) != 0:
        num = res[0]

    
    row_k, col_k = getRowAndColumn(num)

    res2 = getPiece(board, chess.PAWN, chess.WHITE)

    if len(res2) != 0:
        num = res2[0]
    
    row_p, col_p = getRowAndColumn(num)
    
    # so we deal with the pawn being on the 2nd rank.
    if row_p == 1:
        row_p += 1

    if row_k < row_p:

        if move:
            return False
        if row_p - row_k > 1:
            return False
    

    moves_to_end = 7 - row_p
    moves_to_catch = abs(col_p - col_k) - 1

    if moves_to_end < moves_to_catch:
        return False

    if moves_to_end == moves_to_catch:
        if move:
            return False

    return True
    
def canCatchPawn(board):
    A = {}
    if canCatchPawn_helper(board):
        A['can catch pawn'] = 1
    else:
        A['cant catch pawn'] = 1
    
    return A



