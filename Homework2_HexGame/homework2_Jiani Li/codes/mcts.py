from math import sqrt, log
import random
import time
from strategies import *
import copy
import numpy as np


class MCTSNode(object):
    def __init__(self, board, size, playerSide, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.visits = 0
        self.value = 0
        self.children = []
        self.size = size
        self.playerSide = playerSide
        self.myStrategy = strategy(self.board, self.size, self.playerSide)
        self.possiMoves = self.myStrategy.getAllPossiMoves()
        self.frontier = copy.deepcopy(self.possiMoves)
        random.shuffle(self.frontier)

    def add_child(self):
        assert self.frontier != []
        randomMove = self.frontier.pop()
        newBoard = self.myStrategy.getNextBoard(randomMove)
        newNode = MCTSNode(newBoard, self.size, -1 * self.playerSide, self, randomMove)
        self.children.append(newNode)
        return newNode

    def isTerminal(self):
        if self.possiMoves == []:
            return True
        return False

    def isFullyExpanded(self):
        return self.frontier == []


class monteCarloTreeSearch:
    def __init__(self, depthLimit, timeLimit, size, iterations=20):
        self.depthLimit = depthLimit
        self.timeLimit = timeLimit
        self.bestMove = None
        self.size = size
        self.iterations = iterations

    def getMove(self, board, playerSide):
        self.run_game = 0
        self.treeNum = 0
        self.root = MCTSNode(board, self.size, playerSide)
        self.root.PlayerSide = playerSide
        # print "root playerSide", rootPlayerSide
        startTime = time.clock()
        if self.root.myStrategy.getMustWinMoves() != []:
            return choice(self.root.myStrategy.getMustWinMoves())
        elif self.root.myStrategy.getMustMoves() != []:
            return choice(self.root.myStrategy.getMustMoves())
        #for i in range(self.iterations):
        while time.clock() - startTime < self.timeLimit:
            node = self.treePolicy(self.root)
            # print "node", len(node.frontier)
            ###print 'selected node board', node.board
            #print 'frontier length',len(node.frontier)
            # print 'side', node.playerSide
            # print 'possiMoves', node.possiMoves
            reward = self.defaultPolicy(node)
            # print 'reward=', reward
            self.backpropagate(node, reward)
            self.run_game += 1
        print "the number of simulations performed:", self.run_game
        print "the max size of the search tree for all moves", self.treeNum
        self.bestMove = self.selectBestMove(self.root)
        return self.bestMove

    def treePolicy(self, node):
        while not node.isTerminal():

            # print "node board", node.board
            if not node.isFullyExpanded():
                #print "frontier",node.frontier
                self.treeNum += 1
                return self.expand(node)
            else:
                node = self.selectBestChild(node)
                if len(self.root.possiMoves) - len(node.possiMoves) >= 3:
                    return node
                #print "self.selectBestChild(node)", node.board
            # print "node", node.board
        return node

    def defaultPolicy(self, node):
        thisNodePlayerside = node.playerSide
        myStrategy = node.myStrategy

        while not myStrategy.isTerminal():
            possiMoves = myStrategy.getAllPossiMoves()
            # print 'possimoves', possiMoves
            move = random.choice(possiMoves)
            board = myStrategy.getNextBoard(move)
            playerSide = -myStrategy.playerSide
            myStrategy = strategy(board, self.size, playerSide)
        # print "board", myStrategy.board
        # print "winner", myStrategy.winner()
        if myStrategy.winner() == 1 and thisNodePlayerside == 1:
            # print "winner is 1",self.run_game
            reward = -1
        elif myStrategy.winner() == 2 and thisNodePlayerside == -1:
            # print "winner is 2",self.run_game
            reward = -1
        else:
            reward = 1
            # print "winner is *",self.run_game
        return reward

    def backpropagate(self, node, reward):
        node.visits += 1
        node.value += reward
        if node.parent:
            # print "node.parent",node.parent.board
            self.backpropagate(node.parent, -reward)

    def expand(self, node):
        return node.add_child()

    def selectBestChild(self, node):
        bestChild_uct = -float('inf')
        bestChild = node.children[0]
        c = sqrt(2)
        for child in node.children:
            #print "child value", child.value, child.visits,self.uct(child, c),child.board
            if self.uct(child, c) > bestChild_uct:
                bestChild_uct = self.uct(child, c)
                bestChild = child

        return bestChild

    def selectBestMove(self, node):
        bestChild = max(node.children, key=lambda child: self.uct(child, 0))
        print "Best Child Value: ", str(bestChild.value)
        print "Best Child Visits: ", str(bestChild.visits)
        return bestChild.move

    def uct(self, node, c):
        w = float(node.value)
        n = float(node.visits)
        N = float(node.parent.visits)
        uct = w / n + c * sqrt(log(N) / n)
        return uct
