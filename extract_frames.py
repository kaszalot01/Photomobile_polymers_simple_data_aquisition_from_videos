import os
import cv2

def FrameCapture(path):
    vidObj = cv2.VideoCapture(path)
    if not os.path.exists("Frames/"):
        os.mkdir("Frames/")
    path="Frames/"+path.split('/')[1]+'/'+path.split('/')[2]
    # Path to video file

    if not os.path.exists(path):
        os.makedirs(path)

    # The "count" variable will be used to give the files names
    count = 0
    success = 1

    while success:
        # vidObj object calls read
        success, image = vidObj.read()
        # Saves the frames in a folder with the same name as the video
        # Names of the frames include their number
        try:
            cv2.imwrite(path+"/frame"+str(count)+".jpg", image)
        except cv2.error:
            pass
        count += 1


folder='Videos/'+input("Name of a folder in \'Videos\':")+'/'

videos=os.listdir(folder)
for vid in videos:
    video=folder+vid
    FrameCapture(video)