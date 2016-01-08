# Graphics for Gridded Mazes
# For 6.01 Final Lab
# hartz, lpk S2014

import Tkinter
import math

################################
# Color Handling
################################

redHue = 0.0
greenHue = 120.0
blueHue = 240.0
yellowHue = 60.0
cyanHue = 180.0
magentaHue = 250.0

# given a probability, return a Tk Color
def probToMapColor(p, hue = cyanHue, prior = 0.5):
    x = p - prior
    if p > prior:
        s = 1
        v = (1 - p) / (1 - prior)
    else:
        v = 1
        s = p / prior
    return RGBToPyColor(HSVtoRGB(hue, s, v))

#given an r,g,b tuple, return a matching Tk Color String
def RGBToPyColor(colorVals):
    (r, g, b) = [math.floor(c*255.99) for c in colorVals]
    return '#%02x%02x%02x' % (r, g, b)

#given an h,s,v tuple, return a matching r,g,b tuple
def HSVtoRGB(h, s, v):
    if s == 0:
        return (v, v, v)
    else:
        h = h/60  # sector 0 to 5
        i = math.floor( h )
        f = h - i        # factorial part of h
        p = v * ( 1 - s )
        q = v * ( 1 - s * f )
        t = v * ( 1 - s * ( 1 - f ) )
        if i == 0:
            return (v, t, p)
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)



################################
# Abstract Base Class
################################

#Base class; gridded Tk Canvas associated with Maze instance
class MazeGraphicsWindow:
    title = 'MazeGraphicsWindow'
    cell_size = 5

    def __init__(self, maze):
        self.maze = maze
        self.window = Tkinter.Toplevel()
        self.window.title(self.title)
        self.canvas = Tkinter.Canvas(self.window,
                                     width=(self.cell_size+1)*self.maze.width,
                                     height=(self.cell_size+1)*self.maze.height)
        self.canvas.pack()
        self.drawnCells = {}
        self.to_color = {}
        self.by_color = {"white":set()}
        self.dirty = set()
        for r in xrange(self.maze.height):
            for c in xrange(self.maze.width):
                x0 = c*(self.cell_size+1)-1
                x1 = x0+self.cell_size
                y0 = r*(self.cell_size+1)-1
                y1 = y0+self.cell_size
                cell = self.canvas.create_rectangle(x0,y0,x1,y1,
                                                    fill="white",
                                                    outline="white")
                self.drawnCells[(r,c)] = cell
                self.to_color[(r,c)] = "white"
                self.by_color["white"].add((r,c))
                self.dirty.add((r,c))

    def render(self):
        d = set(self.dirty)
        for loc in d:
            self.blitCell(loc,self.to_color[loc])

    def markCell(self, cell, color):
        if self.to_color[cell] != color:
            self.by_color[self.to_color[cell]].discard(cell)
            self.to_color[cell] = color
            self.dirty.add(cell)
            if color not in self.by_color:
                self.by_color[color] = set()
            self.by_color[color].add(cell)

    def markCells(self, cells, color):
        for cell in cells:
            self.markCell(cell, color)

    def blitCell(self, loc, color):
        self.canvas.itemconfigure(self.drawnCells[loc], fill=color, outline=color)
        self.dirty.discard(loc)

    def getBaseColor(self, loc):
        return "white" if self.maze.isClear(loc) else "black"

    def setToBaseColor(self, loc):
        self.markCell(loc, self.getBaseColor(loc))

    def clearColor(self, color):
        for loc in self.by_color.get(color,set()):
            self.setToBaseColor()

    def redrawWorld(self):
        for r in xrange(self.maze.height):
            for c in xrange(self.maze.width):
                self.setToBaseColor((r,c))

    def sonarHit(self, loc):
        self.maze.sonarHit(loc)
        self.drawHit(loc)

    def sonarPass(self, loc):
        self.maze.sonarPass(loc)
        self.drawPass(loc)

    drawHit = drawPass = setToBaseColor
 

##################################
# Specific Types of MazeGraphics 
##################################

#HeatMapWindow: for Bayesian Map, shows Probability of being occupied
class HeatMapWindow(MazeGraphicsWindow):
    title="HeatMap"
    def __init__(self, maze):
        MazeGraphicsWindow.__init__(self, maze)
        self.priorOcc = self.maze.probOccupied((0,0))

    def getBaseColor(self, loc):
        return probToMapColor(self.maze.probOccupied(loc), prior=self.priorOcc)

#PathWindow: for all maps, shows passable and clear cells
class PathWindow(MazeGraphicsWindow):
    title="Path"
    def __init__(self, maze, show_passable):
        MazeGraphicsWindow.__init__(self, maze)
        self.show_passable = show_passable

    def getBaseColor(self, loc):
        return "black" if not self.maze.isClear(loc) else "red" if (self.show_passable and not self.maze.isPassable(loc)) else "white"
