import cv2
import face_recognition
import os
import time
import numpy as np
from tkinter import *
from datetime import datetime
from PIL import ImageTk, Image
path="QuanLyChamCong/imgCheck"
images=[]
classNames=[]
encodeListKnow=[]

def canGiuaCuaSo(window,width,height):
    window.resizable(width=False,height=False)
    screen_width=window.winfo_screenwidth()
    screen_height=window.winfo_screenheight()
    x=(screen_width-width)//2
    y=(screen_height-height)//2
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

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
            return dateString
        else: 
            vitri=nameList.index(name)
            check=myDataList[vitri].split(",")
            if len(check) <3:
                time_default="23:00:00"
                time_default=datetime.strptime(time_default,"%H:%M:%S")
                leaveTime=datetime.now()
                dateString=leaveTime.strftime("%H:%M:%S")
                if (leaveTime.time() > time_default.time()):
                    myDataList[vitri]=myDataList[vitri].rstrip("\n")+","+dateString+"\n"
                    fi.seek(0)
                    fi.truncate()
                    fi.writelines(myDataList)
                    return dateString
                else: 
                    print("Chưa tới giờ điểm danh")


# đổi thành videoCapture("OpenCVLearning/video-test.mp4") để chạy video
def runCam(windowLogin):
    CuaSoDiemDanh=Toplevel(windowLogin)
    CuaSoDiemDanh.title("Điểm Danh Nhân Viên")
    window_width=800
    window_height=600
    canGiuaCuaSo(CuaSoDiemDanh,window_width,window_height)

    # tách ra 1 bên là chứa camera và thông báo, 1 bên là thông tin của nhân viên điểm danh
    left_window=Frame(CuaSoDiemDanh,width=window_width*0.6,height=window_height)
    right_window=Frame(CuaSoDiemDanh,width=window_width*0.4,height=window_height)
    left_window.grid(row=0,column=0,sticky="nsew")
    right_window.grid(row=0,column=1,sticky="nsew")
    CuaSoDiemDanh.grid_columnconfigure(0,weight=1)
    CuaSoDiemDanh.grid_columnconfigure(1,weight=1)
    CuaSoDiemDanh.grid_rowconfigure(0,weight=1)
    # nửa phải
    label_Tieude=Label(right_window,text="Thông Tin Nhân Viên",font=("arial",25))
    label_MaNV=Label(right_window,text="Mã Nhân Viên:",font=("arial",20))
    label_HoTen=Label(right_window,text="Họ và Tên:",font=("arial",20))
    label_ThoiGian=Label(right_window,text="Thời Gian:",font=("arial",20))
    label_Tieude.pack(pady=30)
    label_MaNV.pack(pady=25,anchor="w")
    label_HoTen.pack(pady=25,anchor="w")
    label_ThoiGian.pack(pady=25,anchor="w")
    # nửa trái
    left_window_Cam=Frame(left_window,width=window_width*0.6,height=window_height*0.8)
    left_window_ThongBao=Frame(left_window,width=window_width*0.6,height=window_height*0.2)
    left_window_Cam.grid(row=0,column=0,sticky="nsew")
    left_window_ThongBao.grid(row=1,column=0,sticky="nsew")
        # chứa cam
    def showCam():
        flag=False
        success_count = 0
        cap=cv2.VideoCapture(0)
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
                    dateTime=diemDanh(name[:-1])
                    success_count += 1
                    label_ThongBao.configure(text=f"Thông báo: đã điểm danh {name[:-1]} vào làm thành công")
                    label_MaNV.configure(text="Mã Nhân Viên: 9999")
                    label_HoTen.configure(text=f"Họ và Tên: {name[:-1]}")
                    label_ThoiGian.configure(text=f"Thời Gian: {dateTime}")
                    if success_count >= 10:
                        flag=True
                else: name="Unknow"
                y1,x2,y2,x1=faceLocation
                y1,x2,y2,x1=y1*2,x2*2,y2*2,x1*2
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.putText(frame,name,(x2,y2),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(image=frame)
            label_Cam.configure(image=frame,width=450,height=450)
            left_window_Cam.update()
            if(flag):
                break
        cap.release()
        cv2.destroyAllWindows()
        CuaSoDiemDanh.destroy()
    label_Khung=LabelFrame(left_window_Cam,width=450,height=450)
    label_Khung.pack(pady=15,padx=10)  
    label_Cam=Label(label_Khung)
    label_Cam.pack()
    label_ThongBao=Label(left_window_ThongBao,text="",font=("Arial",15))
    label_ThongBao.pack(pady=15)
    showCam()

