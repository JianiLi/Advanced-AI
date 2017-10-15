from __future__ import division
import heapq, random
import time


class SearchProblem:
    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()

    def getInverseAction(self, action):
        util.raiseNotDefined()

def aStarSearch(problem, heuristic):

    open = PriorityQueue()
    start = problem.getStartState()
    open.push((start, []), heuristic(start, problem))
    inClosed = []
    num_closed = 0
    num_open = 1
    num_moved = 0  # moved from the Closed list to the Open list because shorter paths were found from the start node to this node.
    num_openPlusClosed = 1
    max_open_num = 0

    while not open.isEmpty():
        node, actions = open.pop()
        if problem.isGoalState(node):
            printRes(num_open, num_closed, num_moved, num_openPlusClosed)
            return actions
        if node not in inClosed:
            inClosed.append(node)
            num_closed += 1
            for coord, direction, steps in problem.getSuccessors(node):
                if (actions == [] or not problem.getInverseAction(direction) == actions[-1]) and coord not in inClosed:
                    newActions = actions + [direction]
                    cost = problem.getCostOfActions(newActions) + heuristic(coord, problem)
                    open.update((coord, newActions), cost)
                    num_open += 1
        '''if len(open.elementList()) > max_open_num:
            max_open_num = len(open.elementList())'''
        if len(inClosed) + len(open.elementList()) > num_openPlusClosed:
            num_openPlusClosed = len(inClosed) + len(open.elementList())
    return []


def IDAStarSearch(problem, heuristic):

    def search(node, actions, g, bound, num_closed, num_open_total, num_openPlusClosed, num_open_curr):
        f = g + heuristic(node, problem)
        #open.append(node)
        num_open_total += 1
        num_open_curr += 1
        if f > bound:
            return f, [], num_closed, num_open_total, num_openPlusClosed, num_open_curr
        if problem.isGoalState(node):
            if num_open_curr + num_closed > num_openPlusClosed:
                num_openPlusClosed = num_open_curr + num_closed
            return [0], [], num_closed, num_open_total, num_openPlusClosed, num_open_curr
        min = [float('inf')]
        #closed.append(node)
        #open.remove(node)
        num_closed += 1
        num_open_curr -= 1
        for coord, direction, steps in problem.getSuccessors(node):
            if actions == [] or not problem.getInverseAction(direction) == actions[-1]:
                newActions = actions + [direction]
                t, actions,  num_closed, num_open_total, num_openPlusClosed, num_open_curr = search(coord, actions, g + 1, bound, num_closed, num_open_total, num_openPlusClosed, num_open_curr)
                if t == [0]:
                    actions = actions + newActions
                    return [0], actions, num_closed, num_open_total, num_openPlusClosed, num_open_curr
                if t < min:
                    min = t
        if num_open_curr + num_closed > num_openPlusClosed:
            num_openPlusClosed = num_open_curr + num_closed
        return min, [], num_closed, num_open_total, num_openPlusClosed, num_open_curr

    start = problem.getStartState()
    bound = heuristic(start, problem)
    actions = []
    num_closed = 0
    num_open_total = 0
    num_open_curr = 0
    num_moved = 0  # moved from the Closed list to the Open list because shorter paths were found from the start node to this node.
    num_openPlusClosed = 0
    #open = []
    #closed = []

    while True:
        t, actions, num_closed, num_open_total, num_openPlusClosed, num_open_curr = search(start, actions, 0, bound, num_closed, num_open_total, num_openPlusClosed, num_open_curr)
        if t == [0]:
            actions.reverse()
            printRes(num_open_total, num_closed, num_moved, num_openPlusClosed)
            return actions
        bound = t


