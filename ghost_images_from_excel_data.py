import pandas as pd
import cv2
import os

excel_name=input("Name of a spreadsheet in folder \'Laser_excels\' (without \'.xlsl\'):")
excel_file_path='Laser_excels/'+excel_name
if excel_file_path[-5:]!=".xlsx":
    excel_file_path+='.xlsx'
df = pd.read_excel(excel_file_path)
if not os.path.exists("Ghost_images/"):
    os.mkdir("Ghost_images/")

# Access individual DataFrames by sheet name
for i in range(len(df['file'])):

    file=df['file'][i]
    start=df['start'][i]-1
    finish=df['finish'][i]
    fps=df['fps'][i]
    s05 = fps // 2
    s17 = int(fps * 1.7)

    if not os.path.exists("Ghost_images/" + excel_name):
        os.makedirs("Ghost_images/" + excel_name)

    frame_start = 'Frames/' + excel_name + '/' + file + '/'+'frame'+ str(start) +'.jpg'
    frame_finish = 'Frames/' + excel_name  + '/' + file + '/'+'frame'+ str(finish) +'.jpg'
    frame_15 = 'Frames/' + excel_name  + '/' + file + '/'+'frame'+ str(start+s05) +'.jpg'
    frame_51 = 'Frames/' + excel_name + '/' + file + '/'+'frame'+ str(start+s17) +'.jpg'

    img_start = cv2.imread(frame_start)
    img_finish = cv2.imread(frame_finish)
    img_15 = cv2.imread(frame_15)
    img_51 = cv2.imread(frame_51)

    diff_15=cv2.add(cv2.subtract(img_15, img_start), cv2.subtract(img_start, img_15))
    diff_51=cv2.add(cv2.subtract(img_51, img_start), cv2.subtract(img_start, img_51))
    diff_finish=cv2.add(cv2.subtract(img_finish, img_start), cv2.subtract(img_start, img_finish))

    if not os.path.exists("Ghost_images/"+excel_name+'/'+file):
        os.makedirs("Ghost_images/"+excel_name+'/'+file)

    cv2.imwrite('Ghost_images/'+excel_name+'/'+file+'/'+'diff_after_0.5s.jpg',diff_15)
    cv2.imwrite('Ghost_images/'+excel_name+'/'+file+'/'+'diff_after_1.7s.jpg',diff_51)
    cv2.imwrite('Ghost_images/'+excel_name+'/'+file+'/'+'diff_at_finish.jpg',diff_finish)