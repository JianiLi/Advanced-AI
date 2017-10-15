


class Variable:
    def __init__(self, i,j,duration):
        self.i = i
        self.j = j
        self.duration = duration
        self.domain = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.startT = None

    def constraints(self):
        self.startT + self.duration <= 15
        

VariableSet = []
VariableSet.append(Variable(0,0,3))
VariableSet.append(Variable(0,1,4))
VariableSet.append(Variable(0,2,2))
VariableSet.append(Variable(0,3,2))

VariableSet.append(Variable(1,0,1))
VariableSet.append(Variable(1,1,5))
VariableSet.append(Variable(1,2,5))

VariableSet.append(Variable(2,0,2))
VariableSet.append(Variable(2,1,2))
VariableSet.append(Variable(2,2,2))
VariableSet.append(Variable(2,3,2))

VariableSet.append(Variable(3,0,2))
VariableSet.append(Variable(3,1,3))
VariableSet.append(Variable(3,2,3))
VariableSet.append(Variable(3,3,2))

AssignedVariableSet = []

while VariableSet - AssignedVariableSet:
