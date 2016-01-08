class Polynomial:
    
    ## Intialize a polynomial with a list of coefficients.
    ## The coefficient list starts with the highest order term.
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.order = len(coeffs)-1

    ## Return the coefficient of the x**i term
    def coeff(self,i):
    	if i < 0 :
    		return 0.000
    	elif i > (len(self.coeffs)-1):
    		return 0.000
    	else:
    		return self.coeffs[len(self.coeffs)-(i+1)]

    ## Return the value of this Polynomial evaluated at x=v
    def val(self, v):
        sum = 0
        for coeff in self.coeffs:
            sum = sum*v + coeff
        return sum

    ## Return the roots of this Polynomial
    def roots(self):
        roots = []
        if len(self.coeffs) == 2:
                roots.append(-self.coeffs[1]/self.coeffs[2])
        elif len(self.coeffs) ==3:
                descriminant = complex((self.coeffs[1]*self.coeffs[1])-4*self.coeffs[0]*self.coeffs[2],0)
                plusRoot = (complex(-self.coeffs[1],0)+(descriminant)**(1/2.0))/(complex(2*self.coeffs[0],0))
                minusRoot = (complex(-self.coeffs[1],0)-(descriminant)**(1/2.0))/(complex(2*self.coeffs[0],0))
                roots.append(plusRoot)
                roots.append(minusRoot)
        else:
            raise ValueError('polynomial of inappropriate order')
        return roots
    ## Add two polynomials, return a new Polynomial
    def add (self, other):
        min_length = min(len(other.coeffs),len(self.coeffs))
        return Polynomial(self.coeffs[:-min_length]+other.coeffs[:-min_length]+[self.coeffs[i]+other.coeffs[i] for i in range(-min_length,0)])

    ## Multiply two polynomials, return a new Polynomial
    def mul(self, other):
        newPolynomial = [0] * (len(self.coeffs)+len(other.coeffs)-1)
        for index1,coeff1 in enumerate (self.coeffs):
            for index2,coeff2 in enumerate (other.coeffs):
                newPolynomial[index1+index2]+=coeff1*coeff2
        return Polynomial(newPolynomial)

    def __add__(self, other):
        #override the + operator so we can do things like p1+p2
        return self.add(other)

    def __mul__(self, other):
        #override the * operator so we can do things like p1*p2
        return self.mul(other)

    def __str__(self):
        coeffs = [self.coeff(i) for i in xrange(self.order,-1,-1)]
        return 'Polynomial(%r)' % coeffs


### Test Cases:

# Test Case 1 (Should print: [2, 0, 100])
# Test of order attribute
import random
p1 = Polynomial([1, 3, 2])
p2 = Polynomial([1])
p3 = Polynomial([random.randint(1, 100) for i in range(101)])
ans = [p1.order, p2.order, p3.order]
print "Test Case 1:", ans

# Test Case 2 (Should print: [7, 6, 8, 5, 4])
# Test of coeff method
a = Polynomial([4, 5, 8, 6, 7])
ans = [a.coeff(i) for i in xrange(a.order+1)]
print "Test Case 2:", ans

# Test Case 3 (Should print: [[10, 9, 12, 1], [10, 9, 12, 1]])
# Test of add method
p1 = Polynomial([1, 3, 2, 4])
p2 = Polynomial([9, 7, 6])
a = p1.add(p2)
b = p2.add(p1)
ans = [[a.coeff(i) for i in xrange(a.order+1)], [b.coeff(j) for j in xrange(b.order+1)]]
print "Test Case 3:", ans

# Test Case 4 (Should print: [3, 2, 1, 6, 4, 2])
# Test of mul method
p1 = Polynomial([1,2,3])
p2 = Polynomial([2, 0, 0, 1])
a = p1.mul(p2)
ans = [a.coeff(i) for i in xrange(a.order+1)]
print "Test Case 4:", ans

# Test Case 5 (Should print: [(-1+0j), (-2+0j)])
# Roots
p = Polynomial([1, 3, 2])
ans = p.roots()
print "Test Case 5:", ans

# Test Case 6 (Should print: [(-0.33333333333333326+0.9428090415820635j), (-0.3333333333333334-0.9428090415820635j)])
# Roots
p = Polynomial([3, 2, 3])
ans = p.roots()
print "Test Case 6:", ans

#The test case:
a = Polynomial([0.7581006627662801, 0.34261322847768216, 0.8481519839339997])
ans = ["%.03f" % a.coeff(i) for i in xrange(-1, a.order+2)]
print ans