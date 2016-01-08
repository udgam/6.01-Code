import heapq
from highways import *
from lib601.plotWindow import PlotWindow
from lib601.search import search,SearchNode


def pathCost(path):
    cost = 0
    for i in xrange(len(path)-1):
        cost += distance(path[i], path[i+1])
    return cost
def highway_successors(state):
    def f(state):
        path = []
        for before in highways.neighbors(state):
    return f

class PriorityQueue:
    def __init__(self, items=None):
        self.items = [] if items is None else items
        heapq.heapify(self.items)

    def push(self, item, priority):
        heapq.heappush(self.items, (priority, item))

    def pop(self):
        return heapq.heappop(self.items)

    def __len__(self):
        return self.items.__len__()

    def __str__(self):
        return "PriorityQueue(%r)" % self.items

def ucSearch(successors, startState, goalTest, heuristic=lambda s: 0):
    if goalTest(startState):
        return [startState]
    agenda = PriorityQueue()
    agenda.push(SearchNode(startState, None, cost=0), heuristic(startState))
    expanded = set()
    while len(agenda) > 0:
        priority, parent = agenda.pop()
        if parent.state not in expanded:
            expanded.add(parent.state)
            if goalTest(parent.state):
                return parent.path()
            for childState, cost in successors(parent.state):
                child = SearchNode(childState, parent, parent.cost+cost)
                if childState not in expanded:
                    agenda.push(child, child.cost+heuristic(childState))
    return None
