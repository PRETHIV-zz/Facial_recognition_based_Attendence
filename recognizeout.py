import cv2
import numpy as np
import os
import pymysql
from datetime import datetime

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
conn=pymysql.connect(host='localhost',user='root',password='',db='jpr')
a1=conn.cursor()
font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc



names = []
conn=pymysql.connect(host='localhost',user='root',password='',db='jpr')
s1="SELECT * FROM user_data"
a2=conn.cursor()
a2.execute(s1)
data=a2.fetchall()
m=0
for i in data:
    if int(i[0])>m and len(str(i[0]))<9:
        m=int(i[0])
for i in range(0,m+1):
    names.append(0)
for i in data:
    if len(str(i[0]))<9:
        names[int(i[0])]=i[1]





# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)


starttime=str(datetime.now())
starttime=starttime[11:19]
sarr=list(map(int,starttime.split(':')))
starttime=0
starttime=starttime+(sarr[0]*60)
starttime=starttime+sarr[1]

curtime=str(datetime.now())
curtime=curtime[11:19]
carr=list(map(int,curtime.split(':')))
curtime=0
curtime=carr[0]*60
curtime+=carr[1]

#print(starttime,curtime)

entry=[]

while True:
    curtime=str(datetime.now())
    curtime=curtime[11:19]
    carr=list(map(int,curtime.split(':')))
    curtime=0
    curtime=carr[0]*60
    curtime+=carr[1]
    
    collected_data=[]
    
    if abs(curtime-starttime)>1:
        for i in entry:
            sql="INSERT INTO outat (id, name, outtime, date) VALUES (%s, %s, %s, %s)"
            a1.execute(sql,i)
            conn.commit()
        starttime=curtime
        entry=[]
    ret, img =cam.read()
    #img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            #print(id)
            collected_data.append(id)
            id = names[id]
            iruku=False
            for i in entry:
                if str(i[1])==str(id):
                    iruku=True
                    break
            collected_data.append(id)
            curtime1=str(datetime.now())
            collected_data.append(curtime1[11:19])
            collected_data.append(curtime1[:10])
            if not iruku:
                entry.append(collected_data)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
#print(entry)
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