def AnytimeWAstarSearch(problem, NonePuzzle, heuristic):

    w = 1.3
    open = PriorityQueue()
    start = problem.getStartState()
    fprime = w * heuristic(start, problem)
    open.push((start, []), fprime)
    inClosed = {}
    g = {}
    g[start] = 0
    f = {}
    storeActions = {}
    bound = float('inf')
    incumbent = NonePuzzle
    num_closed = 0
    num_open = 1
    num_moved = 0  # moved from the Closed list to the Open list because shorter paths were found from the start node to this node.
    num_openPlusClosed = 1

    while not open.isEmpty():
        node, actions = open.pop()
        if incumbent == NonePuzzle or f[node] < bound:
            inClosed[node] = actions
            num_closed += 1
            for coord, direction, steps in problem.getSuccessors(node):
                if actions == [] or not problem.getInverseAction(direction) == actions[-1]:
                    newActions = actions + [direction]
                    # print 'newActions=',newActions
                    if problem.getCostOfActions(newActions) + heuristic(coord, problem) < bound:
                        if problem.isGoalState(coord):
                            incumbent = coord
                            g[incumbent] = problem.getCostOfActions(newActions)
                            f[incumbent] = g[incumbent]
                            bound = f[incumbent]
                            storeActions[incumbent] = newActions
                            # print storeActions[incumbent]
                        elif open.isElement(coord) and not inClosed.has_key(coord):
                            if g[coord] > g[node] + 1:
                                g[coord] = g[node] + 1
                                f[coord] = g[coord] + heuristic(coord, problem)
                                open.update((coord, newActions), g[coord] + w * heuristic(coord, problem))
                                num_open += 1
                        elif inClosed.has_key(coord):
                            if g[coord] > g[node] + 1:
                                g[coord] = problem.getCostOfActions(newActions)
                                f[coord] = g[coord] + heuristic(coord, problem)
                                open.update((coord, newActions), g[coord] + w * heuristic(coord, problem))
                                num_open += 1
                                inClosed.pop(coord)
                                num_moved += 1
                        else:
                            g[coord] = problem.getCostOfActions(newActions)
                            f[coord] = g[coord] + heuristic(coord, problem)
                            open.push((coord, newActions), g[coord] + w * heuristic(coord, problem))
                            num_open += 1
        if len(inClosed) + len(open.elementList()) > num_openPlusClosed:
            num_openPlusClosed = len(inClosed) + len(open.elementList())

    printRes(num_open, num_closed, num_moved, num_openPlusClosed)
    return storeActions[incumbent]


