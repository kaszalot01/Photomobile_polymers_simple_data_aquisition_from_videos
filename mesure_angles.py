import cv2
import math
import os
import pandas as pd

def mousePoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        size = len(pointsList)
        if size != 0 and size % 3 != 0:
            cv2.line(img, tuple(pointsList[round((size - 1) / 3) * 3]), (x, y), (0, 0, 255), 2)
        cv2.circle(img, (x, y), 1, (0, 0, 255), cv2.FILLED)
        pointsList.append([x, y])

def gradient(pt1, pt2):
    if pt2[0] == pt1[0]:
        return 0
    else:
        return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

def getAngle(pointsList):
    pt1, pt2, pt3 = pointsList[-3:]
    m1 = gradient(pt1, pt2)
    m2 = gradient(pt1, pt3)
    angR = math.atan((m2 - m1) / (1 + (m2 * m1)))
    angD = round(math.degrees(angR))
    cv2.putText(img, str(angD), (pt3[0] + 20, pt3[1] + 10), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 0, 255), 2)
    return angD

name=input("Name of a folder in \'Ghost_images\':")
folder='Ghost_images/'+name+'/'

subs=os.listdir(folder)
data={}
for sub in subs:
    path=folder+sub
    images=os.listdir(path)
    angles = []
    for image in images:

        print(image)
        img = cv2.imread(path+'/'+image)
        pointsList = []
        cv2.namedWindow(path + '/' + image, cv2.WINDOW_FULLSCREEN)
        while True:
            cv2.imshow(path + '/' + image, img)
            if cv2.waitKey(1) & 0xFF == ord('z'):
                break
            if len(pointsList) % 3 == 0 and len(pointsList) !=0:
                angle=getAngle(pointsList)
            cv2.setMouseCallback(path+'/'+image,mousePoints)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pointsList = []
                img = cv2.imread(path+'/'+image)
        cv2.destroyAllWindows()
        angles.append(angle)
    data[sub]=angles
print(data)
df=pd.DataFrame(data, index=['0.5s','1.7s','finish'])
print(df)
# if not os.path.exists("Angle_excels/"):
#     os.mkdir("Angle_excels/")
# excel_name='Angle_excels/'+name+'.xlsx'
# df.to_excel(excel_name, index=['0.5s','1.7s','finish'])

