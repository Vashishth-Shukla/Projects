import numpy as np

# The 2D quadrilateral element for Coupled Problems WS21/22
NoDim   = 2
NoNodes = 4
# Each node carries three degrees of freedom:
#                   UX -> displacement in x-direction
#                   UY -> displacement in y-direction
#                   DT -> temperature increment T = T0 + DT
NoNodalDofs = 3
# For the temporal discretization we need for each node:
#                        h_I = [a_1, a_2, v_1, v_2, u_1, u_2, ddotT, dotT, T]
NoNodalHist = 9
# Material parameters are:
#                   E    -> Young's modulus
#                   nu   -> Poisson's ratio
#                   rho  -> density
#                   c_a  -> thermal conductivity
#                   c_T  -> specific heat capacity
#                   T0   -> stress free reference temperature
#                   cu   -> thermal expansion coefficient
#                   cs   -> multiplicator on the nonlinear coupling term (0 -> off, 1-> on)
#                   b    -> gravity
def Elmt_Init():
    '''
    The Elmt_Init() function is used to introduce the element to PyFEMP.
    '''
    NoElementDim         = NoDim                    # number of dimensions
    NoElementNodes       = NoNodes                  # number of nodes of this element
    NoElementHistory     = NoNodes*NoNodalHist      # number of scalar history parameters
    ElementDofNames      = ["UX", "UY","DT"]        # list with string names for each dof
    # list with string name for material paramter
    ElementMaterialNames = ["E", "nu", "rho", "c_a", "c_T", "T0", "cu", "cs", "by"]
    # list with string name for postprocessing
    ElementPostNames     = ["UX", "UY", "T", "SigMises"]
    return NoElementDim, NoElementNodes, ElementDofNames, NoElementHistory, ElementMaterialNames, ElementPostNames

