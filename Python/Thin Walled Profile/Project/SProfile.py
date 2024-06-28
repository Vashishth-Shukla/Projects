from Element import  Element

# this class will make the SProfiles

class SProfile(Element):
    # SProfile will take name and 3 coordinates and at least 1 thickness (if provided 2) in one dictionary
    _SPcounter       = 0                 # initialize the object counter
    _SPnextId        = 1                 # initialize id of the next object to instantiate

    def __init__(self,dic):
        self._no = SProfile._SPnextId
        SProfile.appendLog("Created SProfile %d" %(self._no))
        # self._elements = []
        SProfile._SPnextId  += 1
        SProfile._SPcounter += 1
        
        try:
            self._x1 = dic["P1"]
            self._x2 = dic["P2"]
            self._x3 = dic["P3"]
            self._x4 = dic["P4"]
            
            self._t1 = dic["t1"]
            if "t2" in dic.keys():
                self._t2 = dic["t2"]
            else: 
                self._t2 = dic["t1"]

            if "t3" in dic.keys():
                self._t3 = dic["t3"]
            else: 
                self._t3 = dic["t1"]

            if "t4" in dic.keys():
                self._t4 = dic["t4"]
            else: 
                self._t4 = dic["t1"]

        except Exception as e:          # catch exception...
            self.appendLog(e.message)   # ...and add to log file
            # raise a new exception to stop the run!
            raise Exception("*** SProfile data error! (obj. id: %d)" %self._no )
        
        # create elements 
        self._el = [Element(self._x1,self._x2,self._t1), Element(self._x2,self._x3,self._t2),
                    Element(self._x3,self._x4,self._t3), Element(self._x4,self._x1,self._t4)]
        # for self._e in self._el: self._elements.append(self._el)


    def __del__(self):
        self.appendLog("deleting SProfile %d." %self._no )
        SProfile._SPcounter -= 1
    
    
    def getSElements(self):
        return self._el