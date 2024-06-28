from Element import  Element

# this class will make the LProfiles

class LProfile(Element):
    # LProfile will take name and 3 coordinates and at least 1 thickness (if provided 2) in one dictionary
    _LPcounter       = 0                 # initialize the object counter
    _LPnextId        = 1                 # initialize id of the next object to instantiate

    def __init__(self,dic):
        self._no = LProfile._LPnextId
        LProfile.appendLog("Created LProfile %d" %(self._no))
        self._elements = []
        LProfile._LPnextId  += 1
        LProfile._LPcounter += 1
    
        try: 
            self._x1 = dic["P1"]
            self._x2 = dic["P2"]
            self._x3 = dic["P3"]
            self._t1 = dic["t1"]
            if "t2" in dic.keys():
                self._t2 = dic["t2"]
            else: 
                self._t2 = dic["t1"]
        except Exception as e:          # catch exception...
            self.appendLog(e.message)   # ...and add to log file
            # raise a new exception to stop the run!
            raise Exception("*** LProfile data error! (obj. id: %d)" %self._no )
        
        # create elements 
        self._el = [Element(self._x1,self._x2,self._t1), Element(self._x2,self._x3,self._t2)]
        # for self._e in self._el: self._elements.append(self._el)


    def __del__(self):
        self.appendLog("deleting LProfile %d." %self._no )
        LProfile._LPcounter -= 1
    
    
    def getLElements(self):
        return self._el