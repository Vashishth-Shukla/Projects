import numpy as np

# The 2D quadrilateral dynamic element for Coupled Problems WS21/22
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
#                   cs   -> multiplicator on the nonlinear coupling term (0 -> off, 1-> on)????
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
            UL  = [u11, u12, u21, u22, ..., un2]    -> np.vector of current nodal dofs for n-Nodes and 3 dofs at each
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
    r_e = np.zeros(NoNodes*NoNodalDofs) # Four-noded elements and 3 dofs
    k_e = np.zeros((NoNodes*NoNodalDofs, NoNodes*NoNodalDofs)) 

    # read in material parameter
    E, nu, rho, c_a, c_T, T0, cu, cs, by = Mat
    b = np.array([0, by])

    # restructure input to fit our notation
    xI = np.array([[XL[0], XL[1]], [XL[2], XL[3]], [XL[4], XL[5]], [XL[6], XL[7]]])
    uI = np.array([[UL[0], UL[1]], [UL[3], UL[4]], [UL[6], UL[7]], [UL[9], UL[10]]])
    DTI = np.array([UL[2], UL[5], UL[8], UL[11]])

    # read histroy - Newmark time integration
    aIn    = np.array([[Hn[0],  Hn[1] ], [Hn[2] , Hn[3] ], [Hn[4] , Hn[5] ], [Hn[6] , Hn[7]] ])
    vIn    = np.array([[Hn[8],  Hn[9] ], [Hn[10], Hn[11]], [Hn[12], Hn[13]], [Hn[14], Hn[15]]])
    uIn    = np.array([[Hn[16], Hn[17]], [Hn[18], Hn[19]], [Hn[20], Hn[21]], [Hn[22], Hn[23]]])
    ddDTIn = np.array([Hn[24+0], Hn[24+1], Hn[24+2 ], Hn[24+3 ]])
    dDTIn  = np.array([Hn[24+4], Hn[24+5], Hn[24+6 ], Hn[24+7 ]])
    DTIn   = np.array([Hn[24+8], Hn[24+9], Hn[24+10], Hn[24+11]])

    # compute bulk modulus
    kappa = 0.0
    kappa = E / (3*(1-(2*nu)))

    # compute current acceleration and velocity - Newmark time integration
    gamma = 1.0/2.0
    beta  = 1.0/4.0
    aI    = np.zeros((4,2))
    vI    = np.zeros((4,2))
    ddDTI = np.zeros(4) # second derivative of delta T
    dDTI  = np.zeros(4) # first derivative of delta T
    
    # Newmark Integration
    for I in range(4):
        ddDTI[I] = (1 / (beta * dt ** 2)) * (DTI[I] - DTIn[I] - dt * dDTIn[I] - dt ** 2 * (0.5 - beta) * ddDTIn[I])
        dDTI[I] = (gamma / (beta * dt)) * (DTI[I] - DTIn[I]) + (1.0 - (gamma / beta)) * dDTIn[I] + dt * (1 - (gamma / (2.0 * beta))) * ddDTIn[I]

    for I in range(4):
        for k in range(2):
            aI[I, k] = (1 / (beta * dt ** 2)) * (
                        uI[I, k] - uIn[I, k] - dt * vIn[I, k] - dt ** 2 * (0.5 - beta) * aIn[I, k])
            vI[I, k] = (gamma / (beta * dt)) * (uI[I, k] - uIn[I, k]) + (1.0 - (gamma / beta)) * vIn[I, k] + dt * (
                        1 - (gamma / (2.0 * beta))) * aIn[I, k]

    # write history - Newmark time integration
    [[Ht[0],  Ht[1] ], [Ht[2] , Ht[3] ], [Ht[4] , Ht[5] ], [Ht[6] , Ht[7]] ] = aI
    [[Ht[8],  Ht[9] ], [Ht[10], Ht[11]], [Ht[12], Ht[13]], [Ht[14], Ht[15]]] = vI
    [[Ht[16], Ht[17]], [Ht[18], Ht[19]], [Ht[20], Ht[21]], [Ht[22], Ht[23]]] = uI
    [Ht[24+0], Hn[24+1], Ht[24+2 ], Ht[24+3 ]] = ddDTI
    [Ht[24+4], Hn[24+5], Ht[24+6 ], Ht[24+7 ]] = dDTI
    [Ht[24+8], Ht[24+9], Ht[24+10], Ht[24+11]] = DTI

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

        # Creating acceleration vector
        a = np.zeros(2)
        for k in range(2):
            for m in range(4):
               a[k] += SHP[m] * aI[m, k]

       # Creating theta_dot and grad_theta for Element vector of BaEn (temperature gradient)
        grad_theta = np.zeros(2)
        theta_dot = 0.0
        bI = np.zeros(2)
        bJ = np.zeros(2)

        for I in range(4):
           theta_dot += SHP[I] * dDTI[I] # interpolated derivative of theta
        for I in range(4):
            for i in range(2):
                bI[i] = SHP_dx[I, i] # derivative of shape function
            for i in range(2):
                grad_theta[i] += bI[i] * DTI[I] # equation in theory

        # compute strains
        eps = np.zeros(6)
        eps_dot = np.zeros(6)
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
                    eps_dot[i] += BI[i,j] * vI[I,j]

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
            NI = SHP[I]
            del_T += SHP[I] * DTI[I] # in theory

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
            sig[i] += - 3 * cs * kappa * cu * del_T * Iden[i] # in theory
            for m in range(6):
                sig[i] += Cmat[i,m] * eps[m] #+ Dmat[i,m] * eps_dot[m]

        # compute element vector and matrix
        for I in range(4):
            # select shape function at node I
            NI = SHP[I]
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
                r_e[I*NoNodalDofs+k] += (rho * (a[k] - b[k]) * NI) * detJ * wgp # a vector and b vector are vectors that have 2 values inside
                for i in range(6):
                    r_e[I*NoNodalDofs+k] += (sig[i] * BI[i,k]) * detJ * wgp # sig calculated on top this term is also a coupling term

            # Computation of Element vector in case of BaEn
            # volumetric heat source 0
            r_e[I*3+2] += ((rho * c_T * theta_dot * NI)) * detJ * wgp # Time dependent part of heat conductivity
            for k in range(2):
                r_e[I*3+2] += (c_a * grad_theta[k] * bI[k]) * detJ * wgp # heat expansion

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

                # Kronecker delta
                krond = np.identity(2)
                # BaMo terms
                for k in range(2):
                    for l in range(2):
                        k_e[I*NoNodalDofs+k, J*NoNodalDofs+l] += ((rho/(beta * dt**2)) * NJ * NI * krond[k,l]) * detJ * wgp
                        for i in range(6):
                            for m in range(6):
                                k_e[I*NoNodalDofs+k, J*NoNodalDofs+l] += Cmat[i,m] * BJ[m,l] * BI[i,k] * detJ * wgp
                               
                # BaEn terms
                for i in range(2):
                    bJ[i] = SHP_dx[J, i]
              
                k_e[I*3+2, J*3+2] += rho * c_T * NJ * (gamma / (beta * dt)) * NI * detJ * wgp 
                
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

    # compute current acceleration and velocity - Newmark time integration
    aI    = np.zeros((4,2))
    vI    = np.zeros((4,2))
    ddDTI = np.zeros(4)
    dDTI  = np.zeros(4)

    # write histroy - Newmark time integration
    [[Ht[0],  Ht[1] ], [Ht[2] , Ht[3] ], [Ht[4] , Ht[5] ], [Ht[6] , Ht[7]] ] = aI
    [[Ht[8],  Ht[9] ], [Ht[10], Ht[11]], [Ht[12], Ht[13]], [Ht[14], Ht[15]]] = vI
    [[Ht[16], Ht[17]], [Ht[18], Ht[19]], [Ht[20], Ht[21]], [Ht[22], Ht[23]]] = uI
    [Ht[24+0], Hn[24+1], Ht[24+2 ], Ht[24+3 ]] = ddDTI
    [Ht[24+4], Hn[24+5], Ht[24+6 ], Ht[24+7 ]] = dDTI
    [Ht[24+8], Ht[24+9], Ht[24+10], Ht[24+11]] = DTI

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

        # compute Jacobi inverse
        Jinv = np.linalg.inv(J)

        # compute gradient shape functions
        SHP_dx = np.zeros((NoNodes,2))
        for I in range(NoNodes):
            for i in range(2):
                for j in range(2):
                    SHP_dx[I, i] += Jinv[j,i] * SHP_dxi[I,j]

        # compute acceleration vector
        a = np.zeros(2)
        for j in range(2):
                for e in range(4):
                    a[j] +=  SHP[e]  * aI[e,j]

        # Creating theta_dot and grad_theta for Element vector of BaEn (temperature gradient)
        grad_theta = np.zeros(2)
        theta_dot = 0.0
        bI = np.zeros(2)

        for I in range(4):
           theta_dot += SHP[I] * dDTI[I]
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
PostName = 'Justaname'
#call the elemnt with this dummy input
re, ke = Elmt_KS(XL, UL, Hn, Ht, Mat, dt)
#check the resulting vector / matrix
print('r_e :')
print(re)
print('k_e :')
print(ke)