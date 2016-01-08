import time
import math
import soarWorld
reload(soarWorld)
import maze
reload(maze)
from maze import *
from soar.io import io
import lib601.util as util
from search import ucSearch
from lib601.search import search

import tk
import driver
import soarWorld
tk.setInited()


worldname = 'SL12World'


def mazeSuccessors(maze):
    def s(state):
        (r,c) = state
        potential = [(r+i, c+j) for (i,j) in [(1,0),(0,1),(0,-1),(-1,0)]]
        return [cell for cell in potential if maze.isPassable(cell)]
    return s


def UCMazeSuccessors(maze):
    def f(state):
        (r,c) = state
        possible = [((r+i, c+j), (i**2 + j**2)**.5) for (i,j) in [(1,0), (0,1), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]]
        return ((states,cost) for (states,cost) in possible if maze.isPassable(states))
    return f


def TollMazeSuccessors(maze, cells_per_dollar):
    pass # your code here


def getPath(maze):
    print sum([ucSearch(UCMazeSuccessors(maze),
                                                   maze.start,
                                                   lambda x: x==maze.goal)[1]])
    return [maze.indicesToPoint(i) for i in ucSearch(UCMazeSuccessors(maze),
                                                   maze.start,
                                                   lambda x: x==maze.goal)[0]]


PATH_TO_WORLD = '%s.py' % worldname
world = [i.strip() for i in open('%s.txt' % worldname).readlines()]

bounds = {'SL12World': (0.0,0.0,10.8,10.8)}


TOLLS = False
TOLL_CELLS = {(r,222):1.5 for r in xrange(389,443)}
def tollDollars(cell):
    return TOLL_CELLS.get(cell, 0.0)


# this function is called when the brain is loaded
def setup():
    robot.maze = RobotMaze(world, *(bounds[worldname]))
    print robot.maze.x1 - robot.maze.x0
    _t = time.time()
    robot.path = getPath(robot.maze)
    print "getPath completed in %f seconds." % (time.time() - _t)
    (robot.window, robot.initialLocation) = \
                   soarWorld.plotSoarWorldDW(PATH_TO_WORLD)
    if robot.path:
        robot.window.drawPath([i.x - \
                               robot.initialLocation.x \
                               for i in robot.path],
                              [i.y - \
                               robot.initialLocation.y \
                               for i in robot.path], color = 'blue')
    else:
        print 'no plan from', robot.maze.start, 'to', robot.maze.goal
    robot.slimeX = []
    robot.slimeY = []
    if TOLLS:
        for (r,c) in TOLL_CELLS:
            p = robot.maze.indicesToPoint((r,c)) - robot.initialLocation
            robot.window.drawSquare(p.x, p.y, .01, "red")


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
