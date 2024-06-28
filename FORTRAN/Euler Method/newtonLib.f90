! defining 'newtonLib' module
module newtonLib

    type:: NewtonParams                         ! creating the newton parameters
        real(8)       :: yn0                    ! starting value
        real(8)       :: yn                     ! current/solution value
        real(8)       :: ynew                   ! new value of x
        real(8)       :: hn           = 1.0d-6
        real(8)       :: tol          = 1.0d-8
        real(8)       :: fy
        real(8)       :: fprimey
        real(8)       :: cycles       = 0       ! required no of cycles
        real(8)       :: tols         = 1.0d-5  ! if slope is almost zero
        real(8)       :: step         = 0.1
        integer       :: maxIt        = 12

        real(8)             :: falsevalue = 1e10 ! if newton fails return this value

        ! input and output channels
        integer       :: inpChan      = 1231
        integer       :: outChan      = 1232
        integer       :: logChan      = 1233

        logical       :: newtOnScreen = .true.
        logical       :: newtInOut    = .false.

        ! setting default input, output and log file names
        character(128):: inpFile      = "input.txt"
        character(128):: outFile      = "output.txt"
        character(128):: logFile      = "log.txt"
    end type

    contains

    ! this subroutine will print the lines in the given channels and if toggle is true will print on console
    subroutine output(toggal, channel, argument)
        implicit none
        integer         :: channel
        logical         :: toggal
        character(*)    :: argument

        write(channel,*) trim(argument)

        if (toggal) then
           write(*,*) trim(argument)
        end if
    end subroutine

    ! the function we want to solve with the newton method
    ! this function if based on the fPrime function -> the target function for Euler methods
    real(8) function yPrime(fPrime,t1,y0,y1,h)

        implicit none

        real(8),external    :: fPrime   ! (external)fPrime to connect to the objective function
        real(8)             :: t1
        real(8)             :: y0
        real(8)             :: y1
        real(8)             :: h

        yPrime = y0 + h*fPrime(y1,t1) - y1
    end function

    ! this function finds the derivative of any given function
    real(8) function fdot(f,tEuler1,yEuler0,yNewton,hNewton,hEuler)
        implicit none
        real(8),external   :: f !reference to obj. function
        real(8)            :: tEuler1
        real(8)            :: yEuler0
        real(8)            :: yNewton
        real(8)            :: hNewton
        real(8)            :: hEuler
        real(8)            :: fy1,fy2


        fy2 = yPrime(f,tEuler1,yEuler0,(yNewton+(hNewton/2.d0)),hEuler)
        fy1 = yPrime(f,tEuler1,yEuler0,(yNewton-(hNewton/2.d0)),hEuler)

        fdot = (fy2-fy1)/hNewton
    end function
    ! this function will find the solution for each Euler Timestep( y1 for each t1)
    real(8) function newton(f,np,t1,y0,h)
        implicit none
        real(8),external    :: f !reference to obj. function
        real(8)             :: y0
        real(8)             :: t1
        real(8)             :: h
        type(NewtonParams)  :: np !parameter container ('type') p

        ! local variables
        integer             :: i = 0
        real(8)             :: yNewton
        real(8)             :: hNewton

        real(8)             :: hEuler
        real(8)             :: yEuler0
        real(8)             :: tEuler1
        real(8)             :: fy
        real(8)             :: fdoty

        character(128)      :: argument
        character(128)      :: pform

        ! to make the program readable
        yNewton = y0           ! first assumption   we take y0 as first assumption as we believer that the new y will be closer to the old y and the function will be smooth
        hNewton = np%hn

        hEuler  = h
        yEuler0 = y0
        tEuler1 = t1

        ! first assumption
        newton  = y0

        ! Output block and Log block
        write(argument,'(2(a,f12.5))') "for y0 :" , y0, "and t1: " ,t1
        call output(np%newtOnScreen, np%logChan,argument)

        write(argument,*) "--i ---------y -------f(y) -------f'(y)"
        call output(np%newtOnScreen, np%logChan,argument)
        if (np%newtInOut) then
            call output(.false., np%outChan,argument)
        end if

        ! run newton iterations till maxIt is reached
        do i=1,np%maxIt
            fy    = yPrime(f,tEuler1,yEuler0,yNewton,hEuler)           ! this finds the value of the function we want to make 0
            fdoty = fdot(f,tEuler1,yEuler0,yNewton,hNewton,hEuler)

            ! if slop is zero we need to step aside
            if (dabs(fdoty).lt.np%tols) then
               yNewton = yNewton + np%step
               write(*,*) "step aside done",fdoty
               cycle
            end if

            ! calculate the new y
            yNewton = yNewton - fy/fdoty

            ! Log block
            pform = "(i4,1x,3(1x,f12.5))"
            write(argument,pform) i, yNewton , fy, fdoty
            call output(np%newtOnScreen, np%logChan,trim(argument))
            if (np%newtInOut) then
                call output(.false., np%outChan,trim(argument))
            end if

            ! if f(y) = 0 stop the newton iterations
            if (dabs(fy).lt.(np%tol)) then
               newton = yNewton
               return
            end if
        end do
    ! if maxIt reached and no solution found we return the last y value.
    newton = np%falsevalue
    return
    end function
end module
