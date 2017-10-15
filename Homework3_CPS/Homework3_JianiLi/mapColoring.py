import copy

import sys

# from memory_profiler import profile
'''
try:
    from guppy import hpy
except:
    pass
'''
from mapGenerate import *
import commands, os, re

sys.setrecursionlimit(1000000)


def process_info():
    pid = os.getpid()
    res = commands.getstatusoutput('ps aux|grep ' + str(pid))[1].split('\n')[0]

    p = re.compile(r'\s+')
    l = p.split(res)
    info = {'user': l[0],
            'pid': l[1],
            'cpu': l[2],
            'mem': l[3],
            'vsa': l[4],
            'Resident Set Size': l[5],
            'start_time': l[6]}
    return l[5]


def initalize(nodeSet, algorithm):
    initNode = degreeHeuristic(nodeSet)
    initNode.setColor(random.choice(initNode.getRemainingColorSet()))
    curNode = initNode
    if algorithm == "arc" or algorithm == "mrv":
        assignedSet = []
        assignedSet.append(initNode)
    elif algorithm == "backjumping":
        assignedSet = set()
        assignedSet.add(initNode)
    startTime = time.time()
    lastNode = None
    lastState = None

    return initNode, curNode, assignedSet, startTime, lastNode, lastState


def print_map_data(startTime, nodeSet, colorNum, nodeNum, treeNum, lastNode=None, lastState=None, algorithm=None):
    print "--------------------------------------------"
    print "time used for", algorithm, ":", "%.6f" % (time.time() - startTime), "s"
    # print "tree size for", algorithm, ":", treeNum

    if all(node.color for node in nodeSet):
        print "map coloring succeeded."
        map_color(nodeSet, colorNum, nodeNum, None, None, algorithm)
    else:
        print "map coloring failed."
        map_color(nodeSet, colorNum, nodeNum, lastNode, lastState, algorithm)

        # print time.time() - startTime


def degreeHeuristic(nodeSet):
    # get the initial node by degree heuristic
    initNode = max(nodeSet, key=lambda node: len(node.neighborSet))
    return initNode


def MRV(unassignedSet):
    # minimum remaining value
    curNode = min(unassignedSet, key=lambda node: len(node.getRemainingColorSet()))
    return curNode


def LCV(curNode, assignedSet):
    # least constrain value to assign
    constraint = {}
    for color in curNode.getRemainingColorSet():
        constraint[color] = 0
        for node in curNode.neighborSet - set(assignedSet):
            if len(node.getRemainingColorSet()) == 1 and color in node.getRemainingColorSet():
                constraint[color] += 1
    colorToAssign = min(curNode.remainingColorSet, key=lambda color: constraint[color])
    return colorToAssign


def AC3(nodeSet, assignedSet, queue=None):
    nodeSet_copy = copy.deepcopy(nodeSet)
    # assignedSet_copy = copy.deepcopy(assignedSet)
    # unassignedSet_copy = copy.deepcopy(nodeSet_copy - set(assignedSet_copy))

    if queue == None:
        queue = [(node1, node2) for node1 in nodeSet_copy for node2 in node1.neighborSet]

    while queue:
        # print "queue",len(queue)
        (node1, node2) = queue.pop()
        # print "removed",rm_inconsistent_values(node1, node2)
        # print "node1before", node1.getRemainingColorSet()
        if rm_inconsistent_values(node1, node2):
            # print "node1after", node1.getRemainingColorSet()
            if not node1.getRemainingColorSet():
                return False
            for node in node1.neighborSet:
                queue.append((node, node1))
    return True


def rm_inconsistent_values(node1, node2):
    removed = False
    for color1 in node1.getRemainingColorSet():
        color2 = node2.getRemainingColorSet()
        if len(color2) == 0 or (len(color2) == 1 and color1 == color2):
            node1.removeFromRemainingColorSet(color1)
            removed = True

    return removed


