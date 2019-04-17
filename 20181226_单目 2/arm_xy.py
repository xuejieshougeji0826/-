import cv2
import numpy as np
zc = 620
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)  # 取证，变为（x，y）'str'
        cv2.circle(im, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(im, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 255, 0), thickness=1)
        image_points = np.array([
            (51., 270.),  # Nose tip
            (105., 270.),  # Chin
            (106., 324.),  # Left eye left corner
            (52., 324.),  # Right eye right corner
        ], dtype="double")
        model_points = np.array([
            (170.0, 10.0, 0.0),  # Nose tip
            (190.0, 10.0, 0.0),  # Chin
            (190.0, 30.0, 0.0),  # Left eye left corner
            (170.0, 30.0, 0.0),  # Right eye right corner
        ])
        camera_matrix = np.array(
            [[1666.60423322581, 0, 349.373233019274],
             [0, 1673.17431212357, 265.163387912896],
             [0, 0, 1]], dtype="double")
        dist_coeffs = np.transpose([-0.200471180068700, 0.278898322055749, 0.00129390756221543, -0.00277202539360295])
        (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points,
                                                                      image_points, camera_matrix, dist_coeffs,
                                                                      flags=cv2.SOLVEPNP_ITERATIVE)
        rotationtion_vector = cv2.Rodrigues(rotation_vector)[0]
        a11 = [[x * zc, y * zc, zc]]
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
        print (type(world))
        list=(world[0,],world[1,]);
        #print("图像坐标：" + xy)
        #print("world:\n {0}".format(world))
camera = cv2.VideoCapture(0)
while True:
    ret, im = camera.read()
    cv2.namedWindow("Output")
    cv2.setMouseCallback("Output", on_EVENT_LBUTTONDOWN)
    cv2.imshow('Output', im)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
