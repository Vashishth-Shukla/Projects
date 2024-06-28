# -*- coding: utf-8 -*-
# sets the encoding to utf-8 to help the text editor show the file in the right way 

# import block
from datetime import datetime

class Base:

    # class properties (not the properties of the instance)
    _log        = "log.txt"             # defauld log file name
    _verbos     = True                  # put all log in terminal

    @classmethod    # class method -> is available independently of object instances
    def appendLog(cls, text):
        t = datetime.now()
        tstamp = "%2.2d:%2.2d:%2.2d| " %(t.hour, t.minute, t.second)
        textout = tstamp + str(text)
        f = open(Base._log, "a")  # (a)ppend to log
        f.write(textout + "\n")
        f.close()
        if Base._verbos : print "appendLog(): ", textout

    @classmethod
    def clearLogFile(cls):
        import os
        try:
            os.remove(Base._log)
        except:
            print "*** clearLogFile(): could not delete log file"

    @classmethod
    def setLogFileName(cls,name):
        Base._log = name
        Base.clearLogFile()
        Base.appendLog("log file set to '" + name + "'")


    @classmethod
    def setVerbos(cls,boolvar):
        Base._verbos = boolvar
        Base.appendLog("Verbos set to '" + str(boolvar) + "'")