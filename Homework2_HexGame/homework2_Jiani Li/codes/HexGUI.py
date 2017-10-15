import math
from lib.graphics import *
from util import *
import numpy as np
from copy import deepcopy

Sq3 = math.sqrt(3)
halfSq3 = math.sqrt(3) / 2


class HexMove:
    def __init__(self, player, pos):
        self.player = player
        self.pos = pos

    def getPlayer(self): return self.player

    def getPos(self): return self.pos


class HexBlock:  # one piece of the Hex GUI
    delta_x = Vector([-halfSq3, 0, halfSq3, halfSq3, 0, -halfSq3])
    delta_y = Vector([0.5, 1, 0.5, -0.5, -1, -0.5])

    def __init__(self, win, center, edgeLen):
        self.win = win
        self.x, self.y = center
        self.edgeLen = edgeLen
        self.player = None
        points = []
        for i in range(6):
            points.append(Point(self.x + edgeLen * HexBlock.delta_x[i], self.y + edgeLen * HexBlock.delta_y[i]))
        self.region = Polygon(points)
        self.region.setWidth(2)
        self.region.draw(self.win)
        self.piece = Circle(Point(self.x, self.y), edgeLen / 2)

    def undraw(self):
        self.region.undraw()
        self.piece.undraw()

    def clickIn(self, x, y):
        dv = Vector([x - self.x, y - self.y])
        Vec = [Vector(v) for v in [(0, 1), (halfSq3, 0.5), (halfSq3, -0.5)]]
        limit = self.edgeLen
        for v in Vec:
            if abs(v * dv) > limit:
                return False
        return True

    def placePiece(self, player):
        if self.player == None:
            self.piece.setFill(player.getColor())
            self.piece.draw(self.win)
            self.player = player.getNum()
            return True
        else:
            return False

    def getCenter(self):
        return self.x, self.y

    def getPlayer(self):
        return self.player



'''
windowSize = 600
win = GraphWin("hex", windowSize, windowSize)
HexBlock(win, [100, 200], 20)
time.sleep(20)'''


class HexGUI:
    def __init__(self, win, size, gridLen, initCenter):
        self.win = win
        self.size = size
        self.gridLen = gridLen
        self.grid = []
        self.board = np.zeros([self.size, self.size], int)
        for i in range(size):
            self.grid.append([])
        self.xo, self.yo = initCenter
        newCenter_row = initCenter
        for row in range(size):
            newCenter_col = newCenter_row
            for col in range(size):
                newGrid = HexBlock(win, newCenter_col, gridLen)
                self.grid[row].append(newGrid)
                newCenter_col = (newCenter_col[0] + Sq3 * gridLen, newCenter_col[1])
            newCenter_row = (newCenter_row[0]+halfSq3*gridLen , newCenter_row[1] + 1.5 *gridLen)
        self.drawOuterLines()

    def drawOuterLines(self):
        self.lines = []
        p1 = Point(self.xo - Sq3 * self.gridLen, self.yo - self.gridLen)
        p2 = Point(self.xo + (self.size - 2.0 / 3) * Sq3 * self.gridLen, self.yo - self.gridLen)
        p3 = Point(self.xo + (3.0 / 2 * self.size - 1.0 / 2) * Sq3 * self.gridLen,
                   self.yo + (3.0 / 2 * self.size - 1.0 / 2) * self.gridLen)
        p4 = Point(self.xo + (self.size / 2.0 - 5.0 / 6) * Sq3 * self.gridLen,
                   self.yo + (3.0 / 2 * self.size - 1.0 / 2) * self.gridLen)
        ps = [p1, p2, p3, p4]
        for i in range(4):
            self.lines.append(Line(ps[i], ps[(i + 1) % 4]))
            if i % 2:
                self.lines[i].setOutline("blue")
            else:
                self.lines[i].setOutline("red")
            self.lines[i].setWidth(2)
            self.lines[i].draw(self.win)

    def locate(self, p):
        x, y = p.getX(), p.getY()
        for cord1 in range(self.size):
            for cord2 in range(self.size):
                if self.grid[cord1][cord2].clickIn(x, y):
                    return (cord1, cord2)
        return ()

    def placePiece(self, cord, player):
        success = self.grid[cord[0]][cord[1]].placePiece(player)
        if not success: return False
        s = player.getSide()
        self.board[cord[0]][cord[1]] = s
        return success

    def getGrid(self):
        return self.grid

    def getBoard(self):
        return self.board





'''
windowSize = 520
win = GraphWin("hex", windowSize, windowSize - 100)
HexBoard(win, 9, 20, [50, 100])
time.sleep(200)'''
