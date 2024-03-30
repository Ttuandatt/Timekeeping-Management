import cv2
import face_recognition
import os
import time
import numpy as np
from datetime import datetime
path="QuanLyChamCong/imgCheck"
images=[]
classNames=[]
encodeListKnow=[]
def chuanBi():
    global encodeListKnow
    myList=os.listdir(path) 
    print(f"List: {myList}")
    #step 1: load ảnh
    for pic in myList:
        curImg=cv2.imread(f"{path}/{pic}") 
        images.append(curImg)
        classNames.append(os.path.splitext(pic)[0]) 
    encodeListKnow=MahoaListPic(images)
    print("Mã hóa thành công")

#step 3:encoding
dem=0
def MahoaListPic(images):
    global dem
    encodeList=[]
    for pic in images:
        pic=cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
        if  len(face_recognition.face_encodings(pic)) >0:
            encode=face_recognition.face_encodings(pic)[0]
            encodeList.append(encode)
            dem+=1
    print(f"Số lượng {dem}")
    return encodeList



# hàm đưa vào excel
def diemDanh(name):
    with open("QuanLyChamCong/diemDanh.csv","r+") as fi:
        myDataList=fi.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            nowTime=datetime.now()
            dateString=nowTime.strftime("%H:%M:%S")
            fi.writelines(f"\n{name},{dateString}")
        else: 
            vitri=nameList.index(name)
            check=myDataList[vitri].split(",")
            if len(check) <3:
                time_default="07:50:00"
                time_default=datetime.strptime(time_default,"%H:%M:%S")
                leaveTime=datetime.now()
                dateString=leaveTime.strftime("%H:%M:%S")
                #print("Thời gian trừ:")
                #print(leaveTime.time())
                if (leaveTime.time() > time_default.time()):
                    myDataList[vitri]=myDataList[vitri].rstrip("\n")+","+dateString+"\n"
                    #print("Sau khi đổi: "+myDataList[vitri])
                    fi.seek(0)
                    fi.truncate()
                    fi.writelines(myDataList)
                else: 
                    print("Chưa tới giờ điểm danh")
# đổi thành videoCapture("OpenCVLearning/video-test.mp4") để chạy video
def runCam():
    cap=cv2.VideoCapture(0)
    flag=False
    while True:
        ret, frame= cap.read()

        frameS=cv2.resize(frame,(0,0),None,fx=0.5,fy=0.5)
        frameS=cv2.cvtColor(frameS,cv2.COLOR_BGR2RGB)

        # step 2: xác định vị trí khuôn mặt trên cam và encode hình
        faceCurFrame=face_recognition.face_locations(frameS) # lấy từng khuôn mặt và vị trí khuôn mặt hiện tại
        encodeCurFrame=face_recognition.face_encodings(frameS)

        for encodeFace, faceLocation in zip(encodeCurFrame, faceCurFrame):

            kiemTra=face_recognition.compare_faces(encodeListKnow,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnow,encodeFace)
            matchIndex=np.argmin(faceDis) 
            if faceDis[matchIndex] < 0.5:
                name=classNames[matchIndex]
                diemDanh(name[:-1])
                #flag=True
                print(f"Điểm danh thành công: {name}")
            else: name="Unknow"
            y1,x2,y2,x1=faceLocation
            y1,x2,y2,x1=y1*2,x2*2,y2*2,x1*2
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(frame,name,(x2,y2),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        cv2.imshow("Điểm Danh",frame)
        if( cv2.waitKey(1)==ord("q") or flag==True):
            break
    time.sleep(5)
    cap.release()
    cv2.destroyAllWindows()
