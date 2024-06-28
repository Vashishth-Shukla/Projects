# 2D Insulated beam
# No volumetric heat source,viscosity and gravity 
# This problem is a Benchmark for analizing two way coupling
import numpy as np
import matplotlib.pyplot as plt
import PyFEMP
import Insulated_plate_elmt_static as ELEMENT

FEM = PyFEMP.FEM_Simulation(ELEMENT) # starting simulation by creating a FEM_Solution object
a = 0.2
n = 20
#                         |lower left corner
#                                     |upper right corner
#                                               |'doppelt', more elements in mesh for x direction
#                                                         |meshtype: linear triangles or linear rectangular elements
XI, Elem = PyFEMP.msh_rec([0.0, 0.0], [a + 0.8 , a + 0.3], [n*2, n], type='Q1') # XI: nodes of geometry | Elem: Q1
FEM.Add_Mesh(XI, Elem)
# Material parameters are:    
#                   E    -> Young's modulus N/(mm^2) ############# UNITS ##############
#                   nu   -> Poisson's ratio
#                   rho  -> density
#                   c_a  -> thermal conductivity
#                   c_T  -> specific heat capacity
#                   T0   -> stress free reference temperature
#                   cu   -> thermal expansion coefficient
#                   cs   -> multiplicator on the nonlinear coupling term (0 -> off, 1-> on)????
#                   by   -> gravity

# set list of material parameter for each material
steel = [210e9, 0.25, 7850, 45, 502, 293.15,16e-6, 1, 0]
foam  = [40e6, 0.25, 30, 20e-3, 2.1e3, 293.15, 4e-5, 1, 0] 

# set material for each element successively
for i,elmt in enumerate(Elem):
    #compute center of element
    elmt_centr = np.mean(XI[elmt], axis = 0)
    if (elmt_centr[0] > a and elmt_centr[1] < 0.3):
        FEM.Add_Material(steel)
    else:
        FEM.Add_Material(foam)

# Fixing bottom left
bottom_foam  = "y==0 and x>=0 and x<="+str(a)
bottom_steel = "y==0 and x<="+str(a)+"+ 0.2 and x>="+str(a)

FEM.Add_EBC(bottom_foam,  "UY", 0)
FEM.Add_EBC(bottom_steel,  "UX", 0)
FEM.Add_EBC(bottom_steel,  "UY", 0)

# Fixing right wall
right_wall = "x=="+str(a)+" +0.8"
FEM.Add_EBC(right_wall,  "UX", 0)

## Temperature change as dofs
dT_out = 30
dT_bottom = 0 

top_foam = "y== "+str(a)+" + 0.3"
free_steel_bottom = "y==0 and x>= "+str(a)+"+ 0.2 and x<="+str(a)+" + 0.8"

FEM.Add_EBC("x==0",  "DT", dT_out)
FEM.Add_EBC(top_foam,  "DT", dT_out)
FEM.Add_EBC(free_steel_bottom,  "DT", dT_bottom)

FEM.Analysis()

#            |time step as one, because it is steady
#                 |load just once, because the problem is linear and steady
FEM.NextStep(1.0, 1.0)

# produces two outputs: |R| (norm of current residual vector) and |dDI| (norm of the increment of the increment of dofs in newton iteration)
# after that a value returns = sqrt(|R|*|dDI|) If this value is zero, the solution converges!
print( FEM.NewtonIteration() )
print( FEM.NewtonIteration() )

ux = FEM.NodalDof("x==1 and y==0.5", "UX") # define a variable 'ux' which is the displacement in x direction at a chosen position -> here: P(1|0.5)
uy = FEM.NodalDof("x==1 and y==0.5", "UY")
dt = FEM.NodalDof("x==0.5 and y==1.5/6", "DT") # temperature at P(0.5|1.5/6)
dtup = FEM.NodalDof("x==0.5 and y==0.5", "DT")
print('ux :',ux, 'uy :',uy, 'dt :',dt, 'dtup: ', dtup) # print above defined values to the output terminal

# create two plots in one row with a defined size (2,1 would be 2 plots in one column)
#    |-------------------> creates a vector 'ax' with a size of 2 for two plots
fig, ax = plt.subplots(1,2, figsize=(21.0, 7.5)) 
postplot1 = FEM.ShowMesh(ax[0], deformedmesh=True, PostName="T") # ax[0] shows first created plot, ax[1] the second one
ax[0].set_xlim(0, 1.0) # defines the length of the plot
ax[0].set_ylim(0, 0.5) # defines the height of the plot
ax[0].set_xlabel(' x (m)')
ax[0].set_ylabel(' y (m)')
ax[0].set_title(" Heat distribution for a = {} and n = {} ".format(a,n))
cbar1 = fig.colorbar(postplot1, ax=ax[0]) # creates a colorbar for postplot 1 | ax[0] would be right of first plot and ax[1] would be right of second plot
cbar1.set_label('absolute temperature $ {\\theta}$ in K') # text of above created colorbar
postplot2 = FEM.ShowMesh(ax[1], deformedmesh=True, PostName="SigMises")
ax[1].set_xlim(0, 1.0)
ax[1].set_ylim(0, 0.5)
ax[1].set_xlabel(' x (m)')
ax[1].set_ylabel(' y (m)')
ax[1].set_title(" Stress distribution for a = {} and n = {} ".format(a,n))
cbar2 = fig.colorbar(postplot2, ax=ax[1])
cbar2.set_label('von Mises stress $\sigma_{VM}$ in MPa')
plt.show() # showing the above defined plots

