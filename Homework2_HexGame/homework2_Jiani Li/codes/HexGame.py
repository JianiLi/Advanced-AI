from HexGUI import *
from strategies import *


class Player:
    def __init__(self, color, num):
        self.color = color
        self.num = num
        self.side = None

    def getColor(self):
        return self.color

    def getNum(self):
        return self.num

    def setSide(self, side):
        self.side = side

    def getSide(self):
        return self.side


def print_block(i):
    if i == 1:
        return u'\u25CF'
    if i == -1:
        return u'\u25CB'
    return u'\u00B7'


class humanPlayer:
    def getMove(self, win, GUI):
        while not win.isClosed():
            try:
                p = win.getMouse()
                co = GUI.locate(p)
            except:
                return None
            if co != ():
                return co


class HexGame(object):
    def __init__(self, win, size, player1, player2):
        self.running = True
        self.win = win
        self.size = size
        self.p1 = Player("red", 1)
        self.p1.setSide(1)
        self.p2 = Player("blue", 2)
        self.p2.setSide(-1)
        self.players = (self.p1, self.p2)
        self.currentPlayer = 1
        self.GUI = None
        self.turnText = None
        self.player1 = player1
        self.player2 = player2
        windowSize = 520
        self.GUI = HexGUI(self.win, self.size, 20, [80, 100])
        self.turnText = Text(Point(windowSize / 3, windowSize / 10),
                             "Player " + str(self.currentPlayer) + "'s Turn   (thinking)")
        self.turnText.setSize(20)
        self.turnText.draw(self.win)
        self.board = self.GUI.getBoard()

    def print_board(self):
        result = (" " + u"\u25a0") * self.GUI.size + u" \u25E9\n"
        for i in range(self.GUI.size):
            result += " " * i + u"\u25A1" + " "
            for j in range(self.GUI.size):
                result += print_block(self.GUI.board[i, j]) + " "
            result += u"\u25A1" + "\n"
        result += " " * (self.GUI.size) + u"\u25EA" + (" " + u"\u25a0") * self.GUI.size + "\n" + "\n"
        label = str(self.players[self.currentPlayer].getSide()) + "'s turn to place a " + print_block(
            self.players[self.currentPlayer].getSide()) + " piece"
        return result + label

    def switchPlayer(self):
        self.currentPlayer = (self.currentPlayer + 1) % 2
        self.turnText.setText("Player " + str(self.currentPlayer + 1) + "'s Turn   (thinking)")

    def isRunning(self):
        return self.running

    def forceQuit(self):
        self.running = False
        self.win.mouseX = self.win.mouseY = []  # get out of the getMouse() loop
        self.win.close()
        exit(0)

    def player1Go(self):
        playerSide = self.players[self.currentPlayer].getSide()
        if self.player1.__dict__ == humanPlayer().__dict__:
            co = self.player1.getMove(self.win, self.GUI)
        else:
            my_strategy = strategy(self.board, self.size, playerSide)
            #print "len", len(my_strategy.getPossiMoves())
            if my_strategy.alreadyPlacedBlockNum() <= 1:
                co = my_strategy.greatFirstMove()
            else:
                co = self.player1.getMove(self.board, playerSide)
        print "player1 move =", co
        # print "board", self.board
        if self.GUI.placePiece(co, self.players[self.currentPlayer]):
            # print 'playerside', playerSide
            my_strategy = strategy(self.board, self.size, playerSide)
            winner = my_strategy.winner()
            # print "winner =", winner
            if winner == None:
                self.switchPlayer()
            elif winner == self.currentPlayer + 1:
                self.turnText.setTextColor("magenta")
                self.turnText.setText("Player " + str(winner) + " wins.")
                return winner
        return None

    def player2Go(self):
        playerSide = self.players[self.currentPlayer].getSide()

        if self.player2.__dict__ == humanPlayer().__dict__:
            co = self.player2.getMove(self.win, self.GUI)
        else:
            # my_strategy = strategy(self.board, self.size, playerSide)
            # if self.size * self.size - len(my_strategy.getPossiMoves()) <= 1:
            # co = my_strategy.greatFirstMove()
            # else:
            co = self.player2.getMove(self.board, playerSide)
        print "player2 move =", co
        # print "board", self.board
        if self.GUI.placePiece(co, self.players[self.currentPlayer]):
            # print 'playerside', playerSide
            my_strategy = strategy(self.board, self.size, playerSide)
            winner = my_strategy.winner()
            if winner == None:
                self.switchPlayer()
            elif winner == self.currentPlayer + 1:
                self.turnText.setTextColor("magenta")
                self.turnText.setText("Player " + str(winner) + " wins.")
                return winner
        else:
            return False
        return None

    def play(self):
        self.currentPlayer = 0
        while self.running:

            self.turnText.setTextColor(self.players[self.currentPlayer].getColor())
            times = time.clock()
            winner = self.player1Go()
            timeSpan = time.clock() - times
            print "time used for this move:" + str(timeSpan) +"\n" + self.print_board()
            if winner == self.currentPlayer + 1:
                print str(self.players[self.currentPlayer].getSide()) + " wins"
                return winner

            self.turnText.setTextColor(self.players[self.currentPlayer].getColor())
            times = time.clock()
            winner = self.player2Go()
            timeSpan = time.clock() - times
            print "time used for this move:" + str(timeSpan) +"\n" + self.print_board()
            if winner == self.currentPlayer + 1:
                print str(self.players[self.currentPlayer].getSide()) + " wins"
                return winner

        return None
