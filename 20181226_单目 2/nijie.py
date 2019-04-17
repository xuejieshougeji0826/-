
import time
import numpy as np
import math
np.set_printoptions(suppress=True);

def qudingdian(px,py,pz,runningtime,jiange):
    a2=8.9;a3=7.179;a4=14.5;d=0;
    th1=math.atan2(py,px)
    c3=(px*px+py*py+pz*pz-a2*a2-a3*a3)/(2*a2*a3)
    s3=-(math.sqrt(1-c3*c3))
    th3=(math.atan2(s3,c3))
    c2=((math.sqrt(px*px+py*py))*(a2+a3*c3)+(pz*a2*s3))/(a2*a2+a3*a3+a2*a3*c3);
    s2=(pz*(a2+a3*c3)-math.sqrt(px*px+py*py)*a3*s3)/(a2*a2+a3*a3+a2*a3*c3)
    th2=(math.atan2(s2,c2))
    th4=-(math.pi/2)-(th2+th3)
    cos4=(math.cos(th4));sin4=(math.sin(th4));
    cos3 = (math.cos(th3));sin3 = (math.sin(th3));
    cos2 = (math.cos(th2));sin2 = (math.sin(th2));
    cos1 = (math.cos(th1));sin1 = (math.sin(th1));
    t01=np.array([[cos1,-(sin1),0,0],[-sin1,-cos1,0,0],[0,0,1,d],[0,0,0,1]])
    t12=np.array([[cos2,-(sin2),0,0],[0,0,-1,0],[sin2,cos2,0,0],[0,0,0,1]])
    t23=np.array([[cos3,-(sin3),0,a2],[sin3,cos3,0,0],[0,0,1,0],[0,0,0,1]])
    t34=np.array([[cos4,-(sin4),0,a3],[sin4,cos4,0,0],[0,0,-1,0],[0,0,0,1]])
    t45=np.array([[1,0,0,a4],[0,1,0,0],[0,0,1,0],[0,0,0,1]]);
    t02=np.dot(t01,t12);t03=np.dot(t02,t23);t04=np.dot(t03,t34);t05=np.dot(t04,t45);
    a=math.degrees(th1);
    b=math.degrees(th2);
    c=math.degrees(th3);
    d=math.degrees(th4);

    print ("关节角度")
    print (a,b,c,d);
    print("末端坐标")
    print( t04[:,3],'0');
    # def gh(qishi,zhongzhi,miao):
    #     delt=zhongzhi-qishi;melo=5.0*(t-miao/2.0)/(miao/2.0);deno=1.0/(1+math.exp(-melo))
    #     theta=delt*deno+qishi;
    #     return theta
    # for t in np.arange(0,runningtime,jiange):
    #     ag=gh(1500,1500-(11.11*a),runningtime)
    #     bg=gh(1500,1500+(11.11*(90-b)),runningtime)
    #     cg=gh(1500,1500+(11.11*(-c)),runningtime)
    #     dg=gh(1500,1500-(11.11*d),runningtime)
    #     time.sleep(jiange)
#qudingdian(11,0,7,1000,10)
