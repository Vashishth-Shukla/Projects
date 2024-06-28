@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@echo +                 welcome tho the program              +
@echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@echo "<-<-<-<-<-<-<-<-<-<-<-<-<-<-->->->->->->->->->->->->->"
@echo off
path = %path%;C:\mingw64\mingw32\bin;
@echo on


@echo ***  
@echo deleting old Euler.exe
del Euler.exe

@echo ***    
@echo Now, createing new file

gfortran newtonLib.f90 eulerLib.f90 mainEuler.f90 -o Euler.exe
@echo ***
@echo now executing the Euler.exe
@echo ***
Euler.exe

pause