from HexGame import *
from Tkinter import *
from alphaBetaPruning import *
from mcts import *

'''
windowSize = 520
win = GraphWin("Hex Game", windowSize, windowSize - 100)
Hex = HexGame(win, 1, 8)
Hex.play()'''


class ModeChoice:
    def __init__(self, root):
        self.mode = None
        self.frame = Frame(root)
        self.frame.pack()
        self.root = root
        root.minsize(width=520, height=700)
        root.maxsize(width=520, height=700)
        root.title("Choose Mode")

        mode_1 = Button(self.frame, text='human vs. human', command=lambda: self.changeMode(1))
        mode_2 = Button(self.frame, text='alpha-beta pruning vs. human',command=lambda: self.changeMode(2))
        mode_3 = Button(self.frame, text='human vs. alpha-beta pruning', command=lambda: self.changeMode(3))
        mode_4 = Button(self.frame, text='Monte Carlo Tree search vs. human', command=lambda: self.changeMode(4))
        mode_5 = Button(self.frame, text='human vs. Monte Carlo Tree search', command=lambda: self.changeMode(5))
        mode_6 = Button(self.frame, text='alpha-beta pruning vs. Monte Carlo Tree search', command=lambda: self.changeMode(6))
        mode_7 = Button(self.frame, text='Monte Carlo Tree search vs. alpha-beta pruning', command=lambda: self.changeMode(7))
        mode_1.configure(width=60, height=6)
        mode_2.configure(width=60, height=6)
        mode_3.configure(width=60, height=6)
        mode_4.configure(width=60, height=6)
        mode_5.configure(width=60, height=6)
        mode_6.configure(width=60, height=6)
        mode_7.configure(width=60, height=6)

        mode_1.pack()
        mode_2.pack()
        mode_3.pack()
        mode_4.pack()
        mode_5.pack()
        mode_6.pack()
        mode_7.pack()

    def changeMode(self, newMode):
        self.mode = newMode
        self.root.quit()


class HexAgent:
    def __init__(self, win, size, mode):
        self.game = None
        self.mode = mode
        self.running = True
        self.holding = False
        self.win = win
        self.size = size

    def newGame(self):
        if self.mode == 1:
            self.game = HexGame(win=self.win, size=self.size, player1=humanPlayer(), player2=humanPlayer())
        elif self.mode == 2:
            self.game = HexGame(win=self.win, size=self.size,
                                player1=AlphaBetaPruningAgent(depthLimit=1, timeLimit=60, size=self.size),
                                player2=humanPlayer())
        elif self.mode == 3:
            self.game = HexGame(win=self.win, size=self.size,
                                player1=humanPlayer(),
                                player2=AlphaBetaPruningAgent(depthLimit=1, timeLimit=60, size=self.size))
        elif self.mode == 4:
            self.game = HexGame(win=self.win, size=self.size,
                                player1=monteCarloTreeSearch(depthLimit=1, timeLimit=60, size=self.size),
                                player2=humanPlayer())
        elif self.mode == 5:
            self.game = HexGame(win=self.win, size=self.size,
                                player1=humanPlayer(),
                                player2=monteCarloTreeSearch(depthLimit=1, timeLimit=60, size=self.size))
        elif self.mode == 6:
            self.game = HexGame(win=self.win, size=self.size,
                                player1=AlphaBetaPruningAgent(depthLimit=1, timeLimit=60, size=self.size),
                                player2=monteCarloTreeSearch(depthLimit=1, timeLimit=60, size=self.size))
        elif self.mode == 7:
            self.game = HexGame(win=self.win, size=self.size,
                                player1=monteCarloTreeSearch(depthLimit=1, timeLimit=60, size=self.size),
                                player2=AlphaBetaPruningAgent(depthLimit=1, timeLimit=60, size=self.size))

    def play(self):
        try:
            return self.game.play()
        except:
            import traceback
            traceback.print_exc()
            return None

    def isRunning(self):
        return self.running

    def hold(self):
        self.holding = True
        while self.holding:
            self.win.getMouse()

    def forceQuit(self):
        # if call quit() or exit() here, the main loop won't end
        self.holding = False
        self.running = False
        self.game.forceQuit()




def main():
    root = Tk()
    m = ModeChoice(root)
    root.mainloop()

    global win
    windowSize = 520
    win = GraphWin("Hex Game", windowSize, windowSize - 100)

    agent = HexAgent(win, 8, m.mode)
    win.master.protocol("WM_DELETE_WINDOW", agent.forceQuit)

    while agent.isRunning():
        agent.newGame()
        if agent.play() != None:
            agent.hold()


if __name__ == "__main__":
    win = None
    main()
