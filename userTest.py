import copy
import chess
import chess.syzygy
import chess.gaviota
import collections

from collections import Counter
import features
from features import *
import os.path


import features2P

import helperMethods as helper

#weight_vector_3_piece = {'black_king_closer_to_winning_square': -1.400000000000001, 'black_opposition': -1.9200000000000015, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.27, 'white_king_closer': 1.0700000000000007, 'white_king_closer_to_winning_square': -0.22000000000000008, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.04000000000000009, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.42000000000000015, 'black_king_wrong_side': 1.5400000000000011, 'white_king_blocked': -0.6000000000000003, 'white_king_wrong_side': -1.570000000000001, 'black_king_closer': -1.340000000000001, 'h_pawn': -2.6499999999999875}
weight_vector_3_piece = {'black_king_closer_to_winning_square': -1.310000000000001, 'black_opposition': -0.22000000000000006, 'white_opposition': -1.490000000000001, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.3700000000000001, 'white_king_closer': 1.0000000000000007, 'white_king_closer_to_winning_square': -0.3200000000000002, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.03000000000000009, 'white winning setup': -0.02, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.44000000000000017, 'black_king_wrong_side': 1.6300000000000012, 'white_king_blocked': -0.6100000000000003, 'white_king_wrong_side': -1.520000000000001, 'black_king_closer': -1.370000000000001, 'h_pawn': -2.6499999999999875}
weight_vector_4_piece = { \
	'simple adjacent draw': -0.833, \
	'calculate winning': 1.44, \
	'calculate drawing': -0.93, \
	'wrongside + black can catch': -1.12, \
	'black promotes faster': -0.68, \
	'pawn remove draw': -1.5, \
	'king close to defensive square': -0.88, \
	'black king too far to defend': 0.93, \
	'black king too close to defend': -0.91, \
	'black king much closer': -1.24, \
	'white king much closer': 1.09, \
	'black king same rank or above': -0.49, \
	'black king too far': 0.43, \
	'black king close + no high p': -0.14, \
	'black king close + p': -0.08, \
	'white king close to p': 0.24, \
}
weight_vector_5_piece = {'black_king_closer_to_winning_square': -1.400000000000001, 'black_opposition': -1.9200000000000015, 'cant catch pawn': 1.0000000000000007, 'can catch pawn': -0.27, 'white_king_closer': 1.0700000000000007, 'white_king_closer_to_winning_square': -0.22000000000000008, 'black_can_capture': -0.38000000000000017, 'white_king_blocked_down': 0.04000000000000009, 'white_king_blocked_side': -0.5200000000000002, 'white king ahead': 0.42000000000000015, 'black_king_wrong_side': 1.5400000000000011, 'white_king_blocked': -0.6000000000000003, 'white_king_wrong_side': -1.570000000000001, 'black_king_closer': -1.340000000000001, 'h_pawn': -2.6499999999999875}

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

def featureExtractor_4(x):
    val = features2P.getFeatures2P(x)
    print val
    return val


def userInput():
	print ""
	print "This is an endgame solver designed to solve 3,4 and 5 piece chess"
	print "Currently it can solve the following board combinations: " #fill 
	print "Please enter the board in algebraic notation, enter . when you are done"
	print "Uppercase letters define white's pieces, while lowecase define black's pieces"
	print "If there are 2 pieces on the same row, please enter them in ascending order (ka1 before Pa3)"
	print ""
	pieces = []
	while True:
		newPiece = raw_input('Enter new piece: ')
		if newPiece == ".":
			break
		else:
			pieces.append(newPiece)

	FEN = processInput(pieces)

	turn = raw_input('Whose move is it (b or w): ')

	board = chess.Board(FEN + " " + turn + " - - 0 1")
	if turn == "w":
		mirror = helper.mirror_image(FEN + " " + "b" + " - - 0 1")
	else:
		mirror = helper.mirror_image(FEN + " " + "w" + " - - 0 1")
	mirrorBoard = chess.Board(mirror)

	syzygy = chess.syzygy.Tablebases()
	num = 0
	num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))

	actualOutput = 0
	predictedOutput = 0

	if len(pieces) == 3:

		output = predictOutput(board, syzygy, len(pieces))

		actualOutput = output[0]
		predictedOutput = output[1]

	elif len(pieces) == 4:
		output1 = predictOutput(board, syzygy, len(pieces))
		output2 = predictOutput(mirrorBoard, syzygy, len(pieces))

		actualOutput = output1[0]
		if (output1[1] == 1 or output2[1] == 1):
			predictedOutput = 1
		else:
			predictedOutput = -1

	if actualOutput != -100:
		if actualOutput == -1:
			print ""
			print "The actual value according to databases is: DRAW"
		else:
			print ""
			print "The actual value according to databases is: WIN"

		if predictedOutput == -1:
			print "The predicted output according our algorithm is: DRAW"
		else:
			print "The predicted output according our algorithm is: WIN"
	print ""
#problem
#Enter new piece: Ka2
# Enter new piece: ka6
# Enter new piece: pd2
# Enter new piece: .
# Whose move is it (b or w): w
# 3

def predictOutput(board, syzygy, numPieces):
	features = {}
	if numPieces == 3:
		weights = weight_vector_3_piece
		features = featureExtractor_3(board)

	elif numPieces == 4:
		weights = weight_vector_4_piece
		features = featureExtractor_4(board)
	elif numPieces == 5:
		weights = weight_vector_5_piece

	print board

	expectVal = syzygy.probe_wdl(board)
	if (expectVal is None):
	    print "Illegal move"
	    return (-100, -100)

	elif (expectVal == 0):
	    expectVal = -1
	else:
	    expectVal = 1


	ourVal = 0

	for val in features:
	    ourVal += weights[val] * features[val]

	print ourVal

	if (ourVal <= 0):
	    ourVal = -1
	elif (ourVal > 0):
	    ourVal = 1


	return (expectVal, ourVal)

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


def processInput(pieces):
	FEN = ""
	board = [ [] for i in range(8)]
	Error = ""
	wasError = False
	for piece in pieces:
		if len(piece) > 3:
			Error = piece + " incorrect"
			wasError = True
			break
		pieceType = piece[0]

		column = int(piece[2]) - 1
		row = piece[1]


		row = ord(row) - ord('a') + 1
		#row = row - 1

		if column > 7 or row > 8:
			wasError = True
			Error = "Row or column invalid"
			break

		column = 7 - column

		board[column].append((pieceType, row))

	FEN = processBoard(board)
	return FEN

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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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

def getVal(FEN):
	syzygy = chess.syzygy.Tablebases()
	num = 0
	num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))

	board = chess.Board(FEN)
	expectVal = syzygy.probe_wdl(board)
	return expectVal

userInput()


	