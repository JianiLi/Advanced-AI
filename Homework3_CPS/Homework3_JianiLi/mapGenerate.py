import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np


class Node:
    def __init__(self, x, y, colorNum):
        self.x = x
        self.y = y
        self.neighborSet = set()
        self.color = None

        if colorNum == 2:
            self.remainingColorSet = ['r', 'g']
        elif colorNum == 3:
            self.remainingColorSet = ['r', 'g', 'b']
        elif colorNum == 4:
            self.remainingColorSet = ['r', 'g', 'b', 'y']

        self.conflictSet = []
        self.triedColors = []

    def isNeighbor(self, node):
        return node in self.neighborSet

    def connect(self, node):
        node.neighborSet.add(self)
        self.neighborSet.add(node)

    def distance(self, node):
        return math.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def unAssignedNeighborSet(self):
        return self.neighborSet - set(self.conflictSet)

    def getRemainingColorSet(self):
        return self.remainingColorSet

    def removeFromRemainingColorSet(self, color):
        self.remainingColorSet.remove(color)

    def addToRaminingColorSet(self, color):
        self.remainingColorSet.append(color)


class Vector:
    def __init__(self, start, end):
        self.start, self.end = start, end
        self.xVector = end.x - start.x
        self.yVector = end.y - start.y

    def negative(self):
        return Vector(self.end, self.start)

    def product(self, vector):
        return self.xVector * vector.yVector - vector.xVector * self.yVector

    def isIntersection(self, vector):
        A = self.start
        B = self.end
        C = vector.start
        D = vector.end
        if A == C or A == D or B == C or B == D:
            return False
        else:
            AC = Vector(A, C)
            AD = Vector(A, D)
            BC = Vector(B, C)
            BD = Vector(B, D)
            CA = AC.negative()
            CB = BC.negative()
            DA = AD.negative()
            DB = BD.negative()
            return (AC.product(AD) * BC.product(BD) <= 0) and (CA.product(CB) * DA.product(DB) <= 0)


def Map_generate(colorNum, nodeNum):
    startTime = time.time()
    nodeSet = set()
    returnNodes = set()
    connections = []
    candidateNeighbors = {}
    X = np.random.rand(nodeNum, 2)
    for n in range(nodeNum):
        node = Node(X[n][0], X[n][1], colorNum)
        nodeSet.add(node)
        returnNodes.add(node)

    for node in nodeSet:
        plt.plot(node.x, node.y, 'ko', markersize=10)
    for node in nodeSet:
        candidateNeighbors[node] = nodeSet - set([node])

    while nodeSet:
        intersect = False
        random_pick_node = random.choice(tuple(nodeSet))
        if candidateNeighbors[random_pick_node]:
            closestNeighbor = min(candidateNeighbors[random_pick_node], key=random_pick_node.distance)
        else:
            nodeSet.remove(random_pick_node)
            continue
        candidateNeighbors[random_pick_node].remove(closestNeighbor)
        newConnect = Vector(random_pick_node, closestNeighbor)
        for c in connections:
            if newConnect.isIntersection(c):
                intersect = True
                break
        if not intersect:
            random_pick_node.connect(closestNeighbor)
            connections.append(Vector(random_pick_node, closestNeighbor))
            x = [random_pick_node.x, closestNeighbor.x]
            y = [random_pick_node.y, closestNeighbor.y]
            plt.plot(x, y, linewidth=0.5, color='k')
    timeSpan = time.time() - startTime
    print "time used for generate uncolored map:", "%.2f" % timeSpan, "s"
    title = "Uncolored map" + " (" + str(colorNum) + " colors " + str(nodeNum) + " nodes)"
    plt.title(title)
    plt.show()
    return returnNodes


def map_color(nodeSet, colorNum, nodeNum, lastNode=None, lastState=None, algorithm=None):
    for node in nodeSet:
        for neighbor in node.neighborSet:
            x = [node.x, neighbor.x]
            y = [node.y, neighbor.y]
            plt.plot(x, y, linewidth=0.5, color='k')

    if not lastState:
        for node in nodeSet:
            if node.color:
                plt.plot(node.x, node.y, node.color + 'o', markersize=10)
            elif node == lastNode:
                plt.plot(node.x, node.y, 'kx', markersize=8)
            else:
                plt.plot(node.x, node.y, 'wo', markersize=8)
    else:
        for node in lastState:
            try:
                plt.plot(node.x, node.y, node.color + 'o', markersize=10)
            except:
                pass

        for node in nodeSet:
            if node.x == lastNode.x and node.y == lastNode.y:
                plt.plot(node.x, node.y, 'kx', markersize=8)
            else:
                plt.plot(node.x, node.y, 'wo', markersize=0)
    title = "Map coloring of " + algorithm + " (" + str(colorNum) + " colors " + str(nodeNum) + " nodes)"
    plt.title(title)
    plt.show()
