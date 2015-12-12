# !/usr/bin/env python


import collections
from collections import Counter

import features
from features import *

import numpy as np
import chess

import targetedCalculation
from targetedCalculation import *

import helperMethods
from helperMethods import *

weight_vector_3_piece = {'black_king_closer_to_winning_square': -1.400000000000001, 'black_opposition': -1.9200000000000015, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.27, 'white_king_closer': 1.0700000000000007, 'white_king_closer_to_winning_square': -0.22000000000000008, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.04000000000000009, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.42000000000000015, 'black_king_wrong_side': 1.5400000000000011, 'white_king_blocked': -0.6000000000000003, 'white_king_wrong_side': -1.570000000000001, 'black_king_closer': -1.340000000000001, 'h_pawn': -2.6499999999999875}

## predictOutputOnly(board, numPieces)

# get scores we need:
#   sameFile --> above 5
#            --> below 5
#   adjacent
#   passed?!!



# Global variables we need:

debug = False

# bunch of globals whose value we set at the start.
# Should of course use classes for this, but I'm too stupid to use them
# properly, so just used this.

KING = [0,0]
king = [0,0]
PAWN = [0,0]
pawn = [0,0]

king_pawn_D = 0
king_PAWN_D = 0
KING_pawn_D = 0

ROW_DIFF = 0
COL_DIFF = 0

SAME_SIDE = True
KINGS_REVERSED = False
MOVE = True

#KING_PAWN_distance = 0

# Main wrapper function <--> which checks the board and then distributes the calls
# to either sameFile, passedPawns, or adjacent pawns.

def getFeatures2P(board):
    
    # set the global variables here:
    updateGlobals(board)

    A = {}
    
    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    # if pawns on the same file.
    
#    r_diff = row_p - row_P
#    c_diff = col_p - col_P
    
    if arePassedPawns(board):
        A = passedPawns(board)

    elif col_p == col_P and row_p > row_P:
        A = sameFilePawn(board)
     
    # if pawns on adjacent files --> don't need to
    # actually check for this as it's the only other
    # option.
    
    else:
        A = adjacentPawns(board)

    
    return A


def updateGlobals(board):

    global KING, king, PAWN, pawn, king_pawn_D, king_PAWN_D, KING_pawn_D, ROW_DIFF, COL_DIFF
    global SAME_SIDE, KINGS_REVERSED, MOVE

    MOVE = board.turn == chess.WHITE

    KING = getPieceCoOrd(board, chess.KING, chess.WHITE)
    king = getPieceCoOrd(board, chess.KING, chess.BLACK)

    pawn =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    PAWN =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    ROW_DIFF = pawn[0] - PAWN[0]
    COL_DIFF = pawn[1] - PAWN[1]
    
    # calculating distances:
    
    king_pawn_D = kingDistance(king, pawn)
    king_PAWN_D = kingDistance(king, PAWN)
    KING_pawn_D = kingDistance(KING, pawn)
    
    if KING[0] > king[0]:
        KINGS_REVERSED = True
    

    # calculating king-side:

    K = PAWN[1] - KING[1] 
    k = PAWN[1] - king[1]
    
    if K*k >= 0:
        SAME_SIDE = True
    else:
        SAME_SIDE = False

    move = board.turn == chess.WHITE
    

####### New Features:
####### Basic idea is to consider only if White can win or not --> and then flip
# boards, and consider it from black's side as well. This reduces the complexity
# of the methods considerably. 
# Divided into different type of situations <--> will need to add a layer on top
# which analyses the type of position and calls the appropriate method.

# Note: use board.fen to create the fen representation and then convert it back to 
# a board to create a new board --> so original board isn't affected.

##### Pawns on the same file features below. These methods should only be called
# if we've verified that the pawns are on the same file.

# Need to implement these.


def adjacent_isEnd(board):
    
    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    if p[0] == None:
        return True

    if P[0] == None:
        return True

    kp = kingDistance(k, p)
    kP = kingDistance(k, P)
    Kp = kingDistance(K, p)
    

    d = Kp - min(kp, kP)
    
    # just care about the drawing case.
    if d > 2:
        return True


    if kp == 1 or kP == 1:
        return True
    
    if arePassedPawns(board):
        return True

    # if we get two passed pawns here? Just enforce that you capture a pawn
    # evert time there is a chance.


