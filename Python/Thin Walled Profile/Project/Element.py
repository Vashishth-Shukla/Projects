# from Base import Base
from Node import Node
from math import sqrt

# here we define the subclass of Base class, the Node class

class Element(Node):
    # class properties available only *once* (global variables, "class variables"!)
    _Ecounter       = 0                 # initialize the object counter
    _EnextId        = 1                 # initialize id of the next object to instantiate
    _elementList    = [[]]              # this will keep the data of all the created nodes
                    #   | added empty set to start counter from 1 insted of 0


    # constructor 

    def __init__(self,x1,x2,t):         # it takes ... [x1],[x2]
        self._no = Element._EnextId
        self._n     = []                # node list
        Element._EnextId  += 1
        Element._Ecounter += 1
        # set global log file variable
        n1 = Node(x1[0],x1[1])
        self._node1 = n1.getNodeNumber()
        n2 = Node(x2[0],x2[1])
        self._node2 = n2.getNodeNumber()
        self._t  = float(t)

        # check the Node references
        if not isinstance(n1,Node): \
            raise Exception("*** error: invalid node 1")
        if not isinstance(n2,Node): \
            raise Exception("*** error: invalid node 2")


        
        self._n = [n1,n2]
        Element.appendLog("Created Element %d" %(self._no))


    def __del__(self):
        self.appendLog("deleting Element %d." %self._no )
        Element._Ecounter -= 1

    # calculate the difference of the node coordinates
    # i: direction 0:x / 1:y
    def getX(self,i):
        return self._n[1]._x[i] - self._n[0]._x[i]

    def getT(self):
        # RO: Pythagorean theorem
        return self._t

    # calculate the length of the element
    def getL(self):
        # RO: Pythagorean theorem
        return sqrt( (self._n[0]._x[0] - self._n[1]._x[0] )**2 + \
                     (self._n[0]._x[1] - self._n[1]._x[1] )**2 )

    # calculate area of the element
    def getA(self):
        return self.getL()*self._t

    # center coordinate of the element
    # i: direction 0:x / 1:y
    def getC(self,i):
        return (self._n[0]._x[i] + self._n[1]._x[i])/2.

    # calculate the static moment
    # i: direction 0:x / 1:y
    def getS(self,i):
        return self.getC((i+1)%2)*self.getA() # (i+1)%2 gives 'the other direction'

    # calculate area moments of inertia
    # i: direction; 0:xx / 1:yy / 2:xy
    def getI(self,i):
        if   i == 0:    # I_xx
            return (self.getX(1)**2/12. + self.getC(1)**2)*self.getA()
        elif i == 1:    # I_yy
            return (self.getX(0) ** 2 / 12. + self.getC(0) ** 2) * self.getA()
        elif i == 2:    # deviation moment I_xy
            return -(self.getX(0)*self.getX(1)/12. + self.getC(0)*self.getC(1)) \
                    *self.getA()

    # print element's data into the log-file
    def logData(self):
        self.appendLog("> Element %d: t = %.2f mm, l = %.2f mm" % \
                       (self._no, self._t, self.getL()))

        # list node data
        for n in self._n: n.logData()

        # section values
        self.appendLog("   A................: %10.2f mm^2" % \
                       (self.getA(),))
        self.appendLog("   Sx and Sy........: %10.2f %10.2f mm^3" % \
                       (self.getS(0),self.getS(1)))
        self.appendLog("   Ixx, Iyy and Ixy.: %10.2f %10.2f %10.2f mm^4" % \
                       (self.getI(0),self.getI(1),self.getI(2)))
