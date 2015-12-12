# !/usr/bin/env python

import numpy as np
import chess

import targetedCalculation
from targetedCalculation import *

import helperMethods
from helperMethods import *

# defining globals:

# will change their values in the main function for features.

ROOK = [0,0]
rook = [7,7]
KING = [5,5]
king = [0,0]
PAWN = [0,0]

ADVANCED_PAWN = False
SHORT_SIDE = False
WHITE_KING_CLOSE = False
LONG_SIDE_COL = 0
SHORT_SIDE_COL = 0

CUT_OFF = 0


# Can add a whole bunch of smaller methods.
# Major method to add possibly <---> checkPerpetual.
#



def getRookFeatures(board):
    
    A = {}
    
    # just because I'm stupid and don't want to deal with classes.
    global ROOK, rook, PAWN, KING, king, ADVANCED_PAWN
    ROOK =  getPieceCoOrd(board, chess.ROOK, chess.WHITE)
    rook = getPieceCoOrd(board, chess.ROOK, chess.BLACK)
    PAWN = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    KING = getPieceCoOrd(board, chess.KING, chess.WHITE)
    king = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    cut = cutoff(board)
    A.update(cut)
    
    ADVANCED_PAWN = PAWN[0] > 3
    A['advanced pawn'] = 1
    
    
    
    dist = distances(board)
    A.update(dist)
    p = pawnType(board)
    A.update(p)
    
    print A
    return A

# assume the board is not the same
# as the original.




def canBlackKingImprove(board):
    
    ## get the three squares that the king
    ## can go to, to get closer to the pawn.
    # Then check if they are attacked or not.
    
    # col + i, and row, row+1, row-1 are the
    # key squares.
    # i ==> +1 if pawn on right
    # i -- -1 if pawn on left.
    #
    
    new_k = [0, 0]
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    if P[1] > k[1]:
        new_k[0] = k[0]
        new_k[1] = k[1] + 1
    
    else:
        
        new_k[0] = k[0]
        new_k[1] = k[1] - 1

print 'checking cutoff'
    print k
    print new_k
    
    # converts row-col thing into num.
    squares = []
    sq1 = getNumber(new_k[0], new_k[1])
    squares.append(sq1)
    squares.append(sq1 + 8)
    squares.append(sq1 - 8)
    
    for sq in squares:
        if sq < 63 and sq > 0:
            white_attack = board.is_attacked_by(chess.WHITE, sq)
            if not white_attack:
                return True
    
    return False

# checks if the square right above the pawn is attacked,
# by whome etc/

def canPushPawn(board):
    pass




def cutoff(board):
    
    
    A = {}
    global CUT_OFF
    
    # cutoffs don't quite make sense if white king is too far
    # away.
    # If I wouldn't be lazy, will try to check if both kings on same
    # side, then cut off might be useless too.
    
    if not WHITE_KING_CLOSE:
        return A

    move = board.turn == chess.WHITE

    ## don't use the globals because this method
    # is being recursively called.

P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    
    cur_cutoff = abs(k[1] - P[1])
    
    if cur_cutoff > 1:
        
        if not canBlackKingImprove(board):
            
            print 'black cant improve'
            A['cut off'] = 1
            CUT_OFF = cur_cutoff
            return A
    
        if move:
            print 'trying every move now'
            moves = board.generate_legal_moves()
            for m in moves:
                b2 = createNewBoard(board)
                b2.push(m)
                if not canBlackKingImprove(b2):
                    
                    print 'black cant improve'
                    A['cut off' + str(cur_cutoff)] = 1
                    CUT_OFF = cur_cutoff
                    return A
        
        # being lazy here...IDEALLY, should move the best
        # move for black, and then call this whole thing
        # again.
        
        else:
            print 'black to play'
            king_moves = board.generate_legal_moves(king=True)
            for m in king_moves:
                b2 = createNewBoard(board)
                b2.push(m)
                
                k2 = getPieceCoOrd(b2, chess.KING, chess.BLACK)
                
                if abs(k2[1] - P[1]) < cur_cutoff:
                    
                    return cutoff(b2)


