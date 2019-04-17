import cv2, time,socket,sys
import numpy as np
from nijie import qudingdian
#yellowLower = np.array([15, 70, 150])
#yellowUpper = np.array([20, 90, 200])  # z这个颜色是白天用的
yellowLower = np.array([15, 120, 120])
yellowUpper = np.array([22, 150, 142])#z这个颜色晚上用的
# camera=cv2.VideoCapture("xiangpi.mov")
camera = cv2.VideoCapture(0)
zc = 620  #我的摄像头距离面62cm
SERVER_IP = "192.168.2.14"
SERVER_PORT = 8889
print("Starting socket: TCP...")
server_addr = (SERVER_IP, SERVER_PORT)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):#计算坐标函数
    if event == cv2.EVENT_LBUTTONDOWN:
        M = cv2.moments(c)
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
        image_points = np.array([
            (51., 270.),  # Nose tip     #已知的4个点的图像坐标
            (105., 270.),  # Chin
            (106., 324.),  # Left eye left corner
            (52., 324.),  # Right eye right corner
        ], dtype="double")
        model_points = np.array([           #已知的4个点的世界坐标坐标（自己设定）
            (170.0, 10.0, 0.0),  # Nose tip
            (190.0, 10.0, 0.0),  # Chin
            (190.0, 30.0, 0.0),  # Left eye left corner
            (170.0, 30.0, 0.0),  # Right eye right corner
        ])
        #单目相机的内外参数、畸变系数
        camera_matrix = np.array(
            [[1666.60423322581, 0, 349.373233019274],
             [0, 1673.17431212357, 265.163387912896],
             [0, 0, 1]], dtype="double")
        dist_coeffs = np.transpose([-0.200471180068700, 0.278898322055749, 0.00129390756221543, -0.00277202539360295])
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,
                                                                      image_points, camera_matrix, dist_coeffs,
                                                                      flags=cv2.SOLVEPNP_ITERATIVE)
        rotationtion_vector = cv2.Rodrigues(rotation_vector)[0]
        a11 = [[x * zc, y * zc, zc]]    #计算过程
        a1 = np.transpose(a11)
        # print(a1)
        a2 = np.linalg.inv(camera_matrix)
        # print("a2:\n {0}".format(a2))
        a3 = np.dot(a2, a1)
        # print("a3:\n {0}".format(a3))
        a4 = a3 - translation_vector
        # print("a4:\n {0}".format(a4))
        a5 = np.linalg.inv(rotationtion_vector)  # R的逆
        # print("a5:\n {0}".format(a5))
        world = np.dot(a5, a4)
        #print (type(world))
        list=(world[0,],world[1,]);
        #print("图像坐标：" + xy)
        #print("world:\n {0}".format(world))
        cx=world[0,]/10.;cy=world[1,]/10.
        cx=str(cx);cy=str(cy)
        #print(cx,cy)#打印鼠标打印点
        #qudingdian(world[0,]/10-6.,world[1,]/10.,7,1000,10),
        socket_tcp.send(cx.encode()+b','+cy.encode())
while True:
    try:
        print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
        socket_tcp.connect(server_addr)
        break
    except Exception:
        print("Can't connect to server,try it latter!")
        time.sleep(1)
        continue
data = socket_tcp.recv(1024)
print (data)
#socket_tcp.send(b'succeed')
print("连接成功，请点击鼠标启动抓取动作")
while (1):

    ret, camera1 = camera.read()
    hsv = cv2.cvtColor(camera1, cv2.COLOR_BGR2HSV)      #转hsv
    mask1 = cv2.inRange(hsv, yellowLower, yellowUpper)      #转hsv后设定值　通过颜色找到橡皮
    mask2 = cv2.dilate(mask1, np.ones((3,3)), iterations=15)
    mask3 = cv2.erode(mask2, np.ones((3,3)), iterations=9)      #
   # mask4 = cv2.dilate(mask3, np.ones((3,3)), iterations=10)
    _, contours, _a = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print (contours)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
    else:
        continue
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(camera1, [box], 0, (0, 0, 255), 2)

    #pts=np.array(c,np.int32)
    #pts=pts.reshape(-1,1,2)
    #x, y, w, h = cv2.boundingRect(c)
    #cv2.rectangle(camera1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #cv2.polylines(camera1,[pts],True,(0,255,255),1)
    #print(x, y)
    cv2.namedWindow("Camera")
    cv2.setMouseCallback("Camera", on_EVENT_LBUTTONDOWN)
    cv2.imshow("Camera", camera1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
         break

camera1.release()
cv2.destroyAllWindows()

