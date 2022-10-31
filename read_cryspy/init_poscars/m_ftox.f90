! == General purpose formatted write module m_FtoX ==
! 
! ftox: general format. usage: write(6,ftox) foobar,foobar1,foobar2
! foobar can be integer, character, and something like
!   ftof(dfloat/complex,m) 1234.123456 format.
!                m digits below period. m is option (six when m is not given)
!   ftod(dfloat/complex,m) 0.123456d+08 format.
!   ftom(dfloat/complex)   truncate right-hand-side zeros. drealx can be real(8) arrays.
! stdo: file handle for standard output
! stdl: handle for log
!==============
! program test_ftox
!   use m_ftox
!   real(8):: w1,w2,aaa(5)
!   character(12):: fff
!   complex(8):: bb(2)
!   n=-3132922
!   w1=12245.807807807d0
!   w2=-243.901901901d0
!   aaa=[1.24,4.56,117.1234567,4566666.9,90808.]
!   bbb=[(1.24,4.56),(117.1234567,456.8)]
!   write(6,ftox)'nnn1',n,'aaa',ftof(w1),'bbb',ftof(w1,5),'bbb',ftod(w2,12)
!   write(6,ftox)'nnn2',ftof(aaa(1:3))
!   write(6,ftox)'nnn3',ftod(aaa,2),ftof(bb,3) !last digit of ftof is the length after decimal point.
! end program test_ftoX
!=========================
!We have
!>nnn1 -3132922 aaa 12245.807808 bbb 12245.80781 bbb -0.243901901901D+03
!>nnn2 1.240000 4.560000 117.123459
!>nnn3 0.12D+01 0.46D+01 0.12D+03 0.46D+07 0.91D+05
module m_FtoX
  public :: ftof,ftod,ftom, ftox
  character(11):: ftox='(*(g0,x))'
  private
  
  !ftom is removing right-end zeros below decimal point.
  
  interface ftof !123.456789 format
     module procedure ftof,ftofv,ftoc,ftocv
  endinterface ftof
  
  interface ftod !0.123456D+8 format
     module procedure ftod,ftodv,ftocd,ftocdv
  endinterface ftod
  
  interface ftom !zero of righthand-side are truncated (mainly for inputs)
     module procedure ftom,ftomv
  endinterface ftom

contains
  function ftodv(argv,ixx) result(farg)
    intent(in):: argv,ixx
    real(8):: argv(:)
    character(:),allocatable:: farg
    integer,optional:: ixx
    integer::ix,i
    character(1000):: mmm
    ix=6
    if(present(ixx)) ix=ixx
    write(mmm,"(*(g0,x))") (ftod(argv(i),ix),i=1,size(argv))
    mmm=adjustl(mmm)
    if(allocated(farg)) deallocate(farg)
    allocate(farg,source=mmm(1:len(trim(mmm))))
  end function ftodv

  function ftofv(argv,ixx) result(farg)
    intent(in):: argv,ixx
    real(8):: argv(:)
    character(:),allocatable:: farg
    integer,optional:: ixx
    character(1000):: mmm
    integer::ix,i
    ix=6
    if(present(ixx)) ix=ixx
    write(mmm,"(*(g0,x))") (ftof(argv(i),ix),i=1,size(argv))
    mmm=adjustl(mmm)
    if(allocated(farg)) deallocate(farg)
    allocate(farg,source=mmm(1:len(trim(mmm))))
  end function ftofv

  function ftocdv(argv,ixx) result(farg)
    intent(in):: argv,ixx
    complex(8):: argv(:)
    character(:),allocatable:: farg
    integer,optional:: ixx
    character(1000):: mmm
    integer:: i,ix
    ix=6
    if(present(ixx)) ix=ixx
    write(mmm,"(*(g0,x))") (ftocd(argv(i),ix),i=1,size(argv))
    mmm=adjustl(mmm)
    if(allocated(farg)) deallocate(farg)
    allocate(farg,source=mmm(1:len(trim(mmm))))
  end function ftocdv

  function ftocv(argv,ixx) result(farg)
    intent(in):: argv,ixx
    complex(8):: argv(:)
    character(:),allocatable:: farg
    integer,optional:: ixx
    character(1000):: mmm
    integer:: i,ix
    ix=6
    if(present(ixx)) ix=ixx
    write(mmm,"(*(g0,x))") (ftoc(argv(i),ix),i=1,size(argv))
    mmm=adjustl(mmm)
    if(allocated(farg)) deallocate(farg)
    allocate(farg,source=mmm(1:len(trim(mmm))))
  end function ftocv

  function ftomv(argv,ixx) result(farg)
    intent(in):: argv,ixx
    integer:: i,ix
    real(8):: argv(:)
    character(:),allocatable:: farg
    integer,optional:: ixx
    character(1000):: mmm
    ix=6
    if(present(ixx)) ix=ixx