### NEED TO USE THE 3-pieces feature + tester.

def adjacent_getScore(board):

    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    # just a pruning measure, not particularly imp:
    if p[0] == None and P[0] == None:
        kp = kingDistance(k, p)
        kP = kingDistance(k, P)
        Kp = kingDistance(K, p)

        d = Kp - min(kp, kP)
        if d > 2:
            return -1

# not sure if the same rule applies to draws or not.
#    if d < -2:
#        return 1
    
    if p[0] == None:
        return predictOutputOnly(board, 3)

    if P[0] == None:
        return -1
    
    kp = kingDistance(k, p)
    kP = kingDistance(k, P)

    if kp == 1 or kP == 1:
        return -1
    
    ## we just don't want them to ever become both passed pawns.
    
    if arePassedPawns(board):
        return -1

    return -1

def adjacent_white_moves(board):
    
    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
 
    # calculating current dist
    # if it's captured, then it's over, and this
    # shouldn't be called.
    Kp = kingDistance(K, p)
    
    moves = []

    pawnMoves = board.generate_legal_moves(king=False, pawns=True)
    
    for m in pawnMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        moves.append((b2, m)) 
    
    # remaining legal Moves
    legalMoves = board.generate_legal_moves(pawns=False) 
    
    # in visited_W, we don't append every legal move, but we
    # append only those that pass our heuristics.
    

    for m in legalMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        
        K2 = getPieceCoOrd(b2, chess.KING, chess.WHITE)
        # p remains the same since we're moving king here
        K2p = kingDistance(K2, p)
        # >= ?
        if K2p >= Kp:
            continue
        moves.append((b2, m))

    return moves

def adjacent_black_moves(board):
    
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    # calculating current dist
    # if it's captured, then it's over, and this
    # shouldn't be called.
    
    # can I mix both like this?
    kp = min(kingDistance(k, p), kingDistance(k, P))
     

    moves = []

    pawnMoves = board.generate_legal_moves(king=False, pawns=True)
    
    for m in pawnMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        moves.append((b2, m)) 
    
    # remaining legal Moves
    legalMoves = board.generate_legal_moves(pawns=False) 
    
    # in visited_W, we don't append every legal move, but we
    # append only those that pass our heuristics.
    

    for m in legalMoves:
        b2 = createNewBoard(board)
        b2.push(m) 
        k2 = getPieceCoOrd(b2, chess.KING, chess.BLACK)
        # p remains the same since we're moving king here
        k2p = min(kingDistance(k2, p), kingDistance(k2, P))
        # >= ?
        if k2p > kp:
            continue
        moves.append((b2, m))
    
    return moves

def adjacentPawns(board):
    
    A = {}
    
    score = targetedCalculation(board, adjacent_white_moves, adjacent_black_moves, adjacent_getScore, adjacent_isEnd)
    
    if score > 0:
        A['calculate winning'] = 1
    if score < 0:
        A['calculate drawing'] = 1

    return A




# Will be the end if 
#   1. black king is definitely blocking the white pawn
#   2. White king blocking black pawn + white pawn can't be
#   caught.
#   3. Queen + white to move.
#   4. Both Queens.
#   5. 
# (so white can't win).

def passed_isEnd(board):
    
    # white pawn captured:

    move = board.turn == chess.WHITE
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    Q = getPieceCoOrd(board, chess.QUEEN, chess.WHITE) 
    q = getPieceCoOrd(board, chess.QUEEN, chess.BLACK)
    
    w = P[0] == None and Q[0] == None
    b = p[0] == None and q[0] == None
    
    # don't care about b because it shouldn't end
    # if black pawn is captured.

    if w or b:
        return True
    
    if Q[0] != None and move:
        return True
    
    # not move means black to move
    if q[0] != None and not move:
        return True
    
    
    return False


def getQueenScore(board):
      
    # with depth = 3
    return targetedCalculation(board, queens_white_moves, queens_black_moves, queens_getScore, queens_isEnd, 3)
    

