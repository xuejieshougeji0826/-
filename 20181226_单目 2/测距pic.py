import cv2
import numpy as np
zc=208.9
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)#取证，变为（x，y）'str'
        cv2.circle(im, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(im, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 255, 0), thickness=1)
        image_points = np.array([
         (223, 228),  # Nose tip
         (313, 226),  # Chin
         (316, 317),  # Left eye left corner
         (225, 319),  # Right eye right corner
        ], dtype="double")
        model_points = np.array([
         (0.0, 0.0, 0.0),  # Nose tip
         (20.0, 0.0, 0.0),  # Chin
         (20.0, 20.0, 0.0),  # Left eye left corner
         (0.0, 20.0, 0.0),  # Right eye right corner
         ])
        camera_matrix = np.array(
        [[940.97272, 0, 338.60695],
         [0, 937.38239, 207.88185],
         [0, 0, 1]], dtype="double")
        dist_coeffs = np.transpose([0.85504, -9.58387, 0.00207, 0.0069])
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,
        image_points, camera_matrix, dist_coeffs,flags=cv2.SOLVEPNP_ITERATIVE)
        rotationtion_vector = cv2.Rodrigues(rotation_vector)[0]
        a11 = [[x * zc, y * zc, zc]]
        a1 = np.transpose(a11)
        print(a1)
        a2 = np.linalg.inv(camera_matrix)

        print("a2:\n {0}".format(a2))
        a3 = np.dot(a2, a1)
        print("a3:\n {0}".format(a3))
        a4 = a3 - translation_vector
        print("a4:\n {0}".format(a4))
        a5 = np.linalg.inv(rotationtion_vector)  # R的逆
        print("a5:\n {0}".format(a5))
        world = np.dot(a5, a4)
        print("world:\n {0}".format(world))
        print(xy)



camera = cv2.VideoCapture(0)
# # 判断视频是否打开
# if (camera.isOpened()):
#     print('Open')
# else:
#     print('摄像头未打开')
camera=cv2.imread('')
while True:
     ret,im = camera.read()
     cv2.namedWindow("Output")
     cv2.setMouseCallback("Output", on_EVENT_LBUTTONDOWN)
     cv2.imshow('Output',im)
     key = cv2.waitKey(1) & 0xFF
     if key == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()
