import json

from Base import Base
from Node import Node
from Element import Element
from Profile import Profile
from LProfile import LProfile
from SProfile import SProfile
from OProfile import OProfile

# one helper function to flatten the list 
def flatten(l):
    return [item for sublist in l for item in sublist]

# read the input file 
filename = "input.json"
IData = {}
with open(filename, 'r') as file:
    try: 
        IData = json.load(file)
    except: 
        print("**** Please check the input file!")

# check if verbos 
if "verbos" in IData.keys():
    print IData["verbos"]
    Base.setVerbos(IData["verbos"])


# check if the output file name is changed
if "output" in IData.keys():
    Base.setLogFileName(IData["output"])
# Set profile name 

try: 
    PName = IData["Name"]
    # p = Profiel(PName)
except:
    raise Exception("*** error: Missing Profile Name")

# now lets create elements from the input file
# in the begining we have 0 sections
l = 0 
o = 0
s = 0
sectionList = {}
elementsList = []

for key in IData["Profiles"].keys():
    if IData["Profiles"][key]["Type"] == "L":
        l += 1
        data = IData["Profiles"][key]
        sectionList[key] = LProfile(data)
        elementsList.append(sectionList[key].getLElements())
    
    elif IData["Profiles"][key]["Type"] == "S":
        s += 1
        data = IData["Profiles"][key]
        sectionList[key] = SProfile(data)
        elementsList.append(sectionList[key].getSElements())

    elif IData["Profiles"][key]["Type"] == "O":
        o += 1
        data = IData["Profiles"][key]
        sectionList[key] = OProfile(data)
        elementsList.append(sectionList[key].getOElements())



elementsList = flatten(elementsList)
p = Profile(PName)
for e in elementsList: p.addElement(e)
p.computeProfileProps()
p.logData()


# by default the view is on if input file has view = "False" the preview will not be shown
if "view" in IData.keys():
    if IData["view"] == "True" :
        p.view()
else:
    p.view()
