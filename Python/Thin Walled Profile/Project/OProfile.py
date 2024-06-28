from Element import  Element
from math import pi, cos, sin

# this class will make the OProfiles

class OProfile(Element):
    # OProfile will take name and 3 coordinates and at least 1 thickness (if provided 2) in one dictionary
    _OPcounter       = 0                 # initialize the object counter
    _OPnextId        = 1                 # initialize id of the next object to instantiate

    def __init__(self,dic):
        self._no = OProfile._OPnextId
        OProfile.appendLog("Created OProfile %d" %(self._no))
        self._el = []                    # defining an empty element list
        OProfile._OPnextId  += 1
        OProfile._OPcounter += 1
        
        try:
            self._c = [float(dic["C"][0]),float(dic["C"][1])]
            self._r  = float(dic["r"])
            self._n  = int(dic["n"])            
            self._t  = float(dic["t"])


        except Exception as e:          # catch exception...
            self.appendLog(e.message)   # ...and add to log file
            # raise a new exception to stop the run!
            raise Exception("*** OProfile data error! (obj. id: %d)" %self._no )
        # if n < 3, we make n = 3
        if self._n <3:
            self._n = 3

        # create points and elements in one loop
        # here ... to start with the top point we have used x = c1x + r*sin(theta); y = c1y + r*cos(theta)
        # this will creat a counter-clockwise circle

        for i in range(self._n):
            # find the first node 
            x = self._c[0]+(self._r*sin(2*pi*i/self._n))
            y = self._c[1]+(self._r*cos(2*pi*i/self._n))
            x1 = [x,y]
            # find the next node 
            x = self._c[0]+(self._r*sin(2*pi*(i+1)/self._n))
            y = self._c[1]+(self._r*cos(2*pi*(i+1)/self._n))
            x2 = [x,y]
            #now from these 2 nodes make one element and add to the element list
            self._el.append(Element(x1,x2,self._t))
        



        # self._el = [Element(self._x1,self._x2,self._t1), Element(self._x2,self._x3,self._t2),
        #             Element(self._x3,self._x4,self._t3), Element(self._x4,self._x1,self._t4)]
        # for self._e in self._el: self._elements.append(self._el)


    def __del__(self):
        self.appendLog("deleting OProfile %d." %self._no )
        OProfile._OPcounter -= 1
    
    
    def getOElements(self):
        return self._el