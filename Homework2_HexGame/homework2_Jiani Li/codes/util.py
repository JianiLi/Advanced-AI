class Vector(list):
    def __init__(self, l):
        super(Vector, self).__init__(l)

    def __add__(self, v2):
        return Vector([self[i] + v2[i] for i in range(len(self))])

    def __mul__(self, v2):
        try:
            return sum([self[i] * v2[i] for i in range(len(self))])
        except:
            return [x * v2 for x in self]


class Stack:
    def __init__(self, size):
        self.size = size
        self.data = []
        self.itemSum = 0
        self.validSum = 0

    def push(self, item):
        if self.itemSum >= self.size: return None
        if len(self.data) < self.size and len(self.data) == self.itemSum:
            self.data.append(item)
            self.itemSum += 1
        else:
            self.data[self.itemSum] = item
            self.itemSum += 1
        self.validSum = self.itemSum
        return self.data[self.itemSum - 1]

    def pop(self):
        if self.itemSum == 0:
            return None
        else:
            self.itemSum -= 1
            return self.data[self.itemSum]

    def redo(self):
        if self.itemSum < self.validSum:
            self.itemSum += 1
            return self.data[self.itemSum - 1]
        else:
            return None

    def top(self):
        if self.itemSum > 0:
            return self.data[self.itemSum - 1]
        else:
            return None