def passed_getScore(board):
    

    drawing_pawns = [0, 2, 5, 7]

    move = board.turn == chess.WHITE
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    Q = getPieceCoOrd(board, chess.QUEEN, chess.WHITE) 
    q = getPieceCoOrd(board, chess.QUEEN, chess.BLACK)
    
    ## Important to first deal with the queen special cases.
    # otherwise things like Pawn doesn't exist anymore fuck
    # stuff up.

    if q[0] != None and Q[0] == None:
        return -1
    
    # the way isEnd is structured, this should be
    # white's move.

    if Q[0] != None and q[0] == None:
     
        # 2nd rank:
        if p[0] != 1:
            return 1
        else:
            if p[1] not in drawing_pawns:
                return 1
            # NEED TO IMPLEMENT THE PAIN IN THE ASS 
            # IF KING IS CLOSE ENOUGH, IF WHITE KING
            # IS CLOSE ENOUGH CRAP. TEMP SOLUTION FOR NOW.

            else:
                if kingDistance(k, p) == 1:
                    return -1
                else:
                    return 1
    
    ### Need to search for tactics here.
    ### Add a lot of conditions here.
    ## Include a new tactics scanner here?

    if Q[0] != None and q[0] != None:

        return getQueenScore(board)
    ## dunno what to do here, but black pawn should never
    # need to be captured.
    
    # WHAT WE NEED HERE IS TO CALL THE FEATURE EXTRACTOR
    # FROM 3P ENDGAMES.
    #
    if p[0] == None and q[0] == None:
        val = predictOutputOnly(board, 3)
        # print val
        # print board
        return val
    
    if P[0] == None:
        return -1
    
    # possibly controversial
    if k[1] == P[1]:
        return -1

    
    # this will happen when it runs out of depth:
    return -1

def queens_white_moves(board):
    
    moves = []
    QMoves = board.generate_legal_moves(king=False, queens=True)
    
    for m in QMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        q = getPieceCoOrd(b2, chess.QUEEN, chess.BLACK)
        

        if b2.is_check():
            moves.append((b2, m)) 
        elif q[0] == None:
            moves.append((b2, m))

    return moves

def queens_black_moves(board):
    
    moves = []
    KMoves = board.generate_legal_moves(king=True)
    for m in KMoves: 
        b2 = createNewBoard(board)
        b2.push(m)
        moves.append((b2, m)) 
    return moves

def queens_isEnd(board):
    
    q = getPieceCoOrd(board, chess.QUEEN, chess.BLACK)

    if q[0] == None:
        return True


def queens_getScore(board):
    
    if debug:
        print 'get score in queen'
    
    q = getPieceCoOrd(board, chess.QUEEN, chess.BLACK)

    if q[0] == None:
        return 1
    else:
        return -1



def passed_white_moves(board):
    
    
    # spceial case when black just made a queen:

    moves = []
    
    q = getPieceCoOrd(board, chess.QUEEN, chess.BLACK) 
    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    
    if q[0] != None:
        
        if debug:
            print 'white move After Black QUEEN'

        if not kingDistance(K, q) > 1:
            
            if debug:
                print 'White king can capture it'
            # try to see if white can capture it:
            kMoves = board.generate_legal_moves(king=True, pawns=False)

            for m in kMoves:
                
                # can check if we're able to capture the queen or not here.
                b2 = createNewBoard(board)
                b2.push(m)
                moves.append((b2, m)) 
                 
        return moves



    
    p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    ## Added a check to make sure that only queen promotions considered.
    pawnMoves = board.generate_legal_moves(king=False, pawns=True)
    for m in pawnMoves:
        b2 = createNewBoard(board)
        b2.push(m)

        P = getPieceCoOrd(b2, chess.PAWN, chess.WHITE)
        Q = getPieceCoOrd(b2, chess.QUEEN, chess.WHITE)

        if P[0] != None or Q[0] != None:
            moves.append((b2, m)) 

    
    # remaining legal Moves
    legalMoves = board.generate_legal_moves(pawns=False) 
    
    black_can_catch = False
    if canCatchWhitePawn(board, "BLACK"):
        black_can_catch = True
    
    for m in legalMoves:

        b2 = createNewBoard(board)
        b2.push(m)
        
        if black_can_catch:
            if debug:
                print 'black can catch'
            if canCatchWhitePawn(b2, "WHITE"):
                moves.append((b2, m))
        else:
            if debug:
                print 'black can not catch'
            if canCatchBlackPawn(b2, "WHITE"):
                moves.append((b2, m))
                
                if debug:
                    print 'Thinks white can catch black pawn'

    return moves


