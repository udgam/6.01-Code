import math
import lib601.util as util

robotDiameterMeters = 0.44
sonarMax = 1.5

class DynamicRobotMaze:
    def __init__(self, height, width, x0, y0, x1, y1):
        self.width = width
        self.height = height
        self.x0,self.x1 = x0,x1
        self.y0,self.y1 = y0,y1
        self.grid = [[True for c in xrange(width)] for r in xrange(height)]

    def pointToIndices(self, point):
        ix = int(math.floor((point.x-self.x0)*self.width/(self.x1-self.x0)))
        iix = min(max(0,ix),self.width-1)
        iy = int(math.floor((point.y-self.y0)*self.height/(self.y1-self.y0)))
        iiy = min(max(0,iy),self.height-1)
        return ((self.height-1-iiy,iix))

    def indicesToPoint(self, (r,c)):
        x = self.x0 + (c+0.5)*(self.x1-self.x0)/self.width
        y = self.y0 + (self.height-r-0.5)*(self.y1-self.y0)/self.height
        return util.Point(x,y)

    def isClear(self,(r,c)):
        if not (0 <= r < self.height and 0 <= c < self.width):
            return False
        return self.grid[r][c]

    def isPassable(self,(r,c)):
        potential = [(r+i),(c+j) for (i,j) in [(1,0),(0,1),(-1,0),(0,-1)]]
        for cell in potential:
            if not self.isClear(cell):
                return False
        return True

    def probOccupied(self,(r,c)):
        return float(not self.grid[r][c])

    def sonarHit(self,(r,c)):
        self.grid[r][c] = False
    
    def sonarPass(self,(r,c)):
        self.grid[r][c] = True
