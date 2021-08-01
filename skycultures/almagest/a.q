/ loader for Ernie Wright's catalogue data
a:{r:1_read0 x;t:"I S I I I CI I F I * ";
   / bn con  ic  xd  xm ys yd  ym  m   hr  d
   w:4 1 3 1 2 1 3 1 2 1 1 2 1 2 1 3 1 4 1 12 1;
   flip`bn`con`ic`xd`xm`ys`yd`ym`m`hr`id`d!
          ((t;w)0:n#/:r),enlist(n:sum w)_/:r}
/ loader for ... catalogue data
/               4 3 2 2 2 2  2 2
b:{r:read0 x;t:"I SCICI ICI CICIC* ";
   w:4 1 3 1 2 1 3 1 2 1 2 1 1 2 1 2 1 3 1;
   flip`bn`con`inf`ic`w`z`zd`xm`wz`ys`yd`wy`ym`wm`m`d!
          ((t;w)0:n#/:r),enlist(n:sum w)_/:r}
/ loader for cross-reference files
x:{t:"I SCICSCS I SCI I I I IC";
   w:4 1 3 1 2 1 3 1 3 1 1 1 3 1 3 1 2 1 3 1 4 1 4 1;
   flip`bn`con`inf`ic`noi`bc`wb`bl`bi`fc`wf`fi`zr`zn`ln`hr`wh!
        (t;w)0:(sum w)$/:read0 x}
/ compute coordinates
M:1%60e
c:{select bn,con,ic,x:xd+xm*M,y:(1-2*ys="-")*yd+ym*M,m,d from x}
/ adjust for zodiac
z:{update xd:zd+30*z from x}
a1:c A1:a`:almstars/cat1.dat  / Toomer/Grasshoff
a2:c A2:a`:almstars/cat2.dat  / Peters/Knobel
a3:c A3:a`:almstars/cat3.dat  / Manitius
a4:c A4:a`:almstars/catpick.dat  / Pickering
/ -
b1:c z B1:b`$":ptolemy/ptolemy_t.dat"  / Toomer
b2:c z B2:b`$":ptolemy/ptolemy_p.dat"  / Peters & Knobel
b3:c z B3:b`$":ptolemy/ptolemy_m.dat"  / Manitius
b4:c z B4:b`$":ptolemy/ptolemy_b.dat"  / Baily
b5:c z B5:b`$":ptolemy/ptolemy_h.dat"  / Halma
b6:c z B6:b`$":ptolemy/ptolemy_z.dat"  / Flamsteed

C1:x`$":ptolemy/cross_t.dat"  / Toomer
C2:x`$":ptolemy/cross_p.dat"  / Peters & Knobel
C3:x`$":ptolemy/cross_m.dat"  / Manitius
C4:x`$":ptolemy/cross_b.dat"  / Baily
C5:x`$":ptolemy/cross_f.dat"  / Halma
C6:x`$":ptolemy/cross_z.dat"  / Flamsteed

\c 40 200
/ diffs
if[count d:where not all each (=)over{select bn,con,ic from x} each (a1;a2);
   show a1 d; 
   show a2 d;]
show `dx xdesc update dx:abs x-x2 from (a1,'select x2:x from a2) where x<>x2; 