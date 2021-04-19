import sys
from algorithm.yolo.yolo import YOLO
from PIL import Image
import os, cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def detect_curling(video_path, txt_path):
    """
    video_path: 视频路径
    txt_path: 保存的结果路径，保存内容为冰壶的[left, top, right, bottom]
    """
    Yolo = YOLO()
    cap = cv2.VideoCapture(video_path)
    f = open(txt_path, "w")
    while True:
        ret, img = cap.read()
        if not ret:
            break
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img = Yolo.detect_image(img, f)
        f.write("\n")
    Yolo.close_session()
    f.close()


if __name__ == "__main__":
    detect_curling(
        "./algorithm/yolo/data/1.mp4", "./algorithm/yolo/data/coordinates.txt"
    )
