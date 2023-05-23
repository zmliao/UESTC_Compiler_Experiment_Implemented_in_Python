begin
  integer k;
  integer function F(n);
    begin
      integer n;
      if n<=0 then F:=1
      else F:=n*F(n-1)
    end;
  read(m114514114514114514);
  k:=F(m1145141145141141514);
  write(k)
end