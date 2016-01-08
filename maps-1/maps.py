import copy
import random
import time
from graphics import *

class Sudoku:
    def __init__(self):
        self.create_refrence()
        self.createboard()
        self.user_fillin_board()

    def create_refrence(self): ### generates all the positions in each row colom and box
        self.boxes = {}
        self.coloms = {}
        self.rows = {}
        for i in range(9):
            thisbox = []
            thiscolom = []
            thisrow = []
            for j in range (9):
                thisbox.append(i//3*27+i%3*3+j//3*9+j%3)
                thiscolom.append(i+j*9)
                thisrow.append(i*9+j)
            self.boxes[i] = thisbox
            self.coloms[i] = thiscolom
            self.rows[i] = thisrow

    def finder(self,position): ### finds the row colom and box of a given position
        colom = position%9
        row = position//9
        box = colom//3+row//3*3
        return colom, row, box
    
    def createboard(self): ### generates the sudoku board, and gives a dictionary of points for all the 81 positions
        self.win = GraphWin('sudoku',800,700)
        bp = []
        rp = []
        tl = Point(50,50)
        for i in range(10):
            bp.append(Point(50+int(66.666*i),650))
            rp.append(Point(650,50+int(66.666*i)))
        bprp = bp + rp
        rectangles = []
        for pt in bprp:
            rectangles.append(Rectangle(tl,pt))
        for rect in rectangles:
            rect.draw(self.win)
        line1 = Line(Point(50+66*3,50),Point(50+66*3,650))
        line2 = Line(Point(50+66*6+2,50),Point(50+66*6+2,650))
        line3 = Line(Point(50,50+66*3),Point(650,50+66*3))
        line4 = Line(Point(50,50+66*6+2),Point(650,50+66*6+2))
        line1.draw(self.win)
        line2.draw(self.win)
        line3.draw(self.win)
        line4.draw(self.win)
        self.pointspot = {}
        spotnum = 0
        for i in range(9):
            for j in range(9):
                self.pointspot[spotnum] = Point(83+66.66*j,83+66.66*i)
                spotnum += 1
        self.startbutton = Rectangle(Point(670,320),Point(780,380))
        startmessage = Text(Point(725,350),'S O L V E')
        self.startbutton.setFill('red')
        self.startbutton.draw(self.win)
        startmessage.setStyle('bold')
        startmessage.draw(self.win)
        self.gamedic = {}
        for i in range(81):
            self.gamedic[i] = [1,2,3,4,5,6,7,8,9]
            
    def user_fillin_board(self):
        filling = True
        spotdic = {}
        entries = []
        clicknum = 0
        while filling:
            clickspot = self.win.getMouse()
            click = self.where(clickspot)
            if click in range(81):
                self.clicknum = Entry(self.pointspot[click],2)
                entries.append(self.clicknum)
                self.clicknum.draw(self.win)
                self.win.getKey()
                spotdic[click] = self.clicknum
                clicknum += 1
            elif click == 81:
                for i in spotdic.keys():
                    if spotdic[i].getText() not in ['1','2','3','4','5','6','7','8','9']:
                        pass
                    else:
                        self.gamedic[i] = [int(spotdic[i].getText())]
                for i in entries:
                    i.undraw()
                self.solve_sudoku()
                filling = False

    def where(self,point):
        x = point.getX()
        y = point.getY()
        if x>50 and x<650 and y>50 and y<650:
            return int((x-50)/66.66) + 9 *int((y-50)/66.66)
        elif x>670 and x<780 and y>320 and y<380:
            return 81
        else:
            return 82

    def solve_sudoku(self):
        for i in range(10):
            time.sleep(1)
            before = copy.deepcopy(self.gamedic)
            self.easy_solver()
            if self.gamedic == before:
                self.visualive_gamedic()
        print (self.gamedic)
        self.visualive_gamedic()

    def visualive_gamedic(self):
        for i in self.gamedic.keys():
            if len(self.gamedic[i])==1:
                text = Text(self.pointspot[i],self.gamedic[i])
                text.draw(self.win)
            else:
                pass
        self.win.getMouse()        

    def easy_solver(self):
        ### box clean up
        for box in range(9):
            inbox = []
            pairs = []
            hit = []
            for index in self.boxes[box]:
                element = self.gamedic[index]
                if len(element) == 1:
                    inbox.extend(element)
                elif len(element) == 2:
                    if element in pairs:
                        inbox.extend(element)
                        hit.append(element)
                    else:
                        pairs.append(element)
            for index in self.boxes[box]:
                element = self.gamedic[index]
                if len(element) == 1:
                    pass
                elif element in hit:
                    pass
                else:
                    for i in inbox:
                        if i in element:
                            element.remove(i)
                        else:
                            pass
        ### colom clean up
        for colom in range(9):
            incolom = []
            pairs = []
            hit = []
            for index in self.coloms[colom]:
                element = self.gamedic[index]
                if len(element) == 1:
                    incolom.extend(element)
                elif len(element) == 2:
                    if element in pairs:
                        incolom.extend(element)
                        hit.append(element)
                    else:
                        pairs.append(element)
            for index in self.coloms[colom]:
                element = self.gamedic[index]
                if len(element) == 1:
                    pass
                elif element in hit:
                    pass
                else:
                    for i in incolom:
                        if i in element:
                            element.remove(i)
                        else:
                           pass

        ### row clean up
        for row in range(9):
            inrow = []
            pairs = []
            hit = []
            for index in self.rows[row]:
                element = self.gamedic[index]
                if len(element) ==1:
                    inrow.extend(element)
                elif len(element) ==2:
                    if element in pairs:
                        inrow.extend(element)
                        hit.append(element)
                    else:
                        pairs.append(element)
            for index in self.rows[row]:
                element = self.gamedic[index]
                if len(element) == 1:
                    pass
                elif element in hit:
                    pass
                else:
                    for i in inrow:
                        if i in element:
                            element.remove(i)
                        else:
                            pass
            
            

a = Sudoku()
