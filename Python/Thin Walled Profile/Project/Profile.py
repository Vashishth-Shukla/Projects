# -*- coding: utf-8 -*-
# sets the encoding to utf-8

from Base import Base
from Element import Element
from math import sqrt, atan2, pi

# for pixel to mm we need a multiplication factor

P2MM = 3.7795

class Profile(Base):
    _Pcounter       = 0                         # initialize the object counter
    _PnextID        = 1                         # initialize id of the next ogj
    
    # constructor
    def __init__(self,name):
        self._no = Profile._PnextID
        Profile._PnextID += 1
        Profile._Pcounter += 1
        # input data
        self._name = name     # profile name
        self._e  = []         # Element container (list)
        # profile properties: accumulated element contributions
        self._a  = 0          # area
        self._s  = [0, 0]     # static moments
        self._iu = [0, 0, 0]  # s.m.o.a. in user coordinates
        # profile properties: global profile values
        self._cg = [0, 0]     # center of gravity coordinates
        self._ic = [0, 0, 0]  # s.m.o.a. w.r.t. CG coord.sys.
        self._ip = [0, 0]     # s.m.o.a. principle values
        self._ang = 0         # rotation angle

    def __del__(self):
        self.appendLog("deleting Profile %d." %self._no )
        Element._Ecounter -= 1
    # add elements into the Profile's Element container
    #                   |Element object reference
    def addElement(self,e):
        
        self._e.append(e)               # append e to profile's element list

    # calculate the Profile's result data
    def computeProfileProps(self):
        # check if elements are available
        if len(self._e) < 1:
            raise Exception("*** error: no elements found in profile!")

        ## Part 1: compute accumulated/integral quantities
        for e in self._e:
            self._a += e.getA()                          # area
            for i in range(2): self._s[i]  += e.getS(i)  # static moments
            for i in range(3): self._iu[i] += e.getI(i)  # moment of inertia

        ## Part 2: derived global profile properties
        self._cg[0] = self._s[1] / self._a  # center of gravity (CG) x-coordinate
        self._cg[1] = self._s[0] / self._a  # center of gravity (CG) y-coordinate

        # shift second moments of area to CG coordinate system: parallel axis theorem
        self._ic[0] = self._iu[0] - self._cg[1]**2 * self._a
        self._ic[1] = self._iu[1] - self._cg[0]**2 * self._a
        self._ic[2] = self._iu[2] + self._cg[0]*self._cg[1] * self._a

        # principal axis transformation / principal values of profile's second moment of area
        Ixx = self._ic[0]; Iyy = self._ic[1]; Ixy = self._ic[2]
        self._ip[0] = (Ixx + Iyy + sqrt(4 * Ixy ** 2 + (Ixx - Iyy) ** 2)) / 2
        self._ip[1] = (Ixx + Iyy - sqrt(4 * Ixy ** 2 + (Ixx - Iyy) ** 2)) / 2
        #self._ang  = atan(2*Ixy/(Iyy - Ixx))/2  # RO: this might give div. by 0 for sym. profiles!
        self._ang   = atan2(2*Ixy,Iyy-Ixx)/2  # orientation of principal axis
        self._ang  *= 180/pi  # transform radiant to degrees (use pi as imported from math)

    # list the profile's properties
    def logData(self):
        self.appendLog("---- Begin Profile Data Output ----")
        self.appendLog("Profile Name: " + self._name)
        self.appendLog("  Area...................................A: %8.2f" % \
                       (self._a))
        self.appendLog("  Static Moments in User-Coordinates.Sx,Sy: %8.2f %8.2f" % \
                       (self._s[0],self._s[1]))
        self.appendLog("  Moment of Inertia in UC - ...Ixx,Iyy,Ixy: %8.2f %8.2f %8.2f" % \
                       (self._iu[0],self._iu[1],self._iu[2]))

        self.appendLog("  Center of Gravity (CG) Coordinates.ex,ey: %8.2f %8.2f" % \
                       (self._cg[0],self._cg[1]))
        self.appendLog("  Shifted MoI in CG coord-sys. Ixx,Iyy,Ixy: %8.2f %8.2f %8.2f" % \
                       (self._ic[0],self._ic[1],self._ic[2]))
        self.appendLog("  MoI principle values .........Ieta,Izeta: %8.2f %8.2f" % \
                       (self._ip[0],self._ip[1]))
        self.appendLog("  Rotation angle..........................: %8.2f °" % self._ang)

        # list data of all associated elements
        for elem in self._e: elem.logData()
        self.appendLog("---- End Profile Data Output ----")

    # view the profile's shape
    def view(self):
        try: # check for pylab
            import pylab
            self.appendLog("Profile.view(): pylab imported!")
        except:
            self.appendLog("*** Profile.view() error: pylab not found!")
            return
        # for each element in the profile...
        for e in self._e:
            
            x1 = e._n[0]._x[0]                 # x of 1st node
            x2 = e._n[1]._x[0]                 # x of 2nd node
            y1 = e._n[0]._x[1]                 # y of 1st node
            y2 = e._n[1]._x[1]                 # y of 2nd node
            pylab.plot([x1,x2], [y1,y2], 'b', linewidth = e.getT()*P2MM)  # draw element as (b)lue line
            pylab.plot([x1,x2], [y1,y2], 'ro') # draw nodes as (r)ed (p)oints
            # Center of gravity for each element
            x = e.getC(0)
            y = e.getC(1)  
            pylab.plot(x,y, 'ko')
            # Annotations
            # we have "element no: ", e._no, " node-number of node1: ", e._node1," node-number of node2: ", e._node2
            # the node numbers
            # pylab.text(x1,y1,"%2.2d"%e._node1,textcoods = "offset points", ha="center")
            # pylab.text(x2,y2,"%2.2d"%e._node2,textcoods = "offset points", ha="center")
            pylab.annotate("N%2.2d"%e._node1,
                            (x1,y1),
                            color="red",size="12",
                            textcoords="offset points", # how to position the text
                            xytext=(0,10), # distance from text to points (x,y)
                            ha='center')
            pylab.annotate("n%2.2d"%e._node2,
                            (x2,y2),
                            color="red",size="12",
                            textcoords="offset points", # how to position the text
                            xytext=(0,10), # distance from text to points (x,y)
                            ha='center')
            # the element numbers 
            pylab.annotate("E%2.2d"%e._no,
                            (x,y),
                            color="black",size="12",
                            textcoords="offset points", # how to position the text
                            xytext=(0,10), # distance from text to points (x,y)
                            ha='center')

            # pylab.annotate("%2.2d"%e._no)
        # figure setting and save/view figure
        # pylab.tight_layout()
        pylab.axis('equal')                    # equal axis ticks
        pylab.title(self._name)                # set figure title
        pylab.savefig(self._name + ".png")     # save to file
        pylab.show()                           # show plot
