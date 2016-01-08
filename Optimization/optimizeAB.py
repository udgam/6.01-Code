import lib601.sf as sf
import lib601.sim 
import lib601.poly as poly
from lib601.plotWindow import PlotWindow
##import rl

def makeSF(K):
    return sf.FeedbackSubtract(sf.Cascade(sf.Gain(K),sf.FeedbackAdd(sf.R(),sf.Gain(1))),sf.R())

def viewRootLocus():
    # make an instance of RootLocus and start the viewer with K = 0.01
    rl.RootLocus(makeSF).view(0.01)

def stemplot(response):
    PlotWindow().stem(range(len(response)), response)

def optOverLine(f, x0, x1, threshold):
    x= x0
    xOptimal = x0
    fOptimal = f(x)
    while x<=x1:
        if f(x)<fOptimal:
            xOptimal = x
            fOptimal = f(x)
        x+=threshold
    return (xOptimal,fOptimal)

def bisection(f, x0, x1, threshold):
    upperbound = x1
    lowerbound = x0
    while upperbound - lowerbound > threshold:
        mid = (upperbound + lowerbound)/2.0
        slope = (f(mid+0.000001)-f(mid-0.000001))/(2*0.000001)
        if slope<0:
            lowerbound = mid
        else:
            upperbound = mid
    xBest = (upperbound + lowerbound)/2.0
    return (xBest,f(xBest))


k = 1
a = makeSF(k)
b = a.simulator()
c = []
c.append(b.step(1))
for i in range(9):
	c.append(b.step(0))
print c

##viewRootLocus()