def Elmt_KS(XL, UL, Hn, Ht, Mat, dt):
    '''
    The Elmt_KS(XL, UL, Hn, Ht, Mat, dt) function returns the element vector and matrix.
    Input:
            XL  = [x11, x12, x21, x22, ..., xn2]    -> np.vector of nodal coordinates for n-Nodes in 2d
            UL  = [u11, u12, u21, u22, ..., un2]    -> np.vector of current nodal dofs for n-Nodes and 2 dofs at each
            Hn  = [h1, h2,... hm]                   -> np.vector for the previous history of length m (! do NOT write in here)
            Ht  = [h1, h2,... hm]                   -> np.vector for the updated history of length m (!write in here)
            Mat = [M1, M2, ... Mo]                  -> list of material parameter in the order defined in Elmt_Init()
            dt  = dt                                -> time step size
    '''
    verbose = False  # True;
    if verbose: print('XI :',XL)
    if verbose: print('UI :',UL)
    if verbose: print('Hn :',Hn)
    if verbose: print('Ht :',Ht)
    if verbose: print('b  :',Mat)
    if verbose: print('dt :',dt)

    # initialize element vector /matrix
    r_e = np.zeros(NoNodes*NoNodalDofs)
    k_e = np.zeros((NoNodes*NoNodalDofs, NoNodes*NoNodalDofs))

    # read in material parameter
    E, nu, rho, c_a, c_T, T0, cu, cs, by = Mat
    #b = np.array([0, by]) # in our model no gravity is used

    # restructure input to fit our notation
    xI = np.array([[XL[0], XL[1]], [XL[2], XL[3]], [XL[4], XL[5]], [XL[6], XL[7]]])
    uI = np.array([[UL[0], UL[1]], [UL[3], UL[4]], [UL[6], UL[7]], [UL[9], UL[10]]])
    DTI = np.array([UL[2], UL[5], UL[8], UL[11]])

    # compute bulk modulus
    kappa = 0.0
    kappa = E / (3*(1-(2*nu)))


    # provide integration points
    aa = 1/np.sqrt(3)
    EGP = np.array([[-aa, -aa, 1],[aa, -aa, 1],[aa, aa, 1],[-aa, aa, 1]])
    NoInt = len(EGP)

    # start integration Loop
    for GP in range(NoInt):
        xi, eta, wgp  = EGP[GP]
        if verbose: print('GP: ',GP,' Xi_gp = [',xi,', ',eta,' ]')


        # evaluate shape functions at this gp
        SHP = 1/4 * np.array([(1.0-xi)*(1.0-eta), (1.0+xi)*(1.0-eta), (1.0+xi)*(1.0+eta), (1.0-xi)*(1.0+eta)])
        SHP_dxi = 1/4 * np.array([  [ -(1.0-eta),  -(1.0-xi)],
                                    [  (1.0-eta),  -(1.0+xi)],
                                    [  (1.0+eta),   (1.0+xi)],
                                    [ -(1.0+eta),   (1.0-xi)]
                                 ], dtype=np.float64)

        # compute Jacobian matrix
        J = np.zeros((2,2))
        for I in range(4):
            for i in range(2):
                for j in range(2):
                    J[i,j] += SHP_dxi[I,j] * xI[I,i]

        # compute Jacobi- determinant and inverse
        detJ = np.linalg.det(J)
        Jinv = np.linalg.inv(J)

        # compute gradient shape functions
        SHP_dx = np.zeros((4,2))
        for I in range(4):
            for i in range(2):
                for j in range(2):
                    SHP_dx[I, i] += Jinv[j,i] * SHP_dxi[I,j]

       # Creating theta_dot and grad_theta for Element vector of BaEn (temperature gradient)
        grad_theta = np.zeros(2)
        bI = np.zeros(2)
        bJ = np.zeros(2)
        
        for I in range(4):
            for i in range(2):
                bI[i] = SHP_dx[I, i] # derivative of shape function
            for i in range(2):
                grad_theta[i] += bI[i] * DTI[I]

        # compute strains
        eps = np.zeros(6)
        for I in range(4):
            # compute B-matrix for this node I
            BI = np.array([ [SHP_dx[I,0], 0           ],
                            [0          , SHP_dx[I,1] ],
                            [0          , 0           ],
                            [SHP_dx[I,1], SHP_dx[I,0] ],
                            [0          , 0           ],
                            [0          , 0           ]
                        ])
            for i in range(6):
                for j in range(2):
                    eps[i] += BI[i,j] * uI[I,j]

        # form constitutive tensor
        lam   = (E*nu)/((1.0+nu)*(1.0-2.0*nu))
        mue   = E/(2.0*(1.0+nu))

        Cmat = np.array([
                [lam + 2* mue, lam         , lam         , 0  , 0  , 0  ],
                [lam         , lam + 2* mue, lam         , 0  , 0  , 0  ],
                [lam         , lam         , lam + 2* mue, 0  , 0  , 0  ],
                [0           , 0           , 0           , mue, 0  , 0  ],
                [0           , 0           , 0           , 0  , mue, 0  ],
                [0           , 0           , 0           , 0  , 0  , mue]
                ], dtype=np.float64)
        
        # compute delT
        del_T = 0.0
        for I in range(4):
            del_T += SHP[I] * DTI[I]

        # Identity Matrix voigt notation 
        Iden = np.zeros(6)
        Iden[0] = 1
        Iden[1] = 1
        Iden[2] = 1
        Iden[3] = 0
        Iden[4] = 0
        Iden[5] = 0

        # compute stress
        sig = np.zeros(6)
        for i in range(6):
            sig[i] += - 3 * cs * kappa * cu * del_T * Iden[i] # sigma dependent on temperature
            for m in range(6):
                sig[i] += Cmat[i,m] * eps[m]   

        # compute element vector and matrix
        for I in range(4):
            # compute B-matrix for this node I
            BI = np.array([  [SHP_dx[I,0], 0           ],
                             [0          , SHP_dx[I,1] ],
                             [0          , 0           ],
                             [SHP_dx[I,1], SHP_dx[I,0] ],
                             [0          , 0           ],
                             [0          , 0           ]
                         ])
            for i in range(2):
                bI[i] = SHP_dx[I, i]

            # Computation of Element vector in case of BaMo
            for k in range(2):
                for i in range(6):
                    r_e[I*NoNodalDofs+k] += (sig[i] * BI[i,k]) * detJ * wgp

            # Computation of Element vector in case of BaEn
            # volumetric heat source 0
            for k in range(2):
                r_e[I*3+2] += (c_a * grad_theta[k] * bI[k]) * detJ * wgp
             
            for J in range(4):
                # select shape function at node J
                NJ = SHP[J]
                # compute B-matrix for this node J
                BJ = np.array([  [SHP_dx[J,0], 0           ],
                                 [0          , SHP_dx[J,1] ],
                                 [0          , 0           ],
                                 [SHP_dx[J,1], SHP_dx[J,0] ],
                                 [0          , 0           ],
                                 [0          , 0           ]
                             ])

            
                # BaMo terms
                for k in range(2):
                    for l in range(2):
                        for i in range(6):
                            for m in range(6):
                                k_e[I*NoNodalDofs+k, J*NoNodalDofs+l] += Cmat[i,m] * BJ[m,l] * BI[i,k] * detJ * wgp

                # BaEn terms
                for i in range(2):
                    bJ[i] = SHP_dx[J, i]
              
                for p in range(2):
                    k_e[I*3+2, J*3+2] += (c_a * bI[p] * bJ[p]) * detJ * wgp 

                for m in range(6):
                    k_e[I*3+0, J*3+2] += (-3 * cs * kappa * cu * NJ * Iden[m] * BI[m, 0]) * detJ * wgp
                    k_e[I*3+1, J*3+2] += (-3 * cs * kappa * cu * NJ * Iden[m] * BI[m, 1]) * detJ * wgp


    return r_e, k_e

