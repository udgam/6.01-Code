import noiseModel
import maze
reload(maze)
import search
reload(search)
import checkoff
reload(checkoff)
from mazeGraphics import *

import lib601.util as util
import lib601.sonarDist as sonarDist
import lib601.markov as markov
from soar.io import io
import soar.outputs.simulator as sim

import time
import math
import random


###### SETUP

NOISE_ON = False

sl13World = [0.15, util.Point(7.0, 1.0), (-0.5, 8.5, -0.5, 6.5)]
bigFrustrationWorld = [0.2, util.Point(7.0, 1.0), (-0.5, 8.5, -0.5, 8.5)]
frustrationWorld = [0.15, util.Point(3.5, 0.5), (-0.5, 5.5, -0.5, 5.5)]
raceWorld = [0.1, util.Point(2.0, 5.5), (-0.5, 5.5, -0.5, 8.5)]
bigPlanWorld = [0.25, util.Point(3.0, 1.0), (-0.5, 10.5, -0.5, 10.5)]
realRobotWorld = [0.1, util.Point(1.5,0.0), (-2.0, 6.0, -2.0, 6.0)]
robotRaceWorld = [0.1, util.Point(3.0,0.0), (-2.0, 6.0, -2.0, 6.0)]

THE_WORLD = sl13World
(gridSquareSize, goalPoint, (xMin, xMax, yMin, yMax)) = THE_WORLD

# graphics options
show_heatmap = False
show_passable = False
keep_old_windows = False

###### SOAR CONTROL

# this function is called when the brain is (re)loaded
def setup():
    #initialize robot's internal map
    width = int((xMax-xMin)/gridSquareSize)
    height = int((yMax-yMin)/gridSquareSize)
    robot.map = maze.DynamicRobotMaze(height,width,xMin,yMin,xMax,yMax)
    robot.goalIndices = robot.map.pointToIndices(goalPoint)
    sim.SONAR_VARIANCE = (lambda mean: 0.001) if NOISE_ON else (lambda mean: 0) #sonars are accurate to about 1 mm
    robot.plan = None
    robot.successors = search.makeMazeSuccessors(robot.map)
    #initialize graphics
    robot.windows = []
    if show_heatmap:
        robot.windows.append(HeatMapWindow(robot.map))
    robot.windows.append(PathWindow(robot.map, show_passable))
    for w in robot.windows:
        w.redrawWorld()
        w.render()

# this function is called when the start button is pushed
def brainStart():
    robot.done = False
    robot.count = 0
    checkoff.getData(globals())

# this function is called 10 times per second
def step():
    global inp
    robot.count += 1
    inp = io.SensorInput(cheat=True)


    # discretize sonar readings
    # each element in discreteSonars is a tuple (d, cells)
    # d is the distance measured by the sonar
    # cells is a list of grid cells (r,c) between the sonar and the point d meters away
    discreteSonars = []
    for (sonarPose, distance) in zip(sonarDist.sonarPoses,inp.sonars):
        if NOISE_ON:
            distance = noiseModel.noisify(distance, gridSquareSize)
        sensorIndices = robot.map.pointToIndices(inp.odometry.transformPose(sonarPose).point())
        hitIndices = robot.map.pointToIndices(sonarDist.sonarHit(distance, sonarPose, inp.odometry))
        ray = util.lineIndices(sensorIndices, hitIndices)
        discreteSonars.append((distance, ray))


    # figure out where robot is
    startPoint = inp.odometry.point()
    startCell = robot.map.pointToIndices(startPoint)


    # if necessary, make new plan
    if robot.plan is None:
        print 'REPLANNING'
        robot.plan = search.ucSearch(robot.successors,
                              robot.map.pointToIndices(inp.odometry.point()),
                              lambda x: x == robot.goalIndices,
                              lambda x: 0)
    isGood = True
    for i in robot.plan:
        if not robot.map.isPassable(i) and isGood:
            print 'REPLANNING'
            robot.plan = search.ucSearch(robot.successors,
                                  robot.map.pointToIndices(inp.odometry.point()),
                                  lambda x: x == robot.goalIndices,
                                  lambda x: 0)
            isGood = False


    # graphics (draw robot's plan, robot's location, goalPoint)
    # do not change this block
    for w in robot.windows:
        w.redrawWorld()
    robot.windows[-1].markCells(robot.plan,'blue')
    robot.windows[-1].markCell(robot.map.pointToIndices(inp.odometry.point()),'gold')
    robot.windows[-1].markCell(robot.map.pointToIndices(goalPoint),'green')


    # update map
    for (d,cells) in discreteSonars:
        if d != 5.0:
            robot.map.sonarHit(cells[-1])


    # if we are within 0.1m of the goal point, we are done!
    if startPoint.distance(goalPoint) <= 0.1:
        io.Action(fvel=0,rvel=0).execute()
        code = checkoff.generate_code(globals())
        raise Exception('Goal Reached!\n\n%s' % code)

    # otherwise, figure out where to go, and drive there
    destinationPoint = robot.map.indicesToPoint(robot.plan[0])
    while startPoint.isNear(destinationPoint,0.1) and len(robot.plan)>1:
        robot.plan.pop(0)
        destinationPoint = robot.map.indicesToPoint(robot.plan[0])

    currentAngle = inp.odometry.theta
    angleDiff = startPoint.angleTo(destinationPoint)-currentAngle
    angleDiff = util.fixAnglePlusMinusPi(angleDiff)
    fv = rv = 0
    if startPoint.distance(destinationPoint) > 0.1:
        if abs(angleDiff) > 0.1:
            rv = angleDiff
        else:
            fv = 1.5*startPoint.distance(destinationPoint)
    io.setForward(fv)
    io.setRotational(rv)


    # render the drawing windows
    # do not change this block
    for w in robot.windows:
        w.render()

# called when the stop button is pushed
def brainStop():
    stopTime = time.time()
    print 'Total steps:', robot.count
    print 'Elapsed time in seconds:', stopTime - robot.startTime

def shutdown():
    if not keep_old_windows:
        for w in robot.windows:
            w.window.destroy()