# Consider the special case in which black king can be doing two jobs.


def passed_black_moves(board):
    
    moves = []
    
    P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    # consider all pawn moves and make sure only queen is promoted.

    pawnMoves = board.generate_legal_moves(king=False, pawns=True)
    for m in pawnMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        
        p = getPieceCoOrd(b2, chess.PAWN, chess.BLACK)
        q = getPieceCoOrd(b2, chess.QUEEN, chess.BLACK)

        if p[0] != None or q[0] != None:
            moves.append((b2, m)) 
        

    # remaining legal Moves
    legalMoves = board.generate_legal_moves(pawns=False) 
    
    white_can_catch = False
    if canCatchBlackPawn(board, "WHITE"):
        white_can_catch = True
    
    ## might fuck up some edge cases.
    
    white_pawn_faster = None
    if p[0] != None and P[0] != None:

        if 7 - P[0] < (p[0] - 1):
            white_pawn_faster = True
        else:
            white_pawn_faster = False


    for m in legalMoves:

        b2 = createNewBoard(board)
        b2.push(m)
        
        if canCatchWhitePawn(b2, "BLACK"):
            moves.append((b2, m))


        if white_can_catch:
            if canCatchBlackPawn(board, "BLACK") and not white_pawn_faster:
                moves.append((b2, m))


    return moves




def testEasyDraw(board):
    
    A = {}
    result = False
    
    wrongSide = False
    

    if PAWN[1] > KING[1] and PAWN[1] > king[1]:

        cd = king[1] - KING[1]
        if cd >= 2:
            wrongSide = True
   
    if PAWN[1] < KING[1] and PAWN[1] < king[1]:

       cd = KING[1] - king[1]
       if cd >= 2:
           wrongSide = True
    
    if canCatchWhitePawn(board, "BLACK") and wrongSide:

        result = True
        A['wrongside + black can catch'] = 1

    d_to_q = pawn[0]
    D_to_Q = 7 - PAWN[0]


    if not canCatchBlackPawn(board, "WHITE") and d_to_q < D_to_Q:
        result = True
        A['black promotes faster'] = 1


    a = canCatchWhitePawn(board, "BLACK")
    b = canCatchWhitePawn(board, "WHITE")
    c = canCatchBlackPawn(board, "WHITE")

    if a and not b:
        result = True
        A['wrongside + black can catch'] = 1

 #   fen = board.fen()
  #  new_fen = removePiece(fen, 'p')
  #  new_board = chess.Board(new_fen)
  #  score = predictOutputOnly(new_board, 3)

  #  if score < 0:
  #      result = True
  #      A['pawn remove draw'] = 1

## Will lead to some exceptions but a speedup...

#    if canCatchWhitePawn(board, "BLACK") and not canCatchWhitePawn(board, "WHITE"):
        
#        result = True
#        A['black can catch pawn but white cant'] = 1

    
    # Do the remove pawn test here.


    return (result, A)








def passedPawns(board):
    A = {}
    
    ## first run the remove pawn check --> should deal with many simpler cases.


    ## Then just run the targeted calculation and get an answer. That should take
    ## care of dealing with easy cases by doing the isEnd quickly.
    
    ## check basic drawing cases:
      
    
    T = testEasyDraw(board)
    if T[0]:
        return T[1]
       
        
    ## --> 

    score = targetedCalculation(board, passed_white_moves, passed_black_moves, passed_getScore, passed_isEnd)
    
    if score > 0:
        A['calculate winning'] = 1
    if score < 0:
        A['calculate drawing'] = 1

    return A





