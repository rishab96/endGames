#3 piece
import random
import collections
import math
import sys
from collections import Counter
from collections import defaultdict
from util import *

import copy
import chess
import chess.syzygy
import chess.gaviota

import functools
import os.path
import warnings
import json

import features
from features import *

import features2P
from features2P import *

def extractFeatures(x):
    val = getFeatures2P(x)
    print "here"
    print val
    return val

def isIllegal(FEN):

    rows = FEN.split('/')
    
    for i, j in enumerate(rows):
        if i == 0 or i == 7:
            for ch in j:
                if ch == 'P' or ch == 'p':
                    return True

    return False

def train(trainExamples, testExamples, featureExtractor, color, syzygy):
    weights = {}
    weights = defaultdict(lambda: 0.0, weights)

    numIters = 1;
    curIters = 0;
    n = 0.01

    pos = 0

    blackPos = 0
    blackNeg = 0
    for i in range (0,numIters):


        for xl,t in enumerate(trainExamples):

            if isIllegal(t):
                continue

            dotProd = 0.0

            board = chess.Board(t + " " + color + " - - 0 1")
            print board
            print xl
            print ""
           
            expectVal = syzygy.probe_wdl(board)

            if (expectVal is None):
                continue
            elif (expectVal == 0):
                expectVal = -1.0
            else:
                expectVal = 1.0

            print str(xl) + " " + str(expectVal)

            features = featureExtractor(board)

            for val in features:
                dotProd += weights[val] * features[val]

            if (1 - dotProd * expectVal) >= 0:
                for val in features:
                    weights[val] = weights[val] +  n * features[val] * expectVal

            curIters = curIters + 1
    return weights

def test(examples, color, weights, syzygy):
    total = 0
    correct = 0
    incorrect = 0
    for t in examples:
        if isIllegal(t):
            continue

        board = chess.Board(t + " " + color + " - - 0 1")
        expectVal = syzygy.probe_wdl(board)
        features = extractFeatures(board)
        
        if (expectVal is None):
            continue
        elif (expectVal == 0):
            expectVal = -1
        else:
            expectVal = 1


        ourVal = 0
            
        for val in features:
            ourVal += weights[val] * features[val]

        if (ourVal <= 0):
            ourVal = -1

        elif (ourVal > 0):
            ourVal = 1
        
        
        if ourVal == expectVal:
            correct = correct + 1

        total = total + 1
            
        if (total % 1000 == 0):
            print correct
            print total
            print " "

    print correct
    print total
