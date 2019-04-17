from control import Inverse
import serial  
import time  
# 打开串口  
ser = serial.Serial('/dev/ttyAMA0', 115200)  
inverse= Inverse()
time.sleep(1)
ser.write("{G0000#001P1500T2000!#002P1500T2000!#003P1500T2000!#004P1500T2000!}".encode())

time.sleep(2)
ser.write("{G0000#006P2000T2000!}".encode())
time.sleep(1)
print(inverse.go_point(20,-2,-0.5,3,0.05))
ser.write("{G0000#006P1530T2000!}".encode())
time.sleep(2)
ser.write("{G0000#002P1480T2000!}".encode())
time.sleep(2)
ser.write("{G0000#001P1184T2000!}".encode())
time.sleep(2)
ser.write("{G0000#002P1288T2000!#003P804T2000!#004P1414T2000!}".encode())
time.sleep(2)
ser.write("{G0000#006P2000T2000!}".encode())
time.sleep(3)
ser.write("{G0000#001P1500T2000!#002P1500T2000!#003P1500T2000!#004P1500T2000!}".encode())



