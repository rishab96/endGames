
# !/usr/bin/env python

import numpy as np
import chess
import chess.uci

# Take an fen --> swap_colors --> mirror_horizontal to get
# the mirror image with black being white. Also don't forget
# to change whose move it is.

## This should be in the features part <--> but wasn't working out.
## Good thing is that in rook pawn endgames, this might still be useful,
# and anyway no reason why it will be bad.

def opposition(board):

    row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
    row_K, col_K = getPieceCoOrd(board, chess.KING, chess.WHITE)

    rd = row_k - row_K
    cd = col_k - col_K

    if rd == 2 and (abs(cd) == 2 or cd == 0):
        return True
    
    return False

def mirror_image(fen):

    swap = swap_colors(fen)
    mirror = mirror_vertical(swap)
    return mirror


def swap_colors(fen):
    parts = fen.split()
    return parts[0].swapcase() + " " + parts[1] + " - - 0 1"

def mirror_vertical(fen):
    parts = fen.split()
    position_parts = "/".join(reversed(parts[0].split("/")))
    return position_parts + " " + parts[1] + " - - 0 1"

def mirror_horizontal(fen):
    parts = fen.split()
    position_parts = "/".join("".join(reversed(position_part)) for position_part in parts[0].split("/"))
    return position_parts + " " + parts[1] + " - - 0 1"


def manhattanDistance( xy1, xy2 ):
  "Returns the Manhattan distance between points xy1 and xy2"
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

## Usual helper methods.
def kingDistance(square1, square2): 

    row = abs(square1[0] - square2[0]) 
    col = abs(square1[1] - square2[1])
    return max(row, col)

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
        return (None, None)
   
    row_k, col_k = getRowAndColumn(num)
    
    return row_k, col_k

def createNewBoard(board):
    
#    print board

    FEN = board.fen()
    return chess.Board(FEN)


def canCatchWhitePawn(board, king_color):   

    if king_color == "WHITE":
        row_k, col_k = getPieceCoOrd(board, chess.KING, chess.WHITE)
        move = board.turn == chess.WHITE
    
    else:
        row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
        move = board.turn == chess.BLACK     
    
    row_w_p, col_w_p = getPieceCoOrd(board, chess.PAWN, chess.WHITE)
    
    Q = getPieceCoOrd(board, chess.QUEEN, chess.WHITE)
    ## because this probably means that 
    if row_w_p == None and Q[0] == None:
        return False
    
    if row_w_p == None and Q[0] != None:
        return True
    
    if row_w_p == 1:
        row_w_p += 1
    
    ## update the row_k and col_k based on if it's our move or not: 
    if move:
        row_k += 1

        if col_k < col_w_p:
            col_k += 1
        elif col_k > col_w_p:
            col_k -= 1    

    if row_k < row_w_p:
        return False 

    moves_to_end = 7 - row_w_p
    moves_to_catch = abs(col_w_p - col_k) - 1
    
    if moves_to_end <= moves_to_catch:
        return False


    return True


def canCatchBlackPawn(board, king_color):
    
    
    # move should be true or false;
     
    if king_color == "WHITE":
        row_k, col_k = getPieceCoOrd(board, chess.KING, chess.WHITE)
        move = board.turn == chess.WHITE
    
    else:
        row_k, col_k = getPieceCoOrd(board, chess.KING, chess.BLACK)
        move = board.turn == chess.BLACK     
    
    row_b_p, col_b_p = getPieceCoOrd(board, chess.PAWN, chess.BLACK)
    
    q = getPieceCoOrd(board, chess.QUEEN, chess.BLACK)

    if row_b_p == None and q[0] == None:
        return False
    
    ## To be much more efficient should just check if the queen
    # square is attacked or not. WILL CHANGE LATER>
    if row_b_p == None and q[0] != None:
        return True
    
    if row_b_p == 6:
        row_b_p -= 1
    
    ## update the row_k and col_k based on if it's our move or not:
    
    if move:
        row_k -= 1

        if col_k < col_b_p:
            col_k += 1
        elif col_k > col_b_p:
            col_k -= 1    

    if row_k > row_b_p:
        return False 

    moves_to_end = row_b_p
    moves_to_catch = abs(col_b_p - col_k) - 1
    
    # because it's black's move:
    if moves_to_end <= moves_to_catch:
        return False


    return True
