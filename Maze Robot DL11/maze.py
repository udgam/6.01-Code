# Mazes
from lib601.search import search

# set up lists of strings to represent the four test mazes
smallMazeText = [line.strip() for line in open('smallMaze.txt').readlines()]
mediumMazeText = [line.strip() for line in open('mediumMaze.txt').readlines()]
largeMazeText = [line.strip() for line in open('largeMaze.txt').readlines()]
hugeMazeText = [line.strip() for line in open('hugeMaze.txt').readlines()]

class Maze:
    def __init__(self, mazeText):
        self.mazeText = mazeText
        self.height = len(mazeText)
        self.width = len(mazeText[0])
        countC = 0
        countR = 0
        startC = 0
        startR = 0
        goalC = 0
        goalR = 0
        for index in xrange(len(mazeText)):
            numLetter = 0
            for letter in mazeText[index]:
                if letter == "S":
                    startC = numLetter
                    startR = index
                if letter == "G":
                    goalC = numLetter
                    goalR = index
                numLetter+=1
        self.start = (startR, startC)
        self.goal = (goalR, goalC)
    def isPassable(self,tup):
        if tup[0] >= self.height or tup[1] >= self.width:
            return False
        if self.mazeText[tup[0]][tup[1]] == "#":
            return False
        return True

def mazeSuccessors(maze):
    def f(state):
        (r,c) = state
        possible = [(r+i, c+j) for (i,j) in [(1,0), (0,1), (0,-1), (-1,0)]]
        return (states for states in possible if maze.isPassable(states))
    return f
def goalFind(maze):
	def f(state):
		if state == maze.goal:
			return True
		return False
	return f

