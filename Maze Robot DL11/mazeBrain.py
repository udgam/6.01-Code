import math
import lib601.util as util
import soarWorld
reload(soarWorld)
from soar.io import io
from maze import *
from lib601.search import search

import driver
import tk
import soarWorld
tk.setInited()


worldname = 'dl11World'


def getPath(maze):
    path = []
    a = search(mazeSuccessors(maze), maze.start, goalFind(maze), dfs = False)
    for item in a:
        path.append(maze.indicesToPoint(item))
    return path

PATH_TO_WORLD = '%s.py' % worldname
world = [i.strip() for i in open('%s.txt' % worldname).readlines()]

bounds = {'dl11World': (0.0,0.0,10.8,10.8),
          'bigEmptyWorld': (0.0,0.0,4.05,4.05)}


class RobotMaze(Maze):
    ROBOT_DIAMETER = 0.44 # meters, approximate

    def __init__(self, mapText, x0, y0, x1, y1):
        Maze.__init__(self, mapText) #run Maze's __init__ on this instance
        self.Maze = mapText
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.x1 = float(x1)
        self.y1 = float(y1)

    def pointToIndices(self, point):
        stateWidth = float(self.x1-self.x0) / self.width
        c = int(math.floor((point.x-self.x0)/stateWidth))
        c = min(max(0, c), self.width-1)
        stateHeight = float(self.y1-self.y0) / self.height
        r = self.height - 1 - int(math.floor((point.y-self.y0)/stateHeight))
        r = min(max(0, r), self.height-1)
        return (r,c)

    def indicesToPoint(self, (r,c)):
        stateWidth = float((self.x1-self.x0) / self.width)
        stateHeight = float(self.y1-self.y0) / self.height
        pointX = float((c) * stateWidth + stateWidth/2) + self.x0
        pointY = self.y1 - float((r) * stateHeight + stateHeight/2)
        return util.Point(pointX,pointY)
    def isPassable(self, (r,c)):
        stateWidth = float(self.x1-self.x0) / self.width
        stateHeight = float(self.y1-self.y0) / self.height
        row = math.floor(self.ROBOT_DIAMETER/stateHeight/2)+1
        col = math.floor(self.ROBOT_DIAMETER/stateWidth/2)+1
 
        for i in range(int(row)):
            for j in range(int(col)):
                if self.Maze[r+i][c+j]=="#":
                    return False
                if self.Maze[r+i][c-j]=="#":
                    return False
                if self.Maze[r-i][c+j]=="#":
                    return False
                if self.Maze[r-i][c-j]=="#":
                    return False
        return True

# this function is called when the brain is loaded
def setup():
    robot.maze = RobotMaze(world, *(bounds[worldname]))
    robot.path = getPath(robot.maze)
    (robot.window, robot.initialLocation) = \
                   soarWorld.plotSoarWorldDW(PATH_TO_WORLD)
    if robot.path:
        robot.window.drawPath([i.x - \
                               robot.initialLocation.x \
                               for i in robot.path],
                              [i.y - \
                               robot.initialLocation.y \
                               for i in robot.path], color = 'purple')
    else:
        print 'no plan from', robot.maze.start, 'to', robot.maze.goal
    robot.slimeX = []
    robot.slimeY = []
    print 0


# this function is called when the start button is pushed
def brainStart():
    pass


# this function is called 10 times per second
def step():
    x, y, theta = io.getPosition()
    robot.slimeX.append(x)
    robot.slimeY.append(y)

    # the following lines compute the robot's current position and angle
    currentPoint = util.Point(x,y).add(robot.initialLocation)
    currentAngle = util.fixAnglePlusMinusPi(theta)

    fv, rv = driver.drive(robot.path, currentPoint, currentAngle)
    io.setForward(fv)
    io.setRotational(rv)


# called when the stop button is pushed
def brainStop():
    for i in range(len(robot.slimeX)):
        robot.window.drawPoint(robot.slimeX[i], robot.slimeY[i], 'red')

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
smallMap = ['.S..',
                '....',
                '##.#',
                '...G']

m = RobotMaze(smallMap, 1, 1, 2, 3)
print m.indicesToPoint((2, 1))
