from copy import deepcopy
from util import *
from random import choice
import networkx as nx


class strategy:
    def __init__(self, board, size, playerSide):
        self.board = board
        self.size = size
        self.playerSide = playerSide
        self.mark1, self.mark2 = [0] * self.size, [0] * self.size

    '''
    def winner(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 1:
                    self.mark1[row] += 1
                elif self.board[row][col] == -1:
                    self.mark2[col] += 1
        if 0 in self.mark1 and 0 in self.mark2: return None
        if self.scan(1):
            return 1
        elif self.scan(-1):
            return 2
        else:
            return None

    def scan(self, player):
        adjacent = set()
        for i in range(self.size):
            iset = set()
            for j in range(self.size):
                if player == -1:
                    p = self.board[j][i]
                    # p = self.grid[j][i].getPlayer()
                    additem = (j, i)
                elif player == 1:
                    p = self.board[i][j]
                    # p = self.grid[i][j].getPlayer()
                    additem = (i, j)
                if player == p:
                    iset.add(additem)
            if iset.isdisjoint(adjacent) and i > 0:
                return False
            adjacent = self.getAdjacent(iset)
        return True
    '''
    def inRange(self, pos):
        return 0 <= pos[0] < self.size and 0 <= pos[1] < self.size

    def alreadyPlacedBlockNum(self):
        num = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    num += 1
        return num

    def winner(self):
        graph1 = self.currentNetworkGraph(1)
        graph2 = self.currentNetworkGraph(-1)
        source1 = (0, 1)
        target1 = (self.size + 1, 1)
        source2 = (1, 0)
        target2 = (1, self.size + 1)
        try:
            shortestLen1 = nx.shortest_path_length(graph1, source1, target1)
            #print "shortestLen1", shortestLen1
            if shortestLen1 == 1:
                return 1
        except:
            pass
        try:
            shortestLen2 = nx.shortest_path_length(graph2, source2, target2)
            #print "shortestLen2",shortestLen2
            if shortestLen2 == 1:
                return 2
        except:
            pass
        return None

    def getAdjacent(self, iset):
        adjacent = set()
        adVec = [Vector(v) for v in [(1, 0), (-1, 0), (1, -1), (-1, 1), (0, 1), (0, -1)]]
        for item in iset:
            for v in adVec:
                candidate = tuple(map(sum, zip(item, v)))
                if self.inRange(candidate): adjacent.add(candidate)
        return adjacent

    def getNeighbors(self, row, col):
        neighbors = set()
        adVec = [Vector(v) for v in [(1, 0), (-1, 0), (1, -1), (-1, 1), (0, 1), (0, -1)]]
        for v in adVec:
            candidate = tuple(map(sum, zip((row, col), v)))
            if self.inRange(candidate): neighbors.add(candidate)
        return neighbors

    def getRelevantNeighbors(self, row, col):
        relevantNeighbors = set()
        if self.playerSide == -1:
            adVec = [Vector(v) for v in [(1, -1), (-1, 1), (0, 1), (0, -1)]]
            for v in adVec:
                candidate = tuple(map(sum, zip((row, col), v)))
                if self.inRange(candidate): relevantNeighbors.add(candidate)
        else:
            adVec = [Vector(v) for v in [(1, 0), (-1, 0), (1, -1), (-1, 1)]]
            for v in adVec:
                candidate = tuple(map(sum, zip((row, col), v)))
                if self.inRange(candidate): relevantNeighbors.add(candidate)
        return relevantNeighbors

    def getGapNeighbors(self, row, col):
        '''return neighbors that are one col/row away from the node'''
        gapNeighbors = set()
        if self.playerSide == -1:
            adVec = [Vector(v) for v in [(0, -2, 1), (1, -2, 2), (2, -2, 1), (-2, 2, 1), (-1, 2, 2), (0, 2, 1)]]
            for v in adVec:
                candidate = tuple(map(sum, zip((row, col, 0), v)))
                if self.inRange(candidate): gapNeighbors.add(candidate)
        else:
            adVec = [Vector(v) for v in [(2, -2, 1), (2, -1, 2), (2, 0, 1), (-2, 0, 1), (-2, 1, 2), (-2, 2, 1)]]
            for v in adVec:
                candidate = tuple(map(sum, zip((row, col, 0), v)))
                if self.inRange(candidate): gapNeighbors.add(candidate)
        return gapNeighbors

    def getBridgeNeighbors(self, row, col):
        bridgeNeighbors = set()
        if self.playerSide == -1:
            adVec = [Vector(v) for v in [(1, -2), (-1, 2)]]
            for v in adVec:
                candidate = tuple(map(sum, zip((row, col), v)))
                if self.inRange(candidate): bridgeNeighbors.add(candidate)
        else:
            adVec = [Vector(v) for v in [(2, -1), (-2, 1)]]
            for v in adVec:
                candidate = tuple(map(sum, zip((row, col), v)))
                if self.inRange(candidate): bridgeNeighbors.add(candidate)

        return bridgeNeighbors

    def countConnected(self):
        counted = set()
        numCounted = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.playerSide:
                    for neighborRow, neighborCol in self.getNeighbors(row, col, self.playerSide):
                        if self.board[neighborRow][neighborCol] == self.playerSide and (
                                neighborRow, neighborCol) not in counted:
                            counted.add((neighborRow, neighborCol))
                            numCounted += 1
        return numCounted * self.playerSide

    def countUsefulConnected(self):
        counted = set()
        numCounted = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.playerSide:
                    for neighborRow, neighborCol in self.getRelevantNeighbors(row, col):
                        if self.board[neighborRow][neighborCol] == self.playerSide and (
                                neighborRow, neighborCol) not in counted:
                            counted.add((neighborRow, neighborCol))
                            numCounted += 1
        return numCounted * self.playerSide

    def countGapConnected(self):
        counted = set()
        numCounted = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.playerSide:
                    for neighborRow, neighborCol, value in self.getGapNeighbors(row, col):
                        if self.board[neighborRow][neighborCol] == self.playerSide and (
                                neighborRow, neighborCol) not in counted:
                            counted.add((neighborRow, neighborCol))
                            numCounted += value
        return numCounted * self.playerSide

    def getExpandedNum(self):
        expanded = set()
        if self.playerSide == 1:
            for row in range(self.size):
                for col in range(self.size):
                    if col in expanded:
                        continue
                    if self.board[row][col] == self.playerSide:
                        expanded.add(col)
        else:
            for row in range(self.size):
                if row in expanded:
                    continue
                for col in range(self.size):
                    if self.board[row][col] == self.playerSide:
                        expanded.add(row)
        return self.playerSide * len(expanded)

    def getNextBoard(self, move):
        row, col = move
        if self.board[row][col] != 0:
            print 'Invalid moves!'
            exit(0)
        nextBoard = deepcopy(self.board)
        nextBoard[row][col] = self.playerSide
        return nextBoard

    def inRange(self, pos):
        return 0 <= pos[0] < self.size and 0 <= pos[1] < self.size

    def getBlocksBetweenBridge(self, row, col, neighborRow, neighborCol):
        BlocksBetweenBridge = set()
        if self.playerSide == -1:
            if neighborRow == row - 1:
                BlocksBetweenBridge = [(row - 1, col + 1), (row, col + 1)]
            elif neighborRow == row + 1:
                BlocksBetweenBridge = [(row, col - 1), (row + 1, col - 1)]
        elif self.playerSide == 1:
            if neighborRow == row - 2:
                BlocksBetweenBridge = [(row - 1, col), (row - 1, col + 1)]
            elif neighborRow == row + 2:
                BlocksBetweenBridge = [(row + 1, col - 1), (row + 1, col)]
        return BlocksBetweenBridge

    def getAllPossiMoves(self):
        poss = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    poss.append((row, col))
        return poss

    def getPossiMoves(self):
        possiMoves = []
        lessPriorityMoves = []
        relevantNeighbors = []
        OpponentbridgeNeighbors = []
        bridge = []

        if self.winner() == 1 or self.winner() == 2:
            return possiMoves

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.playerSide:
                    currentRelevantNeighbors = self.getRelevantNeighbors(row, col)
                    for cx, cy in currentRelevantNeighbors:
                        if self.board[cx][cy] == 0:
                            relevantNeighbors.append((cx, cy))
                    # print "relevant Neighbors", relevantNeighbors
                    bridgeNeighbors = self.getBridgeNeighbors(row, col)

                    for neighbor in bridgeNeighbors:
                        neighborRow, neighborCol = neighbor
                        if self.board[neighborRow][neighborCol] == self.playerSide:
                            blocksBetweenBridge = self.getBlocksBetweenBridge(row, col, neighborRow, neighborCol)
                            num = 0
                            oppo = 0
                            for (blockx, blocky) in blocksBetweenBridge:
                                if self.board[blockx][blocky] == 0:
                                    mustOccupiedX, mustOccupiedY = blockx, blocky
                                    num += 1
                                elif self.board[blockx][blocky] == -self.playerSide:
                                    oppo += 1
                            if num == 1 and oppo == 1:
                                possiMoves.append((mustOccupiedX, mustOccupiedY))
                        if self.board[neighborRow][neighborCol] == 0:
                            bridge.append(neighbor)
                elif self.board[row][col] == -self.playerSide:
                    self.playerSide = -self.playerSide
                    for (neighborRow, neighborCol) in self.getBridgeNeighbors(row, col):
                        if self.board[neighborRow][neighborCol] == 0:
                            OpponentbridgeNeighbors.append((neighborRow, neighborCol))
                        elif self.board[neighborRow][neighborCol] == self.playerSide:
                            blocksBetweenBridge = self.getBlocksBetweenBridge(row, col, neighborRow, neighborCol)

                    self.playerSide = -self.playerSide

                elif self.board[row][col] == 0:
                    lessPriorityMoves.append((row, col))


        for n in OpponentbridgeNeighbors:
            if not n in possiMoves:
                possiMoves.append(n)
        for n in bridge:
            if not n in possiMoves:
                possiMoves.append(n)
        for n in relevantNeighbors:
            if not n in possiMoves:
                possiMoves.append(n)
        for n in lessPriorityMoves:
            if not n in possiMoves:
                possiMoves.append(n)
        # print "possible moves", possiMoves
        l = list(set(possiMoves))
        l.sort(key=possiMoves.index)

        return l

    def greatFirstMove(self):
        greatFirstMoves = []
        center = self.size / 2
        possiGreatFirstMove = [[center, center], [center - 1, center], [center, center - 1], [center - 1, center - 1]]
        for m in possiGreatFirstMove:
            row, col = m
            if self.board[row][col] == 0:
                greatFirstMoves.append(m)
        greatFirstMove = choice(greatFirstMoves)
        return greatFirstMove

    def init_NetworkGraph(self, playerSide):
        graph = nx.Graph()
        for row in range(self.size):
            for col in range(self.size):
                graph.add_node((row + 1, col + 1))
        for node in graph.nodes():
            x, y = node
            for neighbor in self.getNeighbors(x - 1, y - 1):
                neighborx, neighbory = neighbor
                if (neighborx + 1, neighbory + 1) in graph.nodes():
                    # print "node and neighbor", node, (neighborx + 1, neighbory + 1)
                    graph.add_edge(node, (neighborx + 1, neighbory + 1))

        if playerSide == -1:
            startNode = (1, 0)
            graph.add_node(startNode)
            for row in range(self.size):
                startNodeNeighbor = (row + 1, 1)
                graph.add_edge(startNode, startNodeNeighbor)

            endNode = (1, self.size + 1)
            graph.add_node(endNode)
            for row in range(self.size):
                endNodeNeighbor = (row + 1, self.size)
                graph.add_edge(endNode, endNodeNeighbor)

        elif playerSide == 1:
            startNode = (0, 1)
            graph.add_node(startNode)
            for col in range(self.size):
                startNodeNeighbor = (1, col + 1)
                graph.add_edge(startNode, startNodeNeighbor)

            endNode = (self.size + 1, 1)
            graph.add_node(endNode)
            for col in range(self.size):
                endNodeNeighbor = (self.size, col + 1)
                graph.add_edge(endNode, endNodeNeighbor)

        return graph

    def currentNetworkGraph(self, playerSide):
        graph = self.init_NetworkGraph(playerSide)
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == playerSide:
                    node = (row + 1, col + 1)
                    neighbors = graph.neighbors(node)
                    graph.remove_node(node)
                    for neighbor1 in neighbors:
                        for neighbor2 in neighbors:
                            if neighbor1 != neighbor2:
                                graph.add_edge(neighbor1, neighbor2)

                if self.board[row][col] == -playerSide:
                    node = (row + 1, col + 1)
                    graph.remove_node(node)
        return graph

    def getSecondShortestPathLength(self, playerSide):

        graph = self.currentNetworkGraph(playerSide)
        # print 'possiMoves', self.getPossiMoves()
        if playerSide == 1:
            source = (0, 1)
            target = (self.size + 1, 1)
        elif playerSide == -1:
            source = (1, 0)
            target = (1, self.size + 1)

        distance_to_source = nx.single_source_shortest_path_length(graph, source)
        del distance_to_source[source]
        distance_to_target = nx.single_source_shortest_path_length(graph, target)
        del distance_to_target[target]

        shortest_set = {}
        opponentLenSet = []
        # print "distance_to_source", distance_to_source
        # print "distance_to_target", distance_to_target

        OpponentGraph = self.currentNetworkGraph(-playerSide)
        for move in self.getPossiMoves():
            # print 'move', move
            row, col = move
            node = (row + 1, col + 1)
            # print "move", move
            # print "board", self.board
            # print 'distance_to_source[node]', distance_to_source[node]
            # print 'distance_to_target[node]', distance_to_target[node]
            opponenLen = self.OpponentShortestPathLen(OpponentGraph,node,-playerSide)
            opponentLenSet.append(opponenLen)
            #print "opponent", opponenLen
            try:
                #shortest_set[node] = (distance_to_source[node] + distance_to_target[node])
                shortest_set[node] = (distance_to_source[node] + distance_to_target[node])
            except:
                pass
                # print "shortest set", shortest_set[node]
                # print "shortest set", shortest_set
        '''second shortest
        try:
            shortest_length = min(shortest_set.values())
            for node in shortest_set:
                if shortest_set[node] == shortest_length:
                    del shortest_set[node]
                    break
            second_shortest = min(shortest_set.values())
        except:
            second_shortest = self.size + 1
        # print "heuristic", self.size + 1 - second_shortest
        return (self.size + 1 - second_shortest)

        '''


        # shortest
        try:
            shortest_length = min(shortest_set.values())
        except:
            shortest_length = float('inf')

        '''
        if playerSide == 1:
            return (self.size + 1 - shortest_length)
        else:
            return min(opponentLenSet)'''
        return (self.size + 1 - shortest_length)


    def OpponentShortestPathLen(self,graph,node,playerSide):
        graph.remove_node(node)
        if playerSide == 1:
            source = (0, 1)
            target = (self.size + 1, 1)
        elif playerSide == -1:
            source = (1, 0)
            target = (1, self.size + 1)
        try:
            paths = nx.all_shortest_paths(graph, source, target)
            for p in paths:
                #print "paths", len(p)
                return len(p)
        except:
            return self.size + 1


    def getGoodMoves(self):
        if self.getMustWinMoves() != []:
            return self.getMustWinMoves()
        if self.alreadyPlacedBlockNum() <= 12:
            return self.getPossiMoves()
            return self.getPossiMoves()
        else:
            for row in range(self.size):
                for col in range(self.size):
                    if self.isDeadCell(row, col):
                        self.board[row][col] == -self.playerSide
                        # print "this cell is dead", (row,col)
            return self.getPossiMoves()


    def isDeadCell(self, row, col):
        'A cell is dead if it does not lie in any minimal path from source to target'
        graph = self.currentNetworkGraph(self.playerSide)
        if self.playerSide == 1:
            source = (0, 1)
            target = (self.size + 1, 1)
        elif self.playerSide == -1:
            source = (1, 0)
            target = (1, self.size + 1)
        try:
            paths = nx.all_shortest_paths(graph, source, target)
            for p in paths:
                if (row + 1, col + 1) in p:
                    return False
        except:
            pass
        return True

    def getMustWinMoves(self):
        if self.alreadyPlacedBlockNum() < self.size * 2 - 2:
            return []
        else:
            graph = self.currentNetworkGraph(self.playerSide)
            if self.playerSide == 1:
                source = (0, 1)
                target = (self.size + 1, 1)
            elif self.playerSide == -1:
                source = (1, 0)
                target = (1, self.size + 1)
            actions = []
            try:
                paths = nx.all_shortest_paths(graph, source, target)
                for p in paths:
                    if len(p) > 3:
                        return []
                    x, y = p[1]
                    actions.append((x - 1, y - 1))
            except:
                pass
            return actions

    def getMustMoves(self):
        actions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.playerSide:
                    bridgeNeighbors = self.getBridgeNeighbors(row, col)

                    for neighbor in bridgeNeighbors:
                        neighborRow, neighborCol = neighbor
                        if self.board[neighborRow][neighborCol] == self.playerSide:
                            blocksBetweenBridge = self.getBlocksBetweenBridge(row, col, neighborRow, neighborCol)
                            num = 0
                            oppo = 0
                            for (blockx, blocky) in blocksBetweenBridge:
                                if self.board[blockx][blocky] == 0:
                                    mustOccupiedX, mustOccupiedY = blockx, blocky
                                    num += 1
                                elif self.board[blockx][blocky] == -self.playerSide:
                                    oppo += 1
                            if num == 1 and oppo == 1:
                                actions.append((mustOccupiedX, mustOccupiedY))
        return actions

    def getDeadCells(self):
        deadCell = []
        for row in range(self.size):
            for col in range(self.size):
                if self.isDeadCell(row,col):
                    deadCell.append((row,col))
        return deadCell

    def isTerminal(self):
        possi = self.getAllPossiMoves()
        if possi == []:
            return True
        return False



'''
    def getMustReplyMove(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.playerSide:'''

'''
G=nx.Graph()
G.add_path([0,1,5,2])
G.add_path([0,1,5,7,2])
G.add_path([0,10,2])
for p in nx.all_shortest_paths(G,source=0,target=2):
    print p
    for x in p:
        print x
'''

'''


    def winner(self):

        playerSide = self.playerSide
        graph = self.currentNetworkGraph(playerSide)
        if playerSide == 1:
            source = (0, 1)
            target = (self.size + 1, 1)
        elif playerSide == -1:
            source = (1, 0)
            target = (1, self.size + 1)

        distance_to_source = nx.single_source_shortest_path_length(graph, source)
        del distance_to_source[source]

        distance_to_target = nx.single_source_shortest_path_length(graph, target)
        del distance_to_target[target]

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == playerSide:
                    node = (row + 1, col + 1)

                try:
                    shortest_length = distance_to_source[node] + distance_to_target[node]
                    if shortest_length == 2:
                        if playerSide == 1:
                            return 1
                        else:
                            return 2
                except:
                    pass
        return None
'''
