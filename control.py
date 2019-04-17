import math,time,serial
import numpy as np

L0=7.5;L2=9;L3=7.3;L4=17.5;
ser = serial.Serial('/dev/ttyAMA0', 115200)# # 打开串口
if ser.isOpen == False:
    ser.open()
class Inverse(object):

    # x=22;
    # y=3;
    # z=1;
    def cal_inverse(self,x,y,z):
        self.genhao=1/(math.sqrt(2));
        #th1=acosd(x/(sqrt(x*x+y*y)));
        self.th1=math.asin(y/math.sqrt(x*x+y*y))
        self.k1=z+(self.genhao)*L4-L0;
        self.k2=math.sqrt(x*x+y*y)-self.genhao*L4;
        self.th3=math.acos((self.k1*self.k1+self.k2*self.k2-L2*L2-L3*L3)/(2*L2*L3));

        self.k3=L3*(math.cos(self.th3)-math.sin(self.th3))+L2;
        self.k4=L3*(math.cos(self.th3)+math.sin(self.th3))+L2;

        self.th2=math.pi-math.asin((self.k1+self.k2)/math.sqrt(self.k3*self.k3+self.k4*self.k4))-math.atan(self.k4/self.k3);
        if self.th2>=(math.pi*0.5):
            self.th2=self.th2-math.pi
        self.th5=45*math.pi/180;
        self.th4=math.pi-self.th5-self.th2-self.th3;
        print(self.th3,self.th4,self.th5)
        self.cos4=(math.cos(self.th4));self.sin4=(math.sin(self.th4));
        self.cos3 = (math.cos(self.th3));self.sin3 = (math.sin(self.th3));
        self.cos2 = (math.cos(math.pi*0.5-self.th2));self.sin2 = (math.sin(math.pi*0.5-self.th2));
        self.cos1 = (math.cos(self.th1));self.sin1 = (math.sin(self.th1));
        # print(math.cos(th2))
        # print(cos1,cos2,cos3,cos4)
        self.t01=np.array([[self.cos1,-(self.sin1),0,0],[self.sin1,self.cos1,0,0],[0,0,1,L0],[0,0,0,1]])
        self.t12=np.array([[self.cos2,-(self.sin2),0,0],[0,0,1,0],[self.sin2,self.cos2,0,0],[0,0,0,1]])
        self.t23=np.array([[self.cos3,-(self.sin3),0,L2],[-self.sin3,-self.cos3,0,0],[0,0,1,0],[0,0,0,1]])
        self.t34=np.array([[self.cos4,-(self.sin4),0,L3],[self.sin4,self.cos4,0,0],[0,0,-1,0],[0,0,0,1]])
        self.t45=np.array([[1,0,0,L4],[0,1,0,0],[0,0,1,0],[0,0,0,1]]);
        self.t02=np.dot(self.t01,self.t12)
        self.t03=np.dot(self.t02,self.t23)
        self.t04=np.dot(self.t03,self.t34)
        self.t05=np.dot(self.t04,self.t45);
        self.th1=math.degrees(self.th1)
        self.th2=math.degrees(self.th2)
        self.th3=math.degrees(self.th3)
        self.th4=math.degrees(self.th4)
        self.th5=math.degrees(self.th5)
        # print ("关节角度")
        # print(self.th1,'\n',self.th2,'\n',self.th3,'\n',self.th4,'\n',self.th5,'\n',)
        # print("末端坐标")
        # print( self.t05[:,3][0:3]);
        return self.th1,self.th2,self.th3,self.th4


    def gh(self,a,b,c,d,runningtime,jiange):
        def gh_function(qishi, zhongzhi, miao):
            delt = zhongzhi - qishi
            melo = 5.0 * (t - miao / 2.0) / (miao / 2.0)
            deno = 1.0 / (1 + math.exp(-melo))
            theta = delt * deno + qishi;
            return theta
        for t in np.arange(0,runningtime,jiange):
            print(self.th1, self.th2, self.th3, self.th4)
            self.ag =int(gh_function(1500, 1500 + (8.3888888 * self.th1), runningtime))
            self.bg =int(gh_function(1500, 1500 - (7.4074* self.th2), runningtime))
            self.cg =int(gh_function(1500, 1500 -(7.4074 * self.th3), runningtime))
            self.dg = int(gh_function(1500, 1500 -(7.4074 * self.th4), runningtime))
            single=str("{G0000#001P"+str(self.ag)+"T"+str(runningtime)+"!#002P"+str(self.bg)+"T"+str(runningtime)
                       +"!#003P"+str(self.cg)+"T"+str(runningtime)+"!#004P"+str(self.dg)+"T"+str(runningtime)+"!}")
            ser.write(single.encode())
            print(single)
            time.sleep(jiange)
            
            #print(self.ag,self.bg,self.cg,self.dg)
    def go_point(self,px,py,pz,runningtime,jiange):
        A,B,C,D=self.cal_inverse(px,py,pz)
        self.gh(A,B,C,D,runningtime,jiange)
if __name__ == '__main__':
    inverse= Inverse()
    #inverse.cal_inverse(22,3,1)