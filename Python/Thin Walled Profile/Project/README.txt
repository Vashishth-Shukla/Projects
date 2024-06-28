Welcome to the Profile Properties Calculator

In order to Calculate the profile properties, follow the 2 simple steps
1. update the "input.json" file. 
2. press the "run.bat"



This program can work with L sections, Square sections(S sections) and Circular Sections.
To know the input parameters to put in the input.json file check the "InputFileTemplate.json"

Please note,
    - To run the run.bat file "python2.7" need to be in environment variable. (To check run "python --version" in command prompt and it should return version of Python 2.7)
    - You need to imput the coordinates of the points for the "centerlines" for each elements that you want to add to the profile
    - You can change the name of the output file in input file.
    - To change the input file name you need to open the main.py file and change the line 16 "filename = "input.json"
    - for L profile the p2 has to be the common points for the 2 elements
    - you can provide thickness to each element in L profile, T1 -> Element[P1,P2] and T2 -> [P2,P3] 
    - if only the T1 is given, it will be implimented to both the elements.
    - for S profile the points need to be in clockwise or anti-clockwise direction
    - in S profile you can define 4 thickness, if not provided the T1 will be implimented to all the elements
    

This app contains following files
    - main.py
    - Base.py
    - Node.py
    - Element.py
    - Profile.py
    - LProfile.py
    - SProfile.py
    - OProfile.py