def arePassedPawns(board):

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    if row_p == None or row_P == None:
        return False

    r_diff = row_p - row_P
    c_diff = col_p - col_P
    
    # if both passed pawns.
    
    # r_diff should normally be +ve.
    if abs(c_diff) >= 2 or r_diff < 0:
        return True

    return False

# For K --> p.
#
# What if I remove every stupid heuristic, and only care about
# getting every option, then prune in isEnd.


# customized methods for targetedCalculation.

# white heuristic --> distance between K and pawn.
# Ideally, should have just returned True or False based
# on a bunch of conditions, and maybe take prev board as well.
# For now, this gives some values, and after some complicated
# mix, it all works out.

# Because of the complicated implementation here, needed to include the
# relaxed distance feature in the implementation of targetCalc --> that slows
# us down further. 
# + we've opposition in targetCalc for some complicated reasons, which might
# cause trouble for it when we generalize to other forms.
# Problem with True <--> False heuristic was that we needed context.
# Particularly <--> previous board. So could say when were moving backwards.

# Has become overly bloated and complicated as a heuristi# Has become overly bloated and complicated as a heuristicc

def distKp(board):
    
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # means it has been captured.
    if row_p == None:
        return -2

    A = (row_K, col_K)
    B = (row_p, col_p)
    dist = kingDistance(A, B)
    
    # adding penalties for the king being on a far off row.
    # Being on a far off column is usually preferrable, than being
    # on a far off row:
    #
    # Seems VERY rare if going backward will be better than going
    # forward, so I'll go ahead and put this here.
    
    # just don't want to do that unless it's a must.
    if abs(row_K - row_p) >= 2:
     #   print 'yes K too low'
        dist += 2
    
    # Adding bonuses for opposition completely fucks it up.
    
    return dist

# Heuristic for black. This guy should be willing to go
# after both the pawns <--> white or black.
# We weren't able to include the relaxed distance feature in
# the 

def distkp(board):
    
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    # if the piece has been captured, then this should return -1 or 0?!
    row_p, col_p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    row_P, col_P = getPieceCoOrd(board, chess.PAWN, chess.WHITE)    
    # means it has been captured.
    if row_p == None or row_P == None:
        return 0


    k = (row_k, col_k)
    p = (row_p, col_p)
    P = (row_p, col_P)

    A = kingDistance(k, p)
#    return A
    B = kingDistance(k, P)
    return min(A, B)

# check in the results if this is really a big deal.
# RIGHT now we're just returning everything.
#
def black_moves(board):

    old_dist = distkp(board)
    old_coord = getPieceCoOrd(board, chess.KING, chess.BLACK)
    p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    moves = []

    legalMoves = board.generate_legal_moves(pawns=False) 
     
    
    for m in legalMoves:
        
        b2 = createNewBoard(board)
        b2.push(m)
        new_dist = distkp(b2)
        new_coord = getPieceCoOrd(b2, chess.KING, chess.BLACK)
      
        # cur_dist and new_dist would take care to remove
        # options that make the king go back.
        
        if new_dist <= old_dist:
    #    if True:
            moves.append((b2, m))
        else:
            if opposition(b2):
                moves.append((b2,m))
            
    return moves

