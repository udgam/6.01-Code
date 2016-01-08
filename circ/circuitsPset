from le import solveEquations

class OnePort:
    def __init__(self, e1, e2, i):
        self.e1 = e1
        self.e2 = e2
        self.i = i

class VSrc(OnePort):
    def __init__(self, v0, e1, e2, i):
        OnePort.__init__(self,e1,e2,i)
        self.v0 = v0
        self.equation = [(1,e1), (-1, e2), (-1 *self.v0, None)]

class ISrc(OnePort):
    def __init__(self, i0, e1, e2, i):
        OnePort.__init__(self,e1,e2,i)
        self.i0 = i0
        self.equation = [(-1 *self.i0, None), (1, i)]
class Resistor(OnePort):
    def __init__(self, r, e1, e2, i):
        OnePort.__init__(self,e1,e2,i)
        self.r = r
        self.equation = [(1,e1), (-1, e2), (-1 *self.r, i)]


#SOLVING CIRCUITS

def flatten_list(l):
    out = []
    for i in l:
        if type(i) == list:
            out.extend(flatten_list(i))
        else:
            out.append(i)
    return out
def Potentiometer(rp, alpha, e1, e2, e3, i1, i2):
    r1 = Resistor((1- alpha) * rp, e1, e2, i1)
    r2 = Resistor((alpha) * rp, e2, e3, i2)
    return [r1,r2]
def solveCircuit(componentList, GND):
    # flatten_list is necessary for lists that contain two-ports,
    # which will be introduced in exercises over the nex few weeks.
    # It has no effect on lists that contain just one-ports.
    # Do not remove the following line.
    componentList = flatten_list(componentList)
    equations = []
    nodes = []
    for onePortInstance in componentList:
        equations.append(onePortInstance.equation)
        nodes.append(onePortInstance.e1)
        nodes.append(onePortInstance.e2)
    nodes = list(set(nodes))
    nodes.remove(GND)
    comps = []
    for node in nodes:
        for onePortInstance in componentList:
            if node == onePortInstance.e1:
                comps.append((1,onePortInstance.i))
            elif node == onePortInstance.e2:
                comps.append((-1, onePortInstance.i))
        equations.append(comps)
        comps = []
    ground = [(1,GND)]
    equations.append(ground)
    return solveEquations(equations, verbose = False)
def solving(alpha, a):
    V1 = VSrc(17, 'e1', 'gnd', 'i0')
    p1 = Potentiometer(7000, alpha, 'e1', 'out', 'gnd', 'i1', 'i4')
    r2 = Resistor(1000, 'e1', 'out', 'i2')
    r3 = Resistor(1000, 'out', 'gnd', 'i3')
    circuitComponents = [V1, p1,r2,r3]
    output = solveCircuit(circuitComponents, 'gnd')
    a.append(output['out'])
class VoltageSensor(OnePort):
    def __init__(self, e1, e2, i):
        OnePort.__init__(self,e1,e2,i)
        self.e1 = e1
        self.e2 = e2
        self.i = i
        self.equation = [(1,i)]
    
class VCVS(OnePort):
    def __init__(self, sensor, e1, e2, i, K=1000000):
        OnePort.__init__(self,e1,e2,i)
        self.e1 = e1
        self.e2 = e2
        self.i = i
        self.equation = [(1,e1),(-1,e2),(-K, sensor.e1), (K,sensor.e2)]

def OpAmp(ea1, ea2, Ia, eb1, eb2, Ib, K=1000000):
    sensor = VoltageSensor(ea1, ea2, Ia)
    vcvs = VCVS(sensor, eb1, eb2, Ib,K)
    return [sensor, vcvs]
Ipmt = (760.0 * (10.0 **(-12.00)))
Isrc = ISrc (Ipmt, 'e0', 'gnd', 'i0')
r1 = Resistor(27000000.0, 'e0', 'transamp_out', 'i2')
r2 = Resistor(2900.0, 'transamp_out', 'e2', 'i3')
r3 = Resistor(290000.0, 'e2', 'v_out', 'i4')
o1 = OpAmp('e0', 'gnd', 'i5', 'gnd', 'transamp_out', 'i6')
o2 = OpAmp('e2', 'gnd', 'i7', 'gnd', 'v_out', 'i8')

circuitComponents = [Isrc, r1,r2,r3,o1,o2] #your code here
print solveCircuit(circuitComponents, 'gnd')
