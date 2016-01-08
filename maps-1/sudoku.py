###matrix is [[colom1,colom2,colom3...]
def samesquare(matrix):
    sq = [[],[],[],[],[],[],[],[],[]]
    for i in matrix[0:3]:
        for j in i [0:3]:
            sq[0].append(j)
    for i in matrix[3:6]:
        for j in i [0:3]:
            sq[1].append(j)
    for i in matrix[6:]:
        for j in i [0:3]:
            sq[2].append(j)
    for i in matrix[0:3]:
        for j in i [3:6]:
            sq[3].append(j)
    for i in matrix[3:6]:
        for j in i [3:6]:
            sq[4].append(j)
    for i in matrix[6:]:
        for j in i [3:6]:
            sq[5].append(j)
    for i in matrix[0:3]:
        for j in i[6:]:
            sq[6].append(j)
    for i in matrix[3:6]:
        for j in i[6:]:
            sq[7].append(j)
    for i in matrix[6:]:
        for j in i[6:]:
            sq[8].append(j)
    for i in sq:
        inmate = []
        for j in i:
            if j in inmate and j != 0:
                return False
            inmate.append(j)
    return True
        
    
testmatrix = [[1,2,3,4,0,6,7,8,9],[4,5,6,7,8,9,1,2,3],[7,8,9,1,2,3,4,5,6],[2,3,4,5,6,7,8,9,1],[5,6,7,8,9,1,2,3,4],[8,9,1,2,3,4,5,6,7],[3,4,5,6,7,8,9,1,2],[6,7,8,9,1,2,3,4,5],[9,1,2,3,4,5,6,7,8]]
        


def samerow(matrix):
    for i in range(9):
        inrow = []
        for j in matrix:
            if j[i] in inrow and j[i] != 0:
                return False
            inrow.append(j[i])
    return True
        
def samecolom(matrix):
    for i in matrix:
        incolom = []
        for j in i:
            if j in incolom and j != 0:
                return False
            incolom.append(j)
    return True

def goal(x):
    a = 0
    for i in x:
        for j in i:
            if j != 0:
                a +=1
    return a == 81 and samerow(x) and samesquare(x) and samecolom(x)

def successors(state):
    nextstates = []
    for i,a in enumerate(state):
        for j,b in enumerate(a):
            if b == 0:
                for testnum in range(1,10):
                    changematrix = state
                    changematrix[i][j] = testnum
                    if samerow(changematrix) and samecolom(changematrix) and samesquare(changematrix):
                        nextstates.extend(changematrix)
    return nextstates

def search(successors, startState, goalTest, dfs = False):
    if goalTest(startState):
        return [startState]
    else:
        agenda = [SearchNode(startState, None)]
        visited = {startState}
        while len(agenda) > 0:
            if dfs: # Stack
                parent = agenda.pop(-1)
            else: # Queue
                parent = agenda.pop(0)
            for childState in successors(parent.state):
                child = SearchNode(childState, parent)
                if goalTest(childState):
                    return child.path()
                if childState not in visited:
                    agenda.append(child)
                    visited.add(childState)
        return None

class SearchNode:
    def __init__(self, state, parent, cost = 0.):
        self.state = state
        self.parent = parent
    def path(self):
        p = []
        node = self
        while node:
            p.append(node.state)
            node = node.parent
        p.reverse()
        return p




