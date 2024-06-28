! defining 'eulerLib' module
module eulerLib

    use newtonLib               ! use module newtonLib
    type::EulerParams           ! creating Euler parameters

        ! declaration of variables
        real(8) :: t0 =  0.1d0
        real(8) :: y0 = -0.01d0

        real(8) :: h  =  0.1d0

        real(8) :: tStart   = 0.d0
        real(8) :: tEnd     = 6.d0

        real(8) :: y
        real(8) :: t

        logical :: logOnScreen = .true.
        logical :: outOnScreen = .true.

    end type

    contains

    ! function to read input file
    integer function readInput(filename,ep,np)
         implicit none

         ! declaration of variables
         character(*)      :: filename  !input file name

         type(NewtonParams):: np        ! initialization of newton Parameters
         type(EulerParams) :: ep        ! initialization of Euler Parameters

         ! local helpers
         integer           :: ioerr     !return code of error handler
         integer           :: ind       ! position of space
         character(256)    :: line      ! line buffer
         character(256)    :: key       ! data key
         integer           :: nErrors = 0
         integer           :: lineNr  = 0
         real(8)           :: temp

         ! opening the input file
         open(np%inpChan,file=filename,status='old',iostat=ioerr)

         if(ioerr/= 0) then
            readInput = -1
            return
         end if

         ! input loop, loop over lines in input file
         do
            read(np%inpChan, '(a)',iostat=ioerr) line   ! read into 'line' variable
            if (ioerr /= 0) then
                exit                                    ! exit if End Of File(EOF)......
            end if                                      ! .....is reached
            line = trim(line)                           ! delete trailing blanks
            if(len_trim(line)<1) cycle                  ! line empty --goto next cycle/ line!
            if(line(1:1) == '#') cycle                  ! comment line -- goto next cycle/line!
            ind = scan(line," ")                        ! search for the first space
            key= line(1:ind-1)

            ! Euler Parameter
            if (key=="t0") then                         ! store value into p%x0
                read(line(ind:),*,iostat=ioerr) ep%t0   ! "read" into p%t0
            else if (key=="y0") then                    ! store value into p%y0
                read(line(ind:),*,iostat=ioerr) ep%y0   ! "read" into p%y0
            else if (key=="h") then                     ! store value into p%x0
                read(line(ind:),*,iostat=ioerr) ep%h    ! "read" into p%x0
            else if (key=="tStart") then                ! store value into p%x0
                read(line(ind:),*,iostat=ioerr) ep%tStart   ! "read" into p%x0
            else if (key=="tEnd") then                  ! store value into p%x0
                read(line(ind:),*,iostat=ioerr) ep%tEnd ! "read" into p%x0
                ! if tStart and tEnd values entered are in wrong order
                if (ep%tEnd .lt. ep%tStart) then
                    temp        = ep%tEnd
                    ep%tEnd     = ep%tStart
                    ep%tStart   = temp
                end if
            else if (key=="logOnScreen") then                   ! store value into p%x0
                read(line(ind:),*,iostat=ioerr) ep%logOnScreen  ! "read" into p%x0
            else if (key=="outOnScreen") then                   ! store value into p%x0
                read(line(ind:),*,iostat=ioerr) ep%outOnScreen  ! "read" into p%x0

            ! read Newton parameters
            else if(key=="tol")then
                read(line(ind:),*,iostat=ioerr) np%tol          ! "read" into p%tol
            else if(key=="maxIt")then
                read(line(ind:),*,iostat=ioerr) np%maxIt        ! "read" into p%maxIt
            else if(key=="newtOnScreen")then
                read(line(ind:),*,iostat=ioerr) np%newtOnScreen ! "read" into p%maxIt
            else if(key=="newtInOut")then
                read(line(ind:),*,iostat=ioerr) np%newtInOut    ! "read" into p%maxIt
            else
                write(*,'(3a)') "*** warning: key' ",trim(key), "' not supported! "
            end if

            if (ioerr /= 0)then
                write(*,'(a,i3)') "Input file: format error in line ", lineNr
                write(*,*) "Input error in Key: ",key
                nErrors=nErrors+1
            end if

         end do

         close(np%inpChan)

         readInput = nErrors

     end function

    ! function to calculate forward Euler
    subroutine forEuler(f,ep,np)
        implicit none

        ! declaring variables and initiating Newton and Euler parameters as per above
        type(EulerParams)   :: ep
        type(NewtonParams)  :: np
        real(8),external    :: f
        real(8)             :: t0
        real(8)             :: y0,y

        character*128       :: argument
        character*128       :: pform

        t0= ep%t0
        y0= ep%y0

        ! Output block
        argument = "**** Forward Euler Method ****"
        call output(ep%outOnScreen, np%outChan,trim(argument))
        argument = "---t(i)|-------y(t)"
        call output(ep%outOnScreen, np%outChan,trim(argument))

        do
            ! Output block
            pform = "(1x,f8.2,1x,f8.4)"
            write(argument,pform) t0,y0
            call output(ep%outOnScreen, np%outChan,trim(argument))

            !calculate the new y
            y  = y0 + (ep%h*f(y0,t0))

            ! for the next iteration
            y0 = y
            t0 = t0 + ep%h

            ! loop exit condition
            if (ep%tEnd .lt. t0 ) then
                exit
            end if
        end do
    end subroutine

    ! backward Euler
    logical function backEuler(fPrime,ep,np)
        implicit none

        ! declaring variables and initiating Newton and Euler parameters as per above
        real(8),external    :: fPrime

        type(EulerParams)   :: ep
        type(NewtonParams)  :: np

        character*128       :: pform
        character*128       :: argument

        ! helping variables
        real(8)             :: t0,t1
        real(8)             :: y0,y1
        real(8)             :: h

        y0 = ep%y0
        t0 = ep%t0
        h  = ep%h

        ! Output block
        argument = "**** Backward Euler Method ****"
        call output(ep%outOnScreen, np%outChan,trim(argument))
        argument = "---t(i)|-------y(t)"
        call output(ep%outOnScreen, np%outChan,trim(argument))
        pform = "(1x,f8.2,1x,f8.4)"
        write(argument,pform) t0,y0
        call output(ep%outOnScreen, np%outChan,trim(argument))

        !update the first time step
        t1 = t0 + ep%h

        do
            !loop exit statement
            if (ep%tEnd .le. t1 ) then
                exit
            end if

            ! calculate y1 with newton()
            y1 = newton(fPrime,np,t1,y0,h)

            ! if newton fails
            if (y1 .eq. np%falsevalue) then
                write(argument,*) "*** Newton has failed"
                call output(ep%outOnScreen, np%outChan,trim(argument))
                backEuler = .false.
                return
            end if

            ! Output block
            pform = "(1x,f8.2,1x,f8.4)"
            write(argument,pform) t1,y1
            call output(ep%outOnScreen, np%outChan,argument)

            ! new assignment
            y0 = y1
            t1 = t1 + ep%h
        end do

        ! set return value
        backEuler = .true.
        return
    end function
end module
