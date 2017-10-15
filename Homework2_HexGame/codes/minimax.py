import time
from strategies import *
from random import choice


class minimaxAgent:
    def __init__(self, depthLimit, timeLimit, size):
        self.depthLimit = depthLimit
        self.timeLimit = timeLimit
        self.bestMove = None
        self.size = size

    def getMove(self, board, playerSide):

        startTime = time.clock()
        if self.timeLimit == -1:
            self.minimax(board, self.depthLimit, playerSide, startTime)
        elif self.timeLimit != -1:
            while time.clock() - startTime <= self.timeLimit:
                self.minimax(board, self.depthLimit, playerSide, startTime)
                # print "heuristic =", self.heuristic(GUI, board, playerSide)
        return self.bestMove

    def minimax(self, board, depth, playerSide, startTime):
        my_strategy = strategy(board, self.size, playerSide)
        possiMoves = my_strategy.getPossiMoves()
        if depth == 0 or len(possiMoves) == 0:
            # print "heuristic =", self.heuristic(GUI, board, playerSide)
            return self.heuristic(my_strategy)

        scores = []
        for move in possiMoves:
            if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                break
            nextBoard = my_strategy.getNextBoard(move)
            scores.append(self.minimax(nextBoard, depth - 1, -1 * playerSide, startTime))

        if playerSide == 1:
            if depth == self.currentDepth:
                m = max(scores)
                ilist = [i for i, j in enumerate(scores) if j == m]
                self.bestMove = possiMoves[choice(ilist)]
                return max(scores)

        else:
            if depth == self.currentDepth:
                m = min(scores)
                ilist = [i for i, j in enumerate(scores) if j == m]
                self.bestMove = possiMoves[choice(ilist)]
                return min(scores)

    def heuristic(self, strategy):
        playerSide = -strategy.playerSide
        strategy.playerSide = playerSide
        if strategy.winner() == 1:
            return self.size ** 3
        elif strategy.winner() == 2:
            return (-1 * (self.size ** 3))
        else:
            '''
            moves_already = -self.currentDepth
            for row in range(self.size):
                for col in range(self.size):
                    if strategy.board[row][col] != 0:
                        moves_already += 1
            # print "moves_already =", moves_already

            if moves_already <= 2:
                center = self.size / 2
                greatFirstMove = [strategy.board[center, center], strategy.board[center - 1][center],
                                  strategy.board[center][center - 1],
                                  strategy.board[center - 1][center - 1]]
                if strategy.playerSide in greatFirstMove:
                    return (strategy.playerSide * (self.size ** 3))
                return 0

            elif moves_already <= self.size:
                return (strategy.countGapConnected() + strategy.getExpandedNum())
            else:
                return (
                    strategy.countUsefulConnected() + strategy.getExpandedNum())
'''
            return strategy.playerSide * strategy.getSecondShortestPathLength(strategy.playerSide)


class AlphaBetaPruningAgent():
    def __init__(self, depthLimit, timeLimit, size):
        self.depthLimit = depthLimit
        self.timeLimit = timeLimit
        # self.bestMove = None
        self.size = size

    def getMove(self, board, playerSide):
        # print 'board =', GUI.getPossiMoves(board)
        self.player = playerSide
        self.opponent = -self.player
        alpha = float("-inf")
        beta = float("inf")
        startTime = time.clock()
        bestScore, bestPath = self.abMinimax(board, self.depthLimit, playerSide, startTime, alpha, beta)
        return bestPath[0]

    def abMinimax(self, board, depth, playerSide, startTime, alpha=float("-inf"), beta=float("inf")):
        # print "alpha, beta =", alpha, beta
        my_strategy = strategy(board, self.size, playerSide)
        possiMoves = my_strategy.getPossiMoves()
        if depth == 0 or len(possiMoves) == 0 or my_strategy.winner() != None:
            # print "heuristic =", self.heuristic(GUI, board, playerSide)
            return self.heuristic(my_strategy), []
        bestMove = None

        if playerSide == self.player:
            bestScore = float("-inf")
            for move in possiMoves:
                if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                    return bestScore, path
                nextBoard = my_strategy.getNextBoard(move)
                score, path = self.abMinimax(nextBoard, depth, self.opponent, startTime, alpha, beta)
                # print 'alpha,beta =  ', alpha, beta
                if score > bestScore:
                    bestScore = score
                    bestMove = move

                if bestScore > beta:
                    path.append(bestMove)
                    return bestScore, path

                alpha = max(bestScore, alpha)

        if playerSide == self.opponent:
            bestScore = float("inf")
            for move in possiMoves:
                if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                    return bestScore, path
                nextBoard = my_strategy.getNextBoard(move)

                # print 'nextboard', nextBoard
                # print 'player', self.player
                # print 'depth', depth

                score, path = self.abMinimax(nextBoard, depth - 1, self.player, startTime, alpha, beta)

                if score < bestScore:
                    bestScore = score
                    bestMove = move

                if bestScore > beta:
                    path.append(bestMove)
                    return bestScore, path

                beta = min(bestScore, beta)


        path.append(bestMove)
        print 'path', path
        return bestScore, path

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


'''
        if playerSide == 1:
            v = float("-inf")
        else:
            v = float("inf")

        if depth == self.depthLimit:
            scores = []

        bestMoves = []

        if playerSide == 1:
            # print 'enter playerside 1'
            for move in possiMoves:
                if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                    return v
                nextBoard = my_strategy.getNextBoard(move)
                # print 'nextBoard,', nextBoard
                result = self.abMinimax(nextBoard, depth - 1, -1 * playerSide, startTime, alpha, beta)
                # print 'alpha,beta =  ', alpha, beta
                if result > v:
                    v = result
                    bestMoves = [move]
                elif result == v:
                    bestMoves.append(move)
                if depth == self.currentDepth:
                    scores.append(v)

                if v > beta:
                    return v
                alpha = max(v, alpha)

        else:
            # print 'enter playerside 2'
            for move in possiMoves:
                if self.timeLimit != -1 and time.clock() - startTime >= self.timeLimit:
                    return v
                nextBoard = my_strategy.getNextBoard(move)
                # print 'nextBoard,', nextBoard
                result = self.abMinimax(nextBoard, depth - 1, -1 * playerSide, startTime, alpha, beta)
                if result < v:
                    v = result
                    bestMoves = [move]
                elif result == v:
                    bestMoves.append(move)
                if depth == self.currentDepth:
                    scores.append(v)
                if v < alpha:
                    return v
                beta = min(v, beta)

        if depth == self.currentDepth:
            self.bestMove = choice(bestMoves)'''