def white_moves(board):
    
    K = getPieceCoOrd(board, chess.KING, chess.WHITE)
    p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    
    # calculating current dist
    Kp = kingDistance(K, p)
    
    # compare with old one:
    d = Kp - KING_pawn_D 

    # 2 is a conservative estimate:
    if d > 2: 
        TOO_FAR = True
    else:
        TOO_FAR = False

 #   KING_pawn_D = kingDistance(KING, pawn)

    

    # distKp has evolved into a complicated heuristic function.
    old_dist = distKp(board)
    old_coord = getPieceCoOrd(board, chess.KING, chess.WHITE)

    moves = []

    pawnMoves = board.generate_legal_moves(king=False, pawns=True)
    for m in pawnMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        moves.append((b2, m)) 
    
    # remaining legal Moves
    legalMoves = board.generate_legal_moves(pawns=False) 
    
    # in visited_W, we don't append every legal move, but we
    # append only those that pass our heuristics.
    
    list = []

    for m in legalMoves:
        b2 = createNewBoard(board)
        b2.push(m)
        new_dist = distKp(b2)
        new_coord = getPieceCoOrd(b2, chess.KING, chess.WHITE)
            
            # cur_dist and new_dist would take care to remove
            # options that make the king go back.

        if old_dist >= new_dist:
  #      if True:
            list.append((new_dist,b2, m))
        else:
            if opposition(b2) and not TOO_FAR:
                list.append((new_dist,b2,m))

    #        elif new_coord[0] > old_coord[0]:
    #            moves.append((b2,m))
    
    # Important because ordering makes a big difference here.

    list.sort(key=lambda x: x[0])
    for x in list:
        moves.append((x[1], x[2]))
        # if pawn capture possible, don't
        # consider everything else.
        if x[0] < 0:
            break

    return moves


# This getScore guy should use the 1p tester if pawn captured,
# else it should just return 0. 
# NEED TO USE A PROPER SCORING --> using test of 1p here.

def getScore(board):
    
    simpleT = simpleTests(board)
    
    # test it.
    # just returns the score from simpleT
    if simpleT[0]:
        return simpleT[2]
    
    
    # REPLACE THIS WITH THE 3P FEATURE EXTRACTOR.

    p = board.pieces(chess.PAWN, chess.BLACK)
    P = board.pieces(chess.PAWN, chess.WHITE)

    if len(p) == 0 and len(P) == 1:
      #  return 1
        return 1
    else:
        return -1


# we need to send in custom made end functions.
#
# CAN improve this considerably to prune out unneccesary options...
# divide work with the heuristics..but ok no need for now.

def isEnd_samefileP(board):
    
    simpleT = simpleTests(board)
    
    if simpleT[0]:
        return True

    # condition for end --> pawn Queening.
    p = board.pieces(chess.PAWN, chess.BLACK) 
    P = board.pieces(chess.PAWN, chess.WHITE)

    if len(p) == 0 or len(P) == 0:
        return True
    else:
        return False

# CAN CHANGE STUFF INSIDE TARGETED CALCULATION <--> like the restriction of
# relaxed move etc. But screw it for now.   

# wrapper method for sending targetCalculation for 2 different types of positions.
# Below 5 offers black more drawing chances. 

# We don't really need to make changes to this because if the black k can reach defensive
# spot --> then this wouldn't be called.

def calculate_below5(board):

    
    # test if the piece exists:
    
    # let's say this returns -1 or 1 based on draw or win. Then we can
    # check it with flipped boards, and then decide if it's a draw or win.
    # depth could be the distance of K from P + 2 or something? Or just
    # put up something even bigger.
    score = targetedCalculation(board, white_moves, black_moves, getScore, isEnd_samefileP)
    return score

def calculate_rank5(board):

    
    # test if the piece exists:
    
    # let's say this returns -1 or 1 based on draw or win. Then we can
    # check it with flipped boards, and then decide if it's a draw or win.
    # depth could be the distance of K from P + 2 or something? Or just
    # put up something even bigger.
    score = targetedCalculation(board, white_moves, black_moves, getScore, isEnd_samefileP)
    return score

## Type 3 --> sameFile.
## wrapper function around two types of it.


def sameFilePawn(board):
    
    simpleTest = simpleTests(board)
    if simpleTest[0]:
        return simpleTest[1]


    A = {}
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE) 
    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)

    row_k, col_k =  getPieceCoOrd(board, chess.KING, chess.BLACK)
    row_K, col_K =  getPieceCoOrd(board, chess.KING, chess.WHITE)
    
    kingsReversed = False
    if row_K > row_k:
        kingsReversed = True
    
    
    move = board.turn == chess.WHITE
    
    ## special condition, so if we can move into the
    # 5th rank, then it is also acceptable.
    if move and row_p > 4:
        row_P += 1
    
    ## All these conditions apply to cases where k <--> K 
    # are usually placed. If their sides are reversed, then
    # all we should just call calculation and get done.
    
    # we include kingsReversed here as well, because then the main idea
    # of defence in rank 4 and below doesn't really help.
    if row_P >= 4 or kingsReversed:
        A = sameFilePawn_rank5(board)
    else:
        A = sameFilePawn_below5(board)


    return A



