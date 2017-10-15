import time
from strategies import *
from random import choice


class AlphaBetaPruningAgent():
    def __init__(self, depthLimit, timeLimit, size):
        self.depthLimit = depthLimit
        self.timeLimit = timeLimit
        self.bestMove = set()
        self.size = size
        self.treeSize = 0
        self.evaluatedNodes = 0

    def getMove(self, board, playerSide):
        # print 'board =', GUI.getPossiMoves(board)
        self.player = playerSide
        self.opponent = -self.player
        alpha = float("-inf")
        beta = float("inf")
        startTime = time.clock()
        my_strategy = strategy(board, self.size, playerSide)
        # print "myboard", my_strategy.board
        # print "playerSide", playerSide

        if my_strategy.getMustWinMoves() != []:
            return choice(my_strategy.getMustWinMoves())
        elif my_strategy.getMustMoves() != []:
            return choice(my_strategy.getMustMoves())
        if my_strategy.alreadyPlacedBlockNum() < 0:
            self.abMinimax(board, 1, playerSide, startTime, alpha, beta)
        else:
            score = self.abMinimax(board, self.depthLimit, playerSide, startTime, alpha, beta)
            if score == self.size ** 3:
                print "Predication: Player", self.player, "must win in the future!"
            elif score == -self.size ** 3:
                print "Predication: Player", -self.player, "must win in the future!"
        # print "depth", self.depthLimit
        # print "best moves", self.bestMove
        print "evaluated nodes", self.evaluatedNodes
        print "tree size", self.treeSize
        return choice(list(self.bestMove))

    def abMinimax(self, board, depth, playerSide, startTime, alpha, beta):
        # print "alpha, beta =", alpha, beta
        # print "depth",depth
        self.evaluatedNodes += 1
        self.treeSize += 1
        my_strategy = strategy(board, self.size, playerSide)
        if depth == self.depthLimit and playerSide == self.player:
            possiMoves = my_strategy.getGoodMoves()
        else:
            possiMoves = my_strategy.getAllPossiMoves()
            # if depth == self.depthLimit and playerSide == self.player:
            # print "possible moves", possiMoves
        if depth == 0 or len(possiMoves) == 0 or my_strategy.winner() != None:
            # print "heuristic =", self.heuristic(GUI, board, playerSide)
            return self.heuristic(my_strategy)

        if playerSide == self.player:
            bestScore = float("-inf")
            for move in possiMoves:
                # print "move",move
                if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                    return bestScore
                nextBoard = my_strategy.getNextBoard(move)
                score = self.abMinimax(nextBoard, depth, self.opponent, startTime, alpha, beta)
                # print 'alpha,beta =  ', alpha, beta
                # print 'board', nextBoard
                if score > bestScore:
                    bestScore = score
                    if depth == self.depthLimit:
                        # print "move", move
                        # print "bestScore", bestScore
                        self.bestMove = set()
                        self.bestMove.add(move)

                '''elif score == bestScore:
                    if depth == self.depthLimit:
                        self.bestMove.add(move)
                        print "move", move
                        print "bestScore", bestScore'''
                if bestScore >= beta:
                    self.treeSize -= 1
                    continue
                alpha = max(bestScore, alpha)

        if playerSide == self.opponent:
            bestScore = float("inf")
            for move in possiMoves:
                # print "move",move
                if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                    return bestScore
                nextBoard = my_strategy.getNextBoard(move)
                # print 'nextboard', nextBoard
                # print 'player', self.player
                # print 'depth', depth
                score = self.abMinimax(nextBoard, depth - 1, self.player, startTime, alpha, beta)
                if score < bestScore:
                    bestScore = score
                if bestScore >= beta:
                    self.treeSize -= 1
                    continue
                beta = min(bestScore, beta)

                # if playerSide == self.player and depth == self.depthLimit:
                # self.bestMove = choice(bestMoves)

        return bestScore

    def heuristic(self, strategy):
        if strategy.winner() == 1:
            if self.player == 1:
                return self.size ** 3
            elif self.player == -1:
                return -self.size ** 3
        elif strategy.winner() == 2:
            if self.player == -1:
                return self.size ** 3
            elif self.player == 1:
                return -self.size ** 3
        else:
            return strategy.getSecondShortestPathLength(strategy.playerSide)
