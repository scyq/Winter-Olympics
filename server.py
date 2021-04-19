from fastapi import FastAPI
from algorithm.yolo.demo import detect_curling
from algorithm.draw.draw import draw
from fastapi.responses import JSONResponse, FileResponse
import os

app = FastAPI()
headers = {"Access-Control-Allow-Origin": "*"}

# 返回画完后的图像
@app.get("/start")
def start():
    try:
        detect_curling(
            "./algorithm/yolo/data/1.mp4", "./algorithm/yolo/data/coordinates.txt"
        )
        draw()
    except:
        return False
    path = os.path.dirname("/algorithm/output/frame.jpg")
    return FileResponse(path, headers=headers)
