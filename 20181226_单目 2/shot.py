import cv2
cap=cv2.VideoCapture(0)
i=0
while True:
    ret,frame=cap.read()
    k=cv2.waitKey(1)
    cv2.imshow("capture",frame)
    if k==ord("a"):
        cv2.imwrite("C:/Users/Administrator/Desktop/single2/"+"pic"+"_"+str(i)+'.jpg',frame)
        i+=1

cap.release()
cv2.destroyAllWindows()