import cv2,time
import numpy as np
#yellowLower = np.array([15, 70, 150])
#yellowUpper = np.array([20, 90, 200])#z这个颜色是白天用的
yellowLower = np.array([15, 120, 120])
yellowUpper = np.array([22, 150, 142])#z这个颜色晚上用的
#yellowLower = np.array([20, 140, 180])
#yellowUpper = np.array([28, 170, 200])
print(time.time())
#camera=cv2.VideoCapture("xiangpi.mov")
camera=cv2.VideoCapture(0)

while(1):
    ret,camera1=camera.read()
    hsv = cv2.cvtColor(camera1, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, yellowLower, yellowUpper)
    #mask2 = cv2.erode(mask1, None, iterations=1)
    mask2 = cv2.dilate(mask1, None, iterations=15)
    mask3 = cv2.erode(mask2, None, iterations=8)
    #mask4 = cv2.dilate(mask3, None, iterations=5)
    _, contours, _a = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print (contours)
    if len(contours)>0:
        c=max(contours,key=cv2.contourArea)
        #com=cv2.approxPolyDP(c,30,True)
    else:continue
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box=np.int0(box)
    cv2.drawContours(camera1,[box],0,(0,0,255),2)

    M=cv2.moments(c)
    cx=int(M['m10']/M['m00'])
    cy = int(M['m01'] / M['m00'])
    print (cx,cy)
    #x, y, w, h = cv2.boundingRect(c)
    #cv2.rectangle(camera1, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.namedWindow("Camera")
    cv2.imshow( "Camera", camera1)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
camera1.release()
cv2.destroyAllWindows()

