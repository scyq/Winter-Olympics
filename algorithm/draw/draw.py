import cv2
import numpy as np


def draw():
    file = open("./algorithm/yolo/data/coordinates.txt")
    mutilcurling = []
    for line in file.readlines():
        curLine = line.strip().split(" ")
        mutilcurling.append(curLine[0:100])
    a = []
    frame_img = cv2.imread("./algorithm/draw/playground.jpg", 1)
    # 中心点
    # x = 240.75
    # y = 221

    for i in range(0, len(mutilcurling)):

        a = int(len(mutilcurling[i]) / 4)

        for j in range(0, a):
            xmin = int(mutilcurling[i][0 + j * 4])
            xmax = int(mutilcurling[i][2 + j * 4])
            ymin = int(mutilcurling[i][1 + j * 4])
            ymax = int(mutilcurling[i][3 + j * 4])
            xmid = (xmin + xmax) / 2
            ymid = (ymin + ymax) / 2
            cv2.circle(frame_img, (int(xmid), int(ymid)), 10, (0, 0, 255), -1)
    cv2.imwrite("./src/assets/frame.jpg", frame_img)


if __name__ == "__main__":
    draw()

# for i in range(0,len(mutilcurling)):
#   frame_img = cv2.imread('C:\\Users\\pc\\Desktop\\cut3\\%04d.jpeg'%(i+1),1);
#   a = int(len(mutilcurling[i])/4)
#
#   for j in range(0,a) :
#       xmin = int(mutilcurling[i][0+j*4])
#       xmax = int(mutilcurling[i][2+j*4])
#       ymin = int(mutilcurling[i][1+j*4])
#       ymax = int(mutilcurling[i][3+j*4])
#       cv2.rectangle(frame_img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
#       # cv2.rectangle(frame_img, (640, 610), (770, 710), (0, 0, 255), 2)
#
#
#   cv2.imwrite('C:\\Users\\pc\\Desktop\\huakuang\\%04d.jpeg'%(i+1),frame_img)


if __name__ == "__main__":
    draw()