def Elmt_Post(XL, UL, Hn, Ht, Mat, dt, PostName):
    '''
    The Elmt_Post(XL, UL, Hn, Ht, Mat, dt, PostName) function returns a vector,
    containing a scalar for each node.
    '''

    # initialize return - the post function always returns a vector
    # containing one scalar per node of the element
    r_post = np.zeros(4)

    # read in material parameter
    E, nu, rho, c_a, c_T, T0, cu, cs, by = Mat
    #b = np.array([0, by])

    # restructure input to fit our notation
    xI = np.array([[XL[0], XL[1]], [XL[2], XL[3]], [XL[4], XL[5]], [XL[6], XL[7]]])
    uI = np.array([[UL[0], UL[1]], [UL[3], UL[4]], [UL[6], UL[7]], [UL[9], UL[10]]])
    DTI = np.array([UL[2], UL[5], UL[8], UL[11]])
    
    # compute bulk modulus
    kappa = 0.0
    kappa = E / (3*(1-(2*nu)))

    # provide integration points
    aa = 1/np.sqrt(3)
    EGP = np.array([[-aa, -aa, 1],[aa, -aa, 1],[aa, aa, 1],[-aa, aa, 1]])
    NoInt = len(EGP)

    # start integration Loop
    for GP in range(NoInt):
        xi, eta, wgp  = EGP[GP]


        # evaluate shape functions at this gp
        SHP = 1/4 * np.array([(1.0-xi)*(1.0-eta), (1.0+xi)*(1.0-eta), (1.0+xi)*(1.0+eta), (1.0-xi)*(1.0+eta)])
        SHP_dxi = 1/4 * np.array([  [ -(1.0-eta),  -(1.0-xi)],
                                    [  (1.0-eta),  -(1.0+xi)],
                                    [  (1.0+eta),   (1.0+xi)],
                                    [ -(1.0+eta),   (1.0-xi)]
                                 ], dtype=np.float64)

        # compute Jacobian matrix
        J = np.zeros((2,2))
        for I in range(4):
            for i in range(2):
                for j in range(2):
                    J[i,j] += SHP_dxi[I,j] * xI[I,i]

        # compute jabobian inverse
        Jinv = np.linalg.inv(J)

        # compute gradient shape functions
        SHP_dx = np.zeros((NoNodes,2))
        for I in range(NoNodes):
            for i in range(2):
                for j in range(2):
                    SHP_dx[I, i] += Jinv[j,i] * SHP_dxi[I,j]

        # Creating theta_dot and grad_theta for Element vector of BaEn (temperature gradient)
        grad_theta = np.zeros(2)
        #theta_dot = 0.0
        bI = np.zeros(2)
        #bJ = np.zeros(2)

        for I in range(4):
            for i in range(2):
                bI[i] = SHP_dx[I, i] # derivative of shape function
            for i in range(2):
                grad_theta[i] += bI[i] * DTI[I]

        # compute gradient shape functions
        SHP_dx = np.zeros((4,2))
        for I in range(4):
            for i in range(2):
                for j in range(2):
                    SHP_dx[I, i] += Jinv[j,i] * SHP_dxi[I,j]

        # form B-matrices for each node
        B = [np.array([ [SHP_dx[I,0], 0           ],
                            [0          , SHP_dx[I,1] ],
                            [0          , 0           ],
                            [SHP_dx[I,1], SHP_dx[I,0] ],
                            [0          , 0           ],
                            [0          , 0           ]
                        ])
                        for I in range(4)]

        # compute strains
        eps = np.zeros(6)
        for I in range(4):
            for i in range(6):
                for j in range(2):
                    eps[i] += B[I][i,j] * uI[I,j]

        # form constitutive tensor
        lam   = (E*nu)/((1.0+nu)*(1.0-2.0*nu))
        mue   = E/(2.0*(1.0+nu))

        Cmat = np.array([
                [lam + 2* mue, lam         , lam         , 0  , 0  , 0  ],
                [lam         , lam + 2* mue, lam         , 0  , 0  , 0  ],
                [lam         , lam         , lam + 2* mue, 0  , 0  , 0  ],
                [0           , 0           , 0           , mue, 0  , 0  ],
                [0           , 0           , 0           , 0  , mue, 0  ],
                [0           , 0           , 0           , 0  , 0  , mue]
                ], dtype=np.float64)

        # compute delT
        del_T = 0.0
        for I in range(4):
            # select shape function at node I
            #NI = SHP[I] 
            del_T += SHP[I] * DTI[I]

        # identity
        # Identity Matrix voigt notation
        Iden = np.zeros(6)
        Iden[0] = 1
        Iden[1] = 1
        Iden[2] = 1
        Iden[3] = 0
        Iden[4] = 0
        Iden[5] = 0
        # compute stress
        sig = np.zeros(6)
        for i in range(6):
            sig[i] += - 3 * cs * cu * kappa * del_T * Iden[i]
            for m in range(6):
                sig[i] += Cmat[i,m] * eps[m]


        # compute vonMises stresses
        sig_vm = 0.0
        sig_vm = np.sqrt( \
            sig[0]**2 + sig[1]**2 + sig[2]**2 \
            -sig[0]*sig[1] -sig[0]*sig[2] -sig[1]*sig[2] \
            + 3* (sig[3]**2 + sig[4]**2 + sig[5]**2) \
            )

        if (PostName=="SigMises"):
            r_post += sig_vm * SHP
        
        #print(sig_vm) # to get the von misses values
        
    # based on the string PostName different output is returned
    if (PostName=="UX"):
        r_post = np.array([UL[0], UL[2], UL[4], UL[6]])
        return r_post
    elif (PostName=="UY"):
        r_post = np.array([UL[1], UL[3], UL[5], UL[7]])
        return r_post
    elif (PostName=="T"):
        r_post = np.array([T0+UL[2], T0+UL[5], T0+UL[8], T0+UL[11]])
        return r_post
    elif (PostName=="SigMises"):
        return r_post
    else:
        print("Warning: PostName "+PostName+" not defined!")
        return np.array([0.0, 0.0, 0.0, 0.0]), sig_vm, sig


## This is a sanity check for the element

# define dummy input
XL = np.array([0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0])
UL = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0])
Hn = np.zeros(4*3*3)
Ht = np.zeros(4*3*3)
Mat = [2210e9, 0.25, 7850, 45, 502, 293.15,16e-6, 1, 0]
dt = 1
# call the elemnt with this dummy input
re, ke = Elmt_KS(XL, UL, Hn, Ht, Mat, dt)
# check the resulting vector / matrix
print('r_e :')
print(re)
print('k_e :')
print(ke)


