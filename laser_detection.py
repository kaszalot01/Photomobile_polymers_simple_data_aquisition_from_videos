# import required libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from natsort import natsorted
import pandas as pd

def mask(img_path):
    img=cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_purple = np.array([120,110,110])
    upper_purple = np.array([360,255,255])

    # Create a mask. Threshold the HSV image to get only yellow colors
    return cv2.inRange(hsv, lower_purple, upper_purple)

def find_laser(video):
    path='Frames/'+video
    files = natsorted(os.listdir(path))
    x = []
    y = []
    for i in range(len(files)):
        x.append(i)
        y.append(np.sum(mask(('Frames/' + video + '/' +files[i]))==255))
    plt.figure()
    plt.xlabel('Frame')
    plt.ylabel('Number of purple pixels')
    plt.plot(x,y,'.',label='f')
    plt.plot(x,np.gradient(y),'-',label='df/dx')
    plt.legend()
    if not os.path.exists("Reference_plots/"):
        os.mkdir("Reference_plots/")
    if not os.path.exists("Reference_plots/" + video.split('/')[0]):
        os.mkdir("Reference_plots/" + video.split('/')[0])
    plt.savefig('Reference_plots/'+video.split('/')[0]+'/plot_' + video.split('/')[1] + '.png', dpi=300)
    return np.argmax(np.gradient(y)),np.argmin(np.gradient(y))


folder=input("Name of a folder in \'Frames\':")+'/'
videos=os.listdir('Videos/'+folder)
fps=[]
starts=[]
finishes=[]

for vid in videos:
    video=folder+vid
    fps.append(cv2.VideoCapture('Videos/'+video).get(cv2.CAP_PROP_FPS))
    path = "Frames/"+video+"/" # folder name where frames will be stored
    start, finish=find_laser(video)
    starts.append(start)
    finishes.append(finish)
df=pd.DataFrame({
    "file":videos,
    "fps": fps,
    "start": starts,
    "finish": finishes
})

print(df)
if not os.path.exists("Laser_excels/"):
    os.mkdir("Laser_excels/")
# writing to Excel
excel_name='Laser_excels/'+folder[:-1]+'.xlsx'
# write DataFrame to excel
df.to_excel(excel_name, index=False )