## Two different divisions of sameFile:
# first few lines are very similar, and should have 
# been decomposed...

def sameFilePawn_below5(board):

    A = {}
    
    ## do some shit and then update A
    # and return.
    
    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
           
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # key defensive square --> 2 rows above the black pawn:
    
    # +2 because we're increasing upwards.
    key_r = row_p + 2
    key_c = col_p
    k_defense = kingDistance((key_r,key_c), (row_k, col_k))
    
   
    # should just call kingDistance at all these places here:
    # distance to black pawn:    

    K1 = abs(row_K - row_p) 
    K2 = abs(col_K - col_p)
    K_p = max(K1, K2)
    

    k1 = abs(row_k - row_p) 
    k2 = abs(col_k - col_p)
    k_p = max(k1, k2)
    
    # distance to white pawn for black king:
            
    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_P = max(k1, k2)
    

    # check heuristic:
    k_d = min(k_P, k_p)
    # consider counterattacking case separately.


    ### --> MAYBE CONSIDER PAWN ON 2nd row as a separate case?
    if move:
        K_p -= 1
    else:
        k_d -= 1
        k_defense -= 1

    d = K_p - k_d
    
    if abs(row_p - row_P) == 1:
        # +1 because black just needs to reach the
        # defensive square, not defend it.
        if k_defense <= (K_p+1):
            A['king close to defensive square'] = 1
            return A


    # CHECK! maybe increase cushion?
    # keeping a cushion of one move. Negative d implies that
    # king is closer to defence.
    if d < -2:
        A['black king too far to defend'] = 1
    elif d > 1:

        A['black king too close to defend'] = 1
    else:
        result = calculate_below5(board)
    
        if result > 0:
            A['calculate winning'] = 1
        else:
            A['calculate drawing'] = 1

    return A



def sameFilePawn_rank5(board):
    
    A = {}
    # information common to all these functions
    
    # P over 5th rank
    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # distance to black pawn:

    K1 = abs(row_K - row_p) 
    K2 = abs(col_K - col_p)
    K_p = max(K1, K2)
    

    k1 = abs(row_k - row_p) 
    k2 = abs(col_k - col_p)
    k_p = max(k1, k2)
    
    # distance to white pawn for black king:
            
    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_P = max(k1, k2)
    
    # check heuristic:
    k_d = min(k_P, k_p)
    # consider counterattacking case separately.

    result = 0
    ### --> MAYBE CONSIDER PAWN ON 2nd row as a separate case?
    if move:
        K_p -= 1
    else:
        k_d -= 1
    
    d = K_p - k_d
    
    # means k is much closer.
    if d > 2:
        A['black king much closer'] = 1
    # means K is much closer.
    elif d < -2:
        A['White king much closer'] = 1
    # otherwise call the damned thing.
    else:
        result = calculate_rank5(board)    
    
    if result > 0:
        A['calculate winning'] = 1
    else:
        A['calculate drawing'] = 1

    return A

def simpleTests(board):
    
    KD = KING_pawn_D
    kd = min(king_pawn_D, king_PAWN_D)
    
    score = 0
    result = False
    A = {}
    
    if MOVE:
        KD -= 1
    else:
        kd -= 1
    
    cd = king[1] - KING[1]
    d = kd - KD
#    d2 = king_PAWN_D - KING_pawn_D

    # less than because that means black king rank actually incr.
    if king[0] <= pawn[0] and cd <= 1 and SAME_SIDE:
        A['black king same rank or above'] = 1
        result = True
        score = -1
    # conservative estimates
    if d > 2:
        A['black king too far'] = 1
        result = True
        score = 1

    return (result, A, score)
    


### BASICALLY, EVERYTHING BELOW THIS IS PROBABLY CRAP:

### Not using it, not sure if it is just junk or not.
# Have similar things in each of the other things.