def AnytimeReparingAstarSearch(problem, NonePuzzle, heuristic):
    t0 = time.time()

    def fvalue(node, actions, w):
        return problem.getCostOfActions(actions) + w * heuristic(node, problem)

    def ImprovePath(open, bound, g, INCONS, inClosed, goal, storeGoalActions, w, num_closed, num_open, num_moved,
                    num_openPlusClosed):
        node, actions = open.find_min()
        while fvalue(node, actions, w) < bound:
            inClosed[node] = actions
            num_closed += 1
            open.pop()
            for coord, direction, steps in problem.getSuccessors(node):
                if actions == [] or not problem.getInverseAction(direction) == actions[-1]:
                    newActions = actions + [direction]
                    if problem.isGoalState(coord):
                        goal = coord
                        g[goal] = problem.getCostOfActions(newActions)
                        bound = fvalue(goal, newActions, w)
                        storeGoalActions.append(newActions)
                        return open, bound, g, INCONS, inClosed, storeGoalActions, goal, num_closed, num_open, num_moved, num_openPlusClosed
                    if not (inClosed.has_key(coord) or open.isElement(coord) or INCONS.has_key(coord)):
                        g[coord] = float('inf')
                    if g[coord] > g[node] + 1:
                        g[coord] = problem.getCostOfActions(newActions)
                        if not inClosed.has_key(coord):
                            open.update((coord, newActions), fvalue(coord, newActions, w))
                            num_open += 1
                        else:
                            INCONS[coord] = newActions
                            num_moved += 1
            if len(inClosed) + len(open.elementList()) + len(INCONS) > num_openPlusClosed:
                num_openPlusClosed = len(inClosed) + len(open.elementList()) + len(INCONS)
            node, actions = open.find_min()
        storeGoalActions.append([])
        return open, bound, g, INCONS, inClosed, storeGoalActions, goal, num_closed, num_open, num_moved, num_openPlusClosed

    w = 1.6
    start = problem.getStartState()
    open = PriorityQueue()
    open.push((start, []), w * heuristic(start, problem))
    inClosed = {}

    num_closed = 0
    num_open = 1
    num_moved = 0  # moved from the Closed list to the Open list because shorter paths were found from the start node to this node.
    num_openPlusClosed = 1

    INCONS = {}
    g = {}
    storeGoalActions = []
    bound = float('inf')
    goal = NonePuzzle
    g[start] = 0
    open, bound, g, INCONS, inClosed, storeGoalActions, goal, num_closed, num_open, num_moved, num_openPlusClosed \
        = ImprovePath(open, bound, g, INCONS, inClosed, goal, storeGoalActions, w, num_closed, num_open, num_moved,
                      num_openPlusClosed)

    if INCONS == {}:
        minCost_h_plus_g = min(fvalue(node, actions, 1) for node, actions in open.elementList())
    else:
        minCost_h_plus_g = min(min(fvalue(node, actions, 1) for node, actions in open.elementList()),
                               min(fvalue(node, actions, 1) for node, actions in INCONS.items()))
    wprime = min(w, g[goal] / minCost_h_plus_g)
    t1 = time.time()
    print '\a'
    print('Algorithm found a suboptimal path for wprime = %f of %d moves: %s' % (
        wprime, len(storeGoalActions[-1]), str(storeGoalActions[-1])))
    print '---------------------'
    print 'Running rime for finding the first suboptimal solution:', t1 - t0, 's'
    print '---------------------'
    print 'Still running for finding the optimal solution...'

    while wprime > 1:
        w = w - 0.2
        if w < 1:
            break
        for node, actions in INCONS.items():
            open.update((node, actions), fvalue(node, actions, w))
        INCONS = {}
        inClosed = {}
        for node, actions in open.elementList():
            open.update((node, actions), fvalue(node, actions, w))
        open, bound, g, INCONS, inClosed, storeGoalActions, goal, num_closed, num_open, num_moved, num_openPlusClosed \
            = ImprovePath(open, bound, g, INCONS, inClosed, goal, storeGoalActions, w, num_closed, num_open, num_moved,
                          num_openPlusClosed)
        if INCONS == {}:
            minCost_h_plus_g = min(fvalue(node, actions, 1) for node, actions in open.elementList())
        else:
            minCost_h_plus_g = min(min(fvalue(node, actions, 1) for node, actions in open.elementList()),
                                   min(fvalue(node, actions, 1) for node, actions in INCONS.items()))
        wprime = min(w, g[goal] / minCost_h_plus_g)
        if not storeGoalActions[-1] == storeGoalActions[-2] and not storeGoalActions[-1] == []:
            t2 = time.time()
            print '\a'
            print('Algorithm found a suboptimal path for wprime = %f of %d moves: %s' % (
                wprime, len(storeGoalActions[-1]), str(storeGoalActions[-1])))
            print '---------------------'
            print 'Running rime for finding another suboptimal solution:', t2 - t0, 's'
            print '---------------------'
            print 'Still running for finding the optimal solution...'
        if storeGoalActions[-1] == []:
            storeGoalActions.remove([])

    printRes(num_open, num_closed, num_moved, num_openPlusClosed)
    return storeGoalActions[-1]


class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

    def find_min(self):
        min = heapq.nsmallest(1, self.heap)
        return min[0][2]

    def isElement(self, x):
        element = []
        for e in self.heap:
            element.append(e[2][0])
        if not element == []:
            if x in element:
                return True
        return False

    def elementList(self):
        element = []
        for e in self.heap:
            element.append(e[2])
        return element

def printRes(num_open, num_closed, num_moved, num_openPlusClosed):

    print 'Total number of configurations visited (all nodes inserted into the Open list, including re-visited):', num_open
    print 'Total number of configurations expanded (all nodes inserted into the Closed list, including re-expanded):', num_closed
    print 'Total number of nodes had to be moved from the Closed list to the Open list:', num_moved
    print 'Max size of Open + Closed list (Max size of Open + Closed + INCONS for ARA*):', num_openPlusClosed
    print '---------------------'
    return []
