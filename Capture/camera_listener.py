import cv2
import requests
import os
import json

video_input = os.getcwd()+"/producer/data/Skateboard.mp4"
cap = cv2.VideoCapture(video_input)
frames_iter = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    print("inside loop")
    if ret == True:
        print("preparing frame")

        frames_iter = frames_iter + 1
        cv2.imwrite("tmp.jpg", frame)
        payload = {"image_path": "/apps/Capture/tmp.jpg",\
                            "part_name": "part_a", "topic": "WS1parta",\
                            "broker_url": "broker:9092", "image_file_format": "jpg",
                            "frames_iter": str(frames_iter)
                            }
        response = requests.post("http://127.0.0.1:8000/producer_app/video_input/", data=json.dumps(payload))
        print(response)

    else:
        break
cap.release()