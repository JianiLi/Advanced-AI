import informedSearch
import random
import time


# Module Classes

class sixteenPuzzleState:
    def __init__(self, numbers):
        """
          Constructs a new 16 puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 15 representing an
          instance of the eight puzzle. 0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

          represents the 16 puzzle:
            ---------------------
            |  1 |    |  2 |  3 |
            ---------------------
            |  4 |  5 |  6 |  7 |
            ---------------------
            |  8 |  9 | 10 | 11 |
            ---------------------
            | 12 | 13 | 14 | 15 |
            ---------------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:]  # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(4):
            self.cells.append([])
            for col in range(4):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal(self):
        """
          Checks to see if the puzzle is in its goal state.

            ---------------------
            |  1 |  2 |  3 |  4 |
            ---------------------
            |  5 |  6 |  7 |  8 |
            ---------------------
            |  9 | 10 | 11 | 12 |
            ---------------------
            | 13 | 14 | 15 |    |
            ---------------------

        """
        current = 1
        for row in range(4):
            for col in range(4):
                if current != self.cells[row][col]:
                    return False
                current += 1
                if current == 16:
                    return True
        return True

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if col != 0:
            moves.append('left')
        if row != 3:
            moves.append('down')
        if col != 3:
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new sixteenPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current sixteenPuzzle
        newPuzzle = sixteenPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        for row in range(4):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (21))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col <= 9:
                    if col == 0:
                        col = ' '
                    rowLine = rowLine + '  ' + col.__str__() + ' |'
                else:
                    rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()


# TODO: Implement The methods in this class

class SixteenPuzzleSearchProblem(informedSearch.SearchProblem):
    """
      Implementation of a SearchProblem for the  sixteen Puzzle domain

      Each state is represented by an instance of an sixteenPuzzle.
    """

    def __init__(self, puzzle):
        "Creates a new sixteen PuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getInverseAction(self,action):
        if action == 'up':
            return 'down'
        elif action == 'left':
            return 'right'
        elif action == 'right':
            return 'left'
        elif action == 'down':
            return 'up'

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

def HeuristicOne(state, problem):
    '''heuristic 1: number of misplaced tiles'''
    goalState = sixteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]).cells
    state = state.cells

    heuristic = 0
    for row in range(4):
        for col in range(4):
            if state[row][col] != goalState[row][col]:
                heuristic = heuristic + 1
    return heuristic


def HeuristicTwo(state, problem):
    '''heuristic 2: manhattan distance'''
    goalState = sixteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]).cells
    state = state.cells

    heuristic = 0
    for goalRow in range(4):
        for goalCol in range(4):
            for row in range(4):
                for col in range(4):
                    if goalState[goalRow][goalCol] != 0:
                        if state[row][col] == goalState[goalRow][goalCol]:
                            heuristic = heuristic + manhattanDistance([row, col], [goalRow, goalCol])
    return heuristic


def manhattanDistance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def createRandomSixteenPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = sixteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':

    #puzzle_random2 = createRandomSixteenPuzzle(100)

    puzzle_first_configuration = sixteenPuzzleState([9, 5, 7, 4, 1, 0, 3, 8, 13, 10, 2, 12, 14, 6, 11, 15])
    puzzle_second_configuration = sixteenPuzzleState([3, 6, 9, 4, 5, 2, 8, 11, 10, 0, 15, 7, 13, 1, 14, 12])
    puzzle_piazza = sixteenPuzzleState([5,3,0,4,7,2,6,8,1,9,10,11,13,14,15,12])
    puzzle_random1 = sixteenPuzzleState([0,2,1,3,5,11,7,4,6,9,10,8,13,14,15,12])
    puzzle_random2 = sixteenPuzzleState([5,1,3,2,10,0,4,7,6,9,11,8,13,14,15,12])

    NonePuzzle = sixteenPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    puzzle_num = int(raw_input(
        'Choose the configuration:\n'
        '1 - the first given configuration on blackboard\n'
        '2 - the second given configuration on blackboard\n'
        '3 - the given configuration on Piazza\n'
        '4 - No.1 random generated configuration\n'
        '5 - No.2 random generated configuration\n'
        'Then press enter:  '))
    print '---------------------'
    if puzzle_num == 1:
        puzzle = puzzle_first_configuration
    elif puzzle_num == 2:
        puzzle = puzzle_second_configuration
    elif puzzle_num == 3:
        puzzle = puzzle_piazza
    elif puzzle_num == 4:
        puzzle = puzzle_random1
    elif puzzle_num == 5:
        puzzle = puzzle_random2
    else:
        print 'You have entered an wrong number, please run again!'

    problem = SixteenPuzzleSearchProblem(puzzle)

    heuristic_num = int(raw_input(
        'Choose the heuristic function\n1 - number of misplaced tiles\n2 - manhattan distance\nThen press enter:  '))
    print '---------------------'
    if heuristic_num == 1:
        heuristic = HeuristicOne
    elif heuristic_num == 2:
        heuristic = HeuristicTwo
    else:
        print 'You have entered an wrong number, please run again!'

    algorithm_num = int(raw_input(
        'Choose the algorithm you want to implement\n1 - A*\n2 - IDA*\n3 - AWA*\n4 - ARA*\nThen press enter: '))
    print('Your chosen puzzle:')
    print(puzzle)
    print 'Running...'
    print '---------------------'

    time_start = time.time()
    if algorithm_num == 1:
        path = informedSearch.aStarSearch(problem,heuristic)
    elif algorithm_num == 2:
        path = informedSearch.IDAStarSearch(problem,heuristic)
    elif algorithm_num == 3:
        path = informedSearch.AnytimeWAstarSearch(problem, NonePuzzle,heuristic)
    elif algorithm_num == 4:
        path = informedSearch.AnytimeReparingAstarSearch(problem, NonePuzzle,heuristic)
    else:
        print 'You have entered an wrong number, please run again!'
    time_end = time.time()
    print '\a'
    print('Algorithm found the optimal solution of %d moves: %s' % (len(path), str(path)))
    print '---------------------'
    print 'Total running rime:', time_end - time_start, 's'
    print '---------------------'

    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
        print(curr)

        raw_input("Press return for the next state...")  # wait for key stroke
        i += 1
