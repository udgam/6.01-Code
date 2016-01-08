class DDist:
    def __init__(self, dictionary):
        if not (abs(sum(dictionary.values())-1) < 1e-6 and min(dictionary.values()) >= 0.0):
            raise Exception, "Probabilities must be nonnegative, and must sum to 1"
        self.d = dictionary

    def prob(self, elt):
        if elt in self.d:
            return self.d[elt]
        else:
            return 0

    def support(self):
        a = []
        for element in self.d.keys():
            if self.d[element] > 0:
                a.append(element)
        return a

    def __repr__(self):
        return "DDist(%r)" % self.d
    
    __str__ = __repr__

    def project(self, mapFunc):
        ans = {}
        for key in self.support():
            if mapFunc(key) not in ans:
                ans[mapFunc(key)] = self.prob(key)
            elif mapFunc(key) in ans:
                ans[mapFunc(key)] += self.prob(key)
        return DDist(ans)

    def condition(self, testFunc):
        supportedValues = []
        totalSum = 0
        for element in self.support():
            if testFunc(element):
                totalSum+=self.prob(element)
                supportedValues.append(element)
        dictionary = {}
        for element in supportedValues:
            dictionary[element] = float(self.prob(element)) / totalSum 
        return DDist(dictionary)


        

def marginalize(d, i):
    return d.project(lambda x : x[:i] + x[i+1:])

def makeJointDistribution(PA, PBgA):
    p = {}
    for elt in PA.support():
        dDist = PBgA(elt)
        for elt2 in dDist.support():
            p[(elt,elt2)] = PA.prob(elt) * dDist.prob(elt2)
    return DDist(p)

def totalProbability(PA, PBgA):
    return makeJointDistribution(PA,PBgA).project(lambda x: x[1]) 

def bayesRule(PA, PBgA, b):
    ab = makeJointDistribution(PA, PBgA)
    result = ab.condition(lambda x: x[1] == b)
    dictionary = {}
    for tup in result.support():
        dictionary[tup[0]] = result.prob(tup)
        return DDist(dictionary)

    bprob = 0
    for a in PA.support():
        bprob += PBgA(a).prob(b)

    dictionary = {}
    for a in PA.support():
        dictionary[a] = float(PBgA(a).prob(b)) * PA.prob(a) / bprob
    return DDist(dictionary)
