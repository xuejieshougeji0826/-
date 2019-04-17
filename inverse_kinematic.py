import math
import numpy as np
L0=7.5;
L2=8.8;
L3=7.3;
L4=16.5;
x=22;
y=3;
z=1;
genhao=1/(math.sqrt(2));
#th1=acosd(x/(sqrt(x*x+y*y)));
th1=math.acos(x/math.sqrt(x*x+y*y))
k1=z+(genhao)*L4-L0;
k2=math.sqrt(x*x+y*y)-genhao*L4;
th3=math.acos((k1*k1+k2*k2-L2*L2-L3*L3)/(2*L2*L3));

k3=L3*(math.cos(th3)-math.sin(th3))+L2;
k4=L3*(math.cos(th3)+math.sin(th3))+L2;

th2=math.pi-math.asin((k1+k2)/math.sqrt(k3*k3+k4*k4))-math.atan(k4/k3);
if th2>=(math.pi*0.5):
    th2=th2-math.pi
th5=45*math.pi/180;
th4=math.pi-th5-th2-th3;

cos4=(math.cos(th4));sin4=(math.sin(th4));
cos3 = (math.cos(th3));sin3 = (math.sin(th3));
cos2 = (math.cos(math.pi*0.5-th2));sin2 = (math.sin(math.pi*0.5-th2));
cos1 = (math.cos(th1));sin1 = (math.sin(th1));
print(math.cos(th2))
print(cos1,cos2,cos3,cos4)
t01=np.array([[cos1,-(sin1),0,0],[sin1,cos1,0,0],[0,0,1,L0],[0,0,0,1]])
t12=np.array([[cos2,-(sin2),0,0],[0,0,1,0],[sin2,cos2,0,0],[0,0,0,1]])
t23=np.array([[cos3,-(sin3),0,L2],[-sin3,-cos3,0,0],[0,0,1,0],[0,0,0,1]])
t34=np.array([[cos4,-(sin4),0,L3],[sin4,cos4,0,0],[0,0,-1,0],[0,0,0,1]])
t45=np.array([[1,0,0,L4],[0,1,0,0],[0,0,1,0],[0,0,0,1]]);
t02=np.dot(t01,t12);t03=np.dot(t02,t23);t04=np.dot(t03,t34);t05=np.dot(t04,t45);
th1=math.degrees(th1);
th2=math.degrees(th2);
th3=math.degrees(th3);
th4=math.degrees(th4);
th5=math.degrees(th5);
print ("关节角度")
print(th1,'\n',th2,'\n',th3,'\n',th4,'\n',th5,'\n',)
print("末端坐标")
print( t05[:,3]);
