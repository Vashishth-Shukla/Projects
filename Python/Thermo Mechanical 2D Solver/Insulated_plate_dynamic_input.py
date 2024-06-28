# 2D Insulated beam
# No volumetric heat source,viscosity and gravity 
# This problem is a Benchmark for analizing two way coupling
import numpy as np 
import matplotlib.pyplot as plt
import PyFEMP
import Insulated_plate_elmt_dynamic as ELEMENT

FEM = PyFEMP.FEM_Simulation(ELEMENT)
a = 0.2
n = 10
XI, Elem = PyFEMP.msh_rec([0.0, 0.0], [1, 0.5], [n*2, n], type='Q1')
FEM.Add_Mesh(XI, Elem)
# Material parameters are:
#                   E    -> Young's modulus
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
    #computer center of element
    elmt_centr = np.mean(XI[elmt], axis = 0)
    if (elmt_centr[0] > 0.2 and elmt_centr[1] < 0.3):
        FEM.Add_Material(steel)
    else:
        FEM.Add_Material(foam)
        
# Fixing bottom left
FEM.Add_EBC("y==0 and x<=0.2 and x>=0 ",  "UY", 0)
FEM.Add_EBC("y==0 and x<=0.4 and x>=0.2 ",  "UX", 0)
FEM.Add_EBC("y==0 and x<=0.4 and x>=0.2 ",  "UY", 0)

# Fixing right wall
FEM.Add_EBC("x==1",  "UX", 0)

## Temperature change as dofs
FEM.Add_EBC("x==0",  "DT", 80)
FEM.Add_EBC("y==0.5",  "DT", 80)
FEM.Add_EBC("x<=1 and x>=0.4 and y==0",  "DT", 0)

FEM.Analysis()

time  = 0.0
dt    = 600
nStep = 80
animation = True
times = [0]
uys   = [0]
uxs   = [0]

def load(time):
    if (time< 1):
        
       return time

    else:
       
       return 1 # Our load is applied for 
   
for step in range(nStep):
  time += dt
  
  FEM.NextStep(time, load(time))
  print( FEM.NewtonIteration() )
  print( FEM.NewtonIteration() )

  ux = FEM.NodalDof("x==0.01 and y==0", "UX")
  uy = FEM.NodalDof("x==0.01 and y==0", "UY")
  print('ux :', ux, 'uy :', uy)

  times.append(time)
  uys.append(uy)
  uxs.append(ux)
  
  if animation:
    if (step==0): fig, ax = plt.subplots(1,2, figsize=(14.0, 5.0))

    ax[0].cla()
    postplot1 = FEM.ShowMesh(ax[0], deformedmesh=True, PostName="T")
    ax[0].set_xlabel(' x (m)')
    ax[0].set_ylabel(' y (m)')
    ax[0].set_xlim(0, 1.0) # defines the length of the plot
    ax[0].set_ylim(0, 0.5) # defines the height of the plot
    ax[0].set_title(" Heat distribution over time, current time {}".format(time))
    cbar1 = fig.colorbar(postplot1, ax=ax[0]) # creates a colorbar for postplot 1 | ax[0] would be right of first plot and ax[1] would be right of second plot
    cbar1.set_label('absolute temperature $ {\\theta}$ in [K]') # text of above created colorbar
    
    ax[1].cla()
    postplot2 = FEM.ShowMesh(ax[1], deformedmesh=True, PostName="SigMises")
    ax[1].set_xlabel('x (m)')
    ax[1].set_ylabel('y (m)')
    ax[1].set_xlim(0, 1.0)
    ax[1].set_ylim(0, 0.5)
    ax[1].set_title(" Stress distributions over time, current time {} ".format(time))
    cbar2 = fig.colorbar(postplot2, ax=ax[1])
    cbar2.set_label('von Mises stress $\sigma_{VM}$ in [MPa]')

    fig.tight_layout() # space between subplots

    plt.pause(0.00001)
    cbar1.remove()
    cbar2.remove()
  
plt.show()

# save data in files for later post processing
np.save('time_data',times)
np.save('x_disp_data',uxs)
np.save('y_disp_data',uys)