!    print *,'ftomv',size(argv)
    write(mmm,"(*(g0,x))") (ftom(argv(i)),i=1,size(argv))
    mmm=adjustl(mmm)
    if(allocated(farg)) deallocate(farg)
    allocate(farg,source=mmm(1:len(trim(mmm))))
  end function ftomv
  
!ccccccccccccccccccccccccccccccccccccccccccccccccccc
  function ftof(arg,ixx) result(farg)
    intent(in)::arg,ixx
    real(8):: arg
    integer,optional:: ixx
    character(:),allocatable:: farg
    integer::ix
    ix=6
    if(present(ixx)) ix=ixx
    farg = fwww("("//"f32."//charnum3(ix)//")",arg)
  end function ftof
  !
  function ftod(arg,ixx) result(farg)
    intent(in)::arg,ixx
    real(8):: arg
    integer,optional:: ixx
    character(:),allocatable:: farg
    integer::ix
    ix=6
    if(present(ixx)) ix=ixx
    farg = fwww("("//"d32."//charnum3(ix)//")",arg)
  end function ftod
  !  
  function ftoc(arg,ixx) result(farg)
    intent(in)::arg,ixx
    complex(8):: arg
    integer,optional:: ixx
    character(:),allocatable:: farg
    integer::ix
    ix=6
    if(present(ixx)) ix=ixx
    farg="( "//ftof(dreal(arg),ix)//" , "//ftof(dimag(arg),ix)//" )"
  end function ftoc
  !  
  function ftocd(arg,ixx) result(farg)
    intent(in)::arg,ixx
    complex(8):: arg
    integer,optional:: ixx
    character(:),allocatable:: farg
    integer::ix
    ix=6
    if(present(ixx)) ix=ixx
    farg="( "//ftod(dreal(arg),ix)//" , "//ftod(dimag(arg),ix)//" )"
  end function ftocd
  !  
  function fwww(fmt,arg) result(farg)
    intent(in)::fmt,arg
    real(8):: arg
    character(32):: mmm
    character(*):: fmt
    character(:),allocatable:: farg
    write(mmm,fmt) arg
    mmm=adjustl(mmm)
    if(allocated(farg)) deallocate(farg)
    if(arg>=0)  allocate(farg,source=' '//mmm(1:len(trim(mmm))))
    if(arg<0 )  allocate(farg,source=mmm(1:len(trim(mmm))))
  end function fwww
  !  
  function ftom(arg,ixx) result(farg) !arg =3.45600000 is '3.45', trucates to rightside zeros'
    intent(in)::arg,ixx
    real(8):: arg
    character(:),allocatable:: farg
    character(32):: mmm,fmt
    integer,optional:: ixx
    integer:: i,j
    write(mmm,"(*(g0,x))")ftof(arg,16)
!    print *,'vvvxxx=',trim(mmm)
    j=len(trim(mmm))
    do i=len(mmm),1,-1
       if(mmm(i:i)==' ') cycle
       if(mmm(i:i)=='.') then
          j=i-1
          exit
       elseif(mmm(i:i)/='0') then
          j=i
          exit
       endif
    enddo
    if(allocated(farg)) deallocate(farg)
    allocate(farg,source=mmm(1:j))
  end function ftom
 
  character(3) function charnum3(num)
    integer(4) ::num
    charnum3=char(48+mod(num/100,10))//char(48+mod(num/10,10))//char(48+mod(num,10))
  end function charnum3
end module m_FtoX



! program test_ftox
!    use m_ftox
!    real(8):: w1,w2,aaa(5)
!    complex(8):: bbb(5)
!    character(12):: fff
!    n=-3132
!    w1=12245.807807807d0
!    w2=-243.901901901d0
!    aaa=[1.24d0,4.56d0,117.12d0,4566.3d0,1.92d0]
!    bbb=[1.24,4.56,117.123,4566.4,1.92]
!    write(6,ftox)'nnn1',n,'aaa',ftof(w1),'bbb',ftof(w1,5),'bbb',ftod(w2,12)
!    write(6,ftox)'nnn2',ftof(aaa)
!    write(6,ftox)'nnn2x',ftof(bbb,3)
!    write(6,ftox)'nnn3',ftod(aaa,2)
! !   write(6,ftox)'nnn3mmm',ftom(aaa(1:3))
! end program test_ftoX
!nnn1 -3132 aaa  12245.807808 bbb  12245.80781 bbb -0.243901901901D+03
!nnn2 1.240000  4.560000  117.120000  4566.300000  1.920000
!nnn2x (  1.240 ,  0.000 ) (  4.560 ,  0.000 ) (  117.123 ,  0.000 ) (  4566.400 ,  0.000 ) (  1.920 ,1  0.000 )
!nnn3 0.12D+01  0.46D+01  0.12D+03  0.46D+04  0.19D+01
