import ThreePieceTrain as three
import FourPieceTrain as four

import util
from util import *

import copy
import chess
import chess.syzygy
import chess.gaviota

import functools
import os.path
import warnings
import json

import collections
from collections import Counter

numPieces = raw_input('Number of pieces: ')

inp = raw_input('train or both (both = train and test): ')

syzygy = chess.syzygy.Tablebases()
num = 0
num += syzygy.open_directory(os.path.join(os.path.dirname(__file__), "four-men"))


if int(numPieces) == 3:
	#print "here"
	data3 = readExamples('data3.txt')
	testExamples = data3
	trainExamples = data3

	if inp == "train":
		print three.train(trainExamples, trainExamples, three.extractFeatures, "w", syzygy)

	elif inp == "both":
		weights = three.train(trainExamples, trainExamples, three.extractFeatures, "w", syzygy)
		print weights
		three.test(testExamples, "w", weights, syzygy)
		print weights

elif int(numPieces) == 4:
	#print "here"
	data4 = readExamples('data4.txt')
	testExamples = data4
	trainExamples = data4

	if inp == "train":
		#print "here"
		print four.train(trainExamples, trainExamples, four.extractFeatures, "w", syzygy)

	elif inp == "both":
		weights = four.train(trainExamples, trainExamples, four.extractFeatures, "w", syzygy)
		four.test(testExamples, "w", weights, syzygy)