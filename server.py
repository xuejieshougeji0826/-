import socket,sys,re,serial,time
from control import Inverse
ser = serial.Serial('/dev/ttyAMA0', 115200)
if ser.isOpen == False:
    ser.open()
inverse= Inverse()
# define host ip: Rpi's IP
HOST_IP = "192.168.2.14"
HOST_PORT = 8888
print("Starting socket: TCP...")
# 1.create socket object:socket=socket.socket(family,type)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("TCP server listen @ %s:%d!" % (HOST_IP, HOST_PORT))
host_addr = (HOST_IP, HOST_PORT)
# 2.bind socket to addr:socket.bind(address)
socket_tcp.bind(host_addr)
# 3.listen connection request:socket.listen(backlog)
socket_tcp.listen(1)
# 4.waite for client:connection,address=socket.accept()
socket_con, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s." % client_ip)
socket_con.send("Welcome to RPi TCP server!".encode())

print("Receiving package...")
#reset()
def cut_and_deal(rec_data):


    rec_data=str(rec_data)
    a = [i.start() for i in re.finditer("]" ,rec_data)]
    x=float(rec_data[3:a[0]-1])
    y=float(rec_data[a[0]+3:len(rec_data)-2])
    print (x,y)
    return x,y

while True:
##    try:
        data = socket_con.recv(1024)
        if len(data) > 0:
            #print(data)
            socket_con.send(data)
            x,y=cut_and_deal(data)
            time.sleep(1)
            ser.write("{G0000#001P1500T2000!#002P1500T2000!#003P1500T2000!#004P1500T2000!}".encode())

            time.sleep(2)
            ser.write("{G0000#006P2000T2000!}".encode())
            time.sleep(1)
            print(inverse.go_point(int(x),int(y),-1.2,3,0.05))
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

            continue
#    except Exception:
#        socket_tcp.close()
#        print("?")
#        sys.exit(1)