def basicDistances(board):

    A = {}

    move = board.turn == chess.WHITE
    
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)
             
    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    
    row_P, col_P =  getPieceCoOrd(board, chess.PAWN, chess.WHITE)

    row_p, col_p =  getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    # distance to black pawn:

    K1 = abs(row_K - row_p) 
    K2 = abs(col_K - col_p)
    K_p = max(K1, K2)
    

    k1 = abs(row_k - row_p) 
    k2 = abs(col_k - col_p)
    k_p = max(k1, k2)
    
    # distance to white pawn for black king:
            
    k1 = abs(row_k - row_P) 
    k2 = abs(col_k - col_P)
    k_P = max(k1, k2)
    
    # check heuristic:
#    k_d = min(k_P, k_p)
    # consider counterattacking case separately.


    ### --> MAYBE CONSIDER PAWN ON 2nd row as a separate case?
    if move:
        K_p -= 1
    else:
        k_p -= 1
    
    if row_p >= 5 and row_P >= 4:
        high_P = True
    else:
        high_P = False

    # black's king closer to p should lead to a draw in cases
    # where black's pawn is above 3rd rank.
     
    if k_p <= K_p:
        if not high_P:
            A['black king close + no high p'] = 1
        if high_P:
            A['black king close + high p'] = 1
    else:
        A['white king close to p'] = 1

    
    return A
            




def predictOutputOnly(board, numPieces):
    #cprint "Entered"
    move = board.turn == chess.WHITE
    if not move: #do somethingc
        return -1

    features = {}
    if numPieces == 3:
        weights = weight_vector_3_piece
        features = featureExtractor_3(board)

    elif numPieces == 4:
        weights = weight_vector_4_piece
    elif numPieces == 5:
        weights = weight_vector_5_piece


    ourVal = 0

    for val in features:
        ourVal += weights[val] * features[val]

    if (ourVal <= 0):
        ourVal = -1
    elif (ourVal > 0):
        ourVal = 1

    #print "exited"
    return ourVal

def removePiece(FEN, piece):
    board = [[] for i in range(8)]
    curPos = 0
    curCol = 0
    while curCol <= 7:
        curRow = 1
        while curRow <= 8:
            if (is_number(FEN[curPos])):
                curRow += int(FEN[curPos])
            elif FEN[curPos] != piece:
                board[curCol].append((FEN[curPos], curRow))
                curRow += 1
            elif FEN[curPos] == piece:
                curRow += 1
            curPos += 1
        curPos += 1
        curCol += 1


    val = processBoard(board)

    pos = 0
    while (FEN[pos] != " "):
        pos += 1
    for i in range(pos, len(FEN)):
        val += FEN[i]

    return val


def processBoard(board):
    FEN = ""
    newBoard = []
    for x in board:
        newBoard.append(sorted(x, key=lambda l:l[1]))
    board = newBoard
    for j, row in enumerate(board):
        rowFEN = ""
        curFilled = 0
        prevPos = 0
        for i,piece in enumerate(row):
            if (piece[1] == 1):
                rowFEN = piece[0]
                curFilled = 1

            elif i == 0:
                rowFEN = str(piece[1] - 1) + piece[0]
                curFilled = int(piece[1])
            else:
                diff = int(piece[1]) - curFilled - 1
                if (diff != 0):
                    rowFEN += str(diff)
                rowFEN += piece[0]
                curFilled = int(piece[1])
        left = 8 - curFilled

        if left > 0:
            rowFEN += str(left)

        FEN += rowFEN
        if j != 7:
            FEN += "/"
    return FEN

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def featureExtractor_3(x):
    """
    Chess Features
    """
    
    features = {}
    features = Counter()

    features.update(canCatchPawn(x))
    if (features['cant catch pawn'] == 1):
        return features

    features.update(canBeCaptured(x))
    # if (features['black_can_capture'] == 1):
    #     return {'black_can_capture':1}
    features.update(isWhiteKingAhead(x))
    features.update(isOpposition(x))
    features.update(move_distances(x))
    features.update(wrongSide(x))
    features.update(ishPawn(x))
    
    return features
#### one-pawn Features below ---> old ones.


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

