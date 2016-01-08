import math
import lib601.util as util
import soarWorld
reload(soarWorld)
from soar.io import io

import tk
import checkoff
reload(checkoff)
import soarWorld
tk.setInited()


worldname = 'bigEmptyWorld'

PATH_TO_WORLD = '%s.py' % worldname

bounds = {'dl11World': (0.0,0.0,10.8,10.8),
          'bigEmptyWorld': (0.0,0.0,4.05,4.05)}



# this function is called when the brain is loaded
def setup():
    robot.path = [util.Point(0.911250, 0.911250), util.Point(1.721250, 0.506250),
                  util.Point(2.531250, 1.316250), util.Point(1.721250, 1.721250),
                  util.Point(0.911250, 2.126250), util.Point(1.721250, 2.936250),
                  util.Point(2.531250, 2.531250)]
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
        print 'no plan'
    robot.slimeX = []
    robot.slimeY = []


# this function is called when the start button is pushed
def brainStart():
    checkoff.getData(globals())


def fixAnglePlusMinusPi(theta):
    def fixAnglePlusMinusPi(theta):
    while theta < (-1 * math.pi):
        theta += 2*math.pi
    while theta > math.pi:
        theta -= 2*math.pi
    return theta

# this function should return a tuple (fv, rv), where
# fv is the forward velocity the robot should use on this step, and
# rv is the rotational velocity the robot should use on this step
# in order to follow the desired path
def drive(path, pos, angle):
    if not pos.isNear(path[0], .1):
      tV = pos.distance(path[0]) * .1 if path[0] > pos
      tV = pos.distance(path[0]) * -.1 if path[0] < pos
    




# this function is called 10 times per second
def step():
    x, y, theta = io.getPosition()
    robot.slimeX.append(x)
    robot.slimeY.append(y)
    checkoff.update(globals())

    # the following lines compute the robot's current position and angle
    currentPoint = util.Point(x,y).add(robot.initialLocation)
    currentAngle = fixAnglePlusMinusPi(theta)

    forward_v, rotational_v = drive(robot.path, currentPoint, currentAngle)
    io.setForward(forward_v)
    io.setRotational(rotational_v)


# called when the stop button is pushed
def brainStop():
    for i in range(len(robot.slimeX)):
        robot.window.drawPoint(robot.slimeX[i], robot.slimeY[i], 'red')
    print 'Hex Code for Tutor:\n%s' % checkoff.generate_code(globals())


# called when brain or world is reloaded (before setup)
def shutdown():
    pass
