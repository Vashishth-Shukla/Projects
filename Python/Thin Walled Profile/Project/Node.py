# -*- coding: utf-8 -*-
# sets the encoding to utf-8 to help the text editor show the file in the right way 

# import block

from Base import Base

# here we define the subclass of Base class, the Node class

class Node(Base):
    # class properties available only *once* (global variables, "class variables"!)
    _Ncounter   = 0                 # initialize the object counter
    _NnextId    = 1                 # initialize id of the next object to instantiate
    _nodeList   = [[]]              # this will keep the data of all the created nodes
                #   | added empty set to start counter from 1 insted of 0

    # constructor 

    def __init__(self,x,y):
        
        # set global log file variable
        try:
            self._x = [float(x), float(y)]
            if self._x in Node._nodeList:
                self._nodeNr = Node._nodeList.index([x,y])
                Node.appendLog("Found Node %d: x = %10.4f, y = %10.4f" %(self._nodeNr, self._x[0], self._x[1] ))
            else:
                self._nodeNr = Node._NnextId
                Node._NnextId  += 1
                Node._Ncounter += 1
                Node._nodeList.append(self._x)
        except Exception as e:          # catch exception...
            self.appendLog(e.message)   # ...and add to log file
            # raise a new exception to stop the run!
            raise Exception("*** Node data error! (obj. id: %d)" %self._id )

    def logData(self):
        # log the created instance
        Node.appendLog("   Created Node %d: x = %10.4f, y = %10.4f" %(self._nodeNr, self._x[0], self._x[1] ))
        

    def __del__(self):
        self.appendLog("deleting Node %d." %self._nodeNr )
        Node._Ncounter -= 1
    
    def getNodeNumber(self):
        return self._nodeNr