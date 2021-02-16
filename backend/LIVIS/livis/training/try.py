import os 
import csv 
import cv2
image_dir = r"/home/lincode/Desktop/livis_v2/republic/backend/LIVIS/livis/training/image_data"
out_dir = r"/home/lincode/Desktop/livis_v2/republic/backend/LIVIS/livis/training/bb_img"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
csv_path = r"/home/lincode/Desktop/livis_v2/republic/backend/LIVIS/livis/training/train_labels.csv"

with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i in csv_reader:
        img = cv2.imread(os.path.join(image_dir,i[0]))
        img_name = i[0]
        xmin = str(i[4])
        # print(xmin)
        ymin = str(i[5])
        xmax = str(i[6])
        ymax= str(i[7])
        st = (int(xmin),int(ymin))
        ed = (int(xmax),int(ymax))
        c = (255, 0, 0)
        thickness = 3
        image = cv2.rectangle(img,st,ed,c,thickness) 
    cv2.imwrite(os.path.join(out_dir,img_name),image)    