# if it comes up to this point, then no cutoff was found.

A['no cutoff'] = 1
    CUT_OFF = 0
    
    
    return A







# Might want to refine it a bit more etc,
# but this is very general.
def distances(board):
    
    print 'checking cutOFF'
    print CUT_OFF
    
    global SHORT_SIDE, WHITE_KING_CLOSE, LONG_SIDE_COL, SHORT_SIDE_COL
    A = {}
    KP = kingDistance(KING, PAWN)
    kP = kingDistance(king, PAWN)
    # we just care about how close the black king is to the file
    # of the pawn.
    kP = abs(king[1] - PAWN[1])
    
    if KP <= 2:
        WHITE_KING_CLOSE = True
    
    if KP >= 2:
        A['White king 2D away from pawn'] = 1
    
    if KP >= 4:
        if not ADVANCED_PAWN:
            A['White king really fucking far away'] = 1
        else:
            if kP >= 4:
                A['both kings really fucking far'] = 1
            else:
                A['White king really fucking far away'] = 1


if KP - kP > 1:
    A['Black king is clearly closer than white king'] = 1
    
    ## special case when it can be kicked away soon?!
    
    #   black_close = abs(king[1] - PAWN[1]) <= 1
    if kP <= 1:
        A['Black king caught pawn'] = 1


# check for king being on short side or long:
#
# For the rook being on long or short side, we should possibly
# right another method that checks if we can take it or not.

else:
    
    if PAWN[1] > 3:
        LONG_SIDE_COL = 0
            SHORT_SIDE_COL = 7
            if king[1] > PAWN[1]:
                A['b king short side'] = 1
                SHORT_SIDE = True
        else:
            A['b king long side'] = 1
                SHORT_SIDE = False
        else:
            LONG_SIDE_COL = 7
            SHORT_SIDE_COL = 0
            if king[1] < PAWN[1]:
                A['b king short side'] = 1
                SHORT_SIDE = True
                if rook[1] == 7:
                    A['b king short side, rook h-file'] = 1
            else:
                A['b king long side'] = 1
                SHORT_SIDE = False

kside = 7 - PAWN[1]
    qside = PAWN[1]
    
    shortside = min(kside, qside)
    longside = max(kside, qside)
    
    if ADVANCED_PAWN and not SHORT_SIDE and WHITE_KING_CLOSE:
        A['b king long side + adv pawn' + str(shortside)] = 1
elif ADVANCED_PAWN and SHORTSIDE and WHITE_KING_CLOSE:
    A['b king short side + adv pawn' + str(longside)] = 1
        
        if king[1] == SHORT_SIDE_COL:
            A['b king last col'] = 1
        
        if PAWN[1] > 3:
            if rook[0] == LONG_SIDE_COL:
                A['nice defensive setup'] = 1
            elif ROOK[0] == LONG_SIDE_COL:
                A['nice white setup'] = 1


diff = PAWN[0] - rook[0]
    
    if diff < 0 and not ADVANCED_PAWN:
        A['rook ahead of pawn'] = 1
elif diff < 0 and ADVANCED_PAWN:
    A['black rook shitty placed'] = 1
    elif diff > 2 and ADVANCED_PAWN:
        A['black rook behind pawn'] = 1

# can add more conditions.
#

##### check about stuff like number of rook moves below a threshold?



return A


def pawnType(board):
    
    A = {}
    c = PAWN[1]
    
    if c == 0 or c == 7:
        A['rook pawn'] = 1
    elif c == 1 or c == 6:
        
        A['knight pawn'] = 1
    elif c == 2 or c == 5:
        
        A['bishop pawn'] = 1
    elif c == 3 or c == 4:
        
        A['center pawn'] = 1
    
    # just a separate feature for how advanced.
    if ADVANCED_PAWN:
        A[str(PAWN[0])] = 1
    
    
    
    return A


def cutOff(board):
    
    A = {}
    if not WHITE_KING_CLOSE:
        return A









def checks(board):
    
    pass
