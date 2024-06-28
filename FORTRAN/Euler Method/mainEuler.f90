!##############################################################################################
! This program calculates the Backward and Forward Euler methods for the given fPrime function
!
! -- Author(s):
!           Bhargav Sanchania   (3106382)
!           Vashishth Shukla    (3098673)
!
!##############################################################################################

! Target function in the form of y and t

real(8) function fPrime(y,t)
    real(8):: y,t
    fPrime =  y**2 + 1 - t**2
end function

! Main function starts

program mainEuler

    use eulerLib        ! use module eulerLib
    use newtonLib       ! use module newtonLib

    ! in order to avoid the external variable we say
    implicit none

    ! variable declaration
    real(8), external   :: fPrime               ! (external) to connect to the objective function
    type(NewtonParams)  :: np                   ! initialization of newton Parameters
    type(EulerParams)   :: ep                   ! initialization of Euler Parameters

    logical             :: bEuler = .false.     ! helping variable for calling the function

    integer             :: nCode                !return code of input reader call
    character(128)      :: argument


    ! starting statement on the console
    write(*,*) "opening the log and output files!"

    ! now opening the output file and log file
    open(np%outChan,file=np%outFile,status='replace') ! iostat=ioerr not checking the io status... because replace
    open(np%logChan,file=np%logFile,status='replace') ! iostat=ioerr not checking the io status... because replace

    !'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ! NOTE for Log / Output block:
    ! Log / Output block for the Log (the block below is one model for the output and the Log file
    ! the write statement will add the target string in the variable
    ! the call function will print the string in the Log/ Output file
    ! the 'logOnScreen' and the 'outOnScreen' will help decide to get the output on console or not!
    !'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    ! Log block
    write(argument, *) "reading input file!"
    call output(ep%logOnScreen,np%logChan,argument)

    ! read input file with the function
    nCode = readInput(np%inpFile,ep,np)

    if (ncode>0) then
        write(argument, *) "*** ERROR: program stopped with",nCode,"Errors!"
        call output(ep%logOnScreen,np%logChan,argument)
        stop
    elseif (nCode<0) then
        write(argument, *) "*** ERROR: input file not found"
        call output(ep%logOnScreen,np%logChan,argument)
        stop
    end if

    ! Log block
    write(argument, *) "input file reading completed!"
    call output(ep%logOnScreen,np%logChan,argument)
    write(argument, *) "running forward Euler Method"
    call output(ep%logOnScreen,np%logChan,argument)

    ! for forward Euler Method
    call forEuler(fPrime,ep,np)

    ! Log/Output block
     write(*,*) "+++++ forward Euler was Completed. +++++"
     write(argument, *) "+++++ forward Euler was completed. +++++"
     call output(.false.,np%logChan,argument)


    ! Log block
    write(argument, *) "running backward Euler Method"
    call output(ep%logOnScreen,np%logChan,argument)

    ! function for the backward Euler Method
    bEuler = backEuler(fPrime,ep,np)

    if (bEuler) then
        write(*,*) "+++++ Backward Euler was successful. +++++"
    else
        write(*,*) "+++++ Backward Euler was unsuccessful. +++++"
    end if

    ! output the the output file as well as screen
    write(argument, *) "closing the output and log files."
    call output(ep%logOnScreen,np%logChan,argument)

    ! closing the output and the log files.
    close(np%outChan)
    close(np%logChan)

end program
