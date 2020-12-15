import cv2

for i in range(10):
    print(i)
    try:
        cap = cv2.VideoCapture(i)
        ret,frame = cap.read()
        cv2.imwrite(str(i)+'.jpg',frame)
        print('Port :', str(i),' is connected!!')
    except:
        pass