def backtracking(curNode, assignedSet, initNode, treeNum, algorithm):
    if curNode == initNode:
        return None, None, treeNum
    if algorithm == "arc" or algorithm == "mrv":
        curNode = assignedSet[-1]
        # print "curNode", curNode.x, curNode.y, curNode.conflictSet
    elif algorithm == "backjumping":
        lastNode = curNode
        try:
            curNode = curNode.conflictSet[-1]
            # print "curNode", curNode.x,curNode.y,curNode.conflictSet
        except:
            pass
        '''
        for i in lastNode.conflictSet:
            if not i in curNode.conflictSet:
                curNode.conflictSet.append(i)
        try:
            curNode.conflictSet.remove(curNode)
        except:
            pass
        '''
    try:
        assignedSet.remove(curNode)
    except:
        pass
    curNode.triedColors.append(curNode.getColor())

    for node in curNode.neighborSet - set(assignedSet):
        if set(curNode.getRemainingColorSet()) - set(curNode.triedColors):
            node.color = None
        if algorithm == "backjumping":
            try:
                node.conflictSet.remove(curNode)
            except:
                pass

        cannotAssignColor = set()
        if algorithm == "arc" or algorithm == "mrv":
            for n in node.neighborSet - set([curNode]):
                cannotAssignColor.add(n.color)
        elif algorithm == "backjumping":
            for n in node.conflictSet:
                cannotAssignColor.add(n.color)

        if curNode.getColor() not in cannotAssignColor:
            node.addToRaminingColorSet(curNode.getColor())
    if set(curNode.getRemainingColorSet()) - set(curNode.triedColors):
        curNode.setColor(random.choice(list(set(curNode.getRemainingColorSet()) - set(curNode.triedColors))))
        if algorithm == "arc" or algorithm == "mrv":
            assignedSet.append(curNode)
        elif algorithm == "backjumping":
            assignedSet.add(curNode)
            # treeNum += 1
    else:
        curNode.triedColors = []
        curNode, assignedSet, treeNum = backtracking(curNode, assignedSet, initNode, treeNum, algorithm)
    return curNode, assignedSet, treeNum


# @profile(precision=4)
def mainloop(nodeSet, algorithm):
    '''
    try:
        hp = hpy()
        startHp = hp.heap()
    except:
        print "No guppy module found, please install!"
    '''
    # rssStart = process_info()
    # memStart = psutil.virtual_memory()
    nodeSet = copy.deepcopy(nodeSet)
    initNode, curNode, assignedSet, startTime, lastNode, lastState = initalize(nodeSet, algorithm)
    treeNum = 1

    # print "initNode",initNode.x,initNode.y
    while nodeSet - set(assignedSet):
        unassignedSet = nodeSet - set(assignedSet)
        for node in curNode.neighborSet - set(assignedSet):
            if algorithm == "backjumping":
                node.conflictSet.append(curNode)
            if curNode.getColor() in node.getRemainingColorSet():
                node.removeFromRemainingColorSet(curNode.getColor())
        curNode = MRV(unassignedSet)
        # print "node",curNode.x,curNode.y
        if algorithm == "mrv" or algorithm == "backjumping":
            if curNode.getRemainingColorSet():
                colorToAssign = LCV(curNode, assignedSet)
                curNode.setColor(colorToAssign)
                if algorithm == "mrv":
                    assignedSet.append(curNode)
                elif algorithm == "backjumping":
                    assignedSet.add(curNode)
                treeNum += 1
            else:
                # backtracking
                lastNode = copy.deepcopy(curNode)
                lastState = copy.deepcopy(assignedSet)
                curNode, assignedSet, treeNum = backtracking(curNode, assignedSet, initNode, treeNum, algorithm)
                if curNode == None:
                    break
        elif algorithm == "arc":
            # print "curNode.getRemainingColorSet()", curNode.getRemainingColorSet()
            # print "AC3(nodeSet, assignedSet)", AC3(nodeSet, assignedSet)
            if curNode.getRemainingColorSet() and AC3(nodeSet, assignedSet):
                colorToAssign = LCV(curNode, assignedSet)
                curNode.setColor(colorToAssign)
                assignedSet.append(curNode)
                treeNum += 1
            else:
                # backtracking
                lastNode = copy.deepcopy(curNode)
                lastState = copy.deepcopy(assignedSet)
                curNode, assignedSet, treeNum = backtracking(curNode, assignedSet, initNode, treeNum, algorithm)
                if curNode == None:
                    break
    print_map_data(startTime, nodeSet, colorNum, nodeNum, treeNum, lastNode, lastState, algorithm)
    '''
    try:
        print "Heap at the beginning of the function\n",startHp
        print "Heap at the end of the function\n", hp.heap()
    except:
        print "No guppy module found, please install!"
    '''
    # rssUsed = int(process_info()) - int(rssStart)
    # print rssUsed
    # memoEnd = psutil.virtual_memory()
    # print memStart
    # print memoEnd


if __name__ == '__main__':

    colorNum = int(raw_input(
        'Assign color number (3 or 4, then press ''enter''):'))
    if not (colorNum == 3 or colorNum == 4):
        print 'You have entered an wrong number, please run again!'
        sys.exit(0)

    nodeNum = int(raw_input(
        'Assign node number (20 or more):  '))
    if nodeNum > 200:
        select = int(raw_input("It may take minutes to generate the map, press '0' to continue, press '1' to stop:"))
        if select == 1:
            sys.exit(0)

    nodeSet = Map_generate(colorNum, nodeNum)

    p1 = mainloop(nodeSet, algorithm="mrv")
    p2 = mainloop(nodeSet, algorithm="arc")
    p3 = mainloop(nodeSet, algorithm="backjumping")
    print "--------------------------------------------"
