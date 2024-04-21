import cv2, os, time
import face_recognition
import numpy as np
from tkinter import *
from datetime import datetime
import mysql.connector
from PIL import ImageTk, Image
import LichChamCongGUI
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
    myListFolder=os.listdir(path) 
    print(f"List: {myListFolder}")
    #step 1: load ảnh
    for folderAnh in myListFolder:
        myList=os.listdir(path+"/"+folderAnh)
        for pic in myList:
            curImg=cv2.imread(f"{path}/{folderAnh}/{pic}")
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

# hàm điểm danh đưa vào excel
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
            return 1, dateString
        else: 
            vitri=nameList.index(name)
            check=myDataList[vitri].split(",")
            if len(check) <3:
                time_default="16:00:00"
                time_default=datetime.strptime(time_default,"%H:%M:%S")
                leaveTime=datetime.now()
                dateString=leaveTime.strftime("%H:%M:%S")
                if (leaveTime.time() > time_default.time()):
                    myDataList[vitri]=myDataList[vitri].rstrip("\n")+","+dateString+"\n"
                    # xóa toàn bộ nội dung và add lại nội dung mới
                    fi.seek(0)
                    fi.truncate()
                    fi.writelines(myDataList)
                    return 2, dateString
                else: 
                    return 0,"Chưa tới giờ điểm danh!!"
            else:
                return 0,"Bạn đã điểm danh rồi!!"




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
    label_Tieude=Label(right_window,text="Thông Tin Nhân Viên",font=("arial",20))
    label_MaNV=Label(right_window,text="Mã Nhân Viên:",font=("arial",18))
    label_HoTen=Label(right_window,text="Họ và Tên:",font=("arial",18))
    label_NgaySinh=Label(right_window,text="Ngày Sinh:",font=("arial",18))
    label_Sdt=Label(right_window,text="Số Điện Thoại:",font=("arial",18))
    label_ThoiGian=Label(right_window,text="Thời Gian:",font=("arial",18))
    label_Tieude.pack(pady=15)
    label_MaNV.pack(pady=15,anchor="w")
    label_HoTen.pack(pady=15,anchor="w")
    label_NgaySinh.pack(pady=15,anchor="w")
    label_Sdt.pack(pady=15,anchor="w")
    label_ThoiGian.pack(pady=15,anchor="w")
    # nửa trái
    left_window_Cam=Frame(left_window,width=window_width*0.6,height=window_height*0.8)
    left_window_ThongBao=Frame(left_window,width=window_width*0.6,height=window_height*0.2)
    left_window_Cam.grid(row=0,column=0,sticky="nsew")
    left_window_ThongBao.grid(row=1,column=0,sticky="nsew")

    def hienThongTinDiemDanhThanhCong(maNV):
        mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
        sql="Select * From nhanvien Where MaNV=%s and TrangThai=%s"
        mycursor=mydatabase.cursor()
        mycursor.execute(sql,(maNV,1))
        result=mycursor.fetchall()
        infoNhanVien=[]
        day=datetime.now().strftime("%Y-%m-%d")
        thang=datetime.now().month; nam=datetime.now().year
        KCHienTai=""
        if (thang<10):
            KCHienTai="KC0"+str(thang)+str(nam)
        else:
            KCHienTai="KC"+str(thang)+str(nam)
        LichChamCongGUI.KyCongChiTietChoNhanVien(KCHienTai)
        for i in result:
            infoNhanVien.append(i)
        infoNhanVien=infoNhanVien[0] # vì fetchall trả về số lượng nên phải lấy index [0]
        # hiển thị thông tin NV: mã, hoten, ngaysinh, sdt
        typeTime,dateTime=diemDanh(infoNhanVien[0])

        if ( typeTime==1):
            # lưu thời gian điểm danh của NV vào congnhanvien
            label_ThongBao.configure(text=f"Thông báo: điểm danh {infoNhanVien[1]} vào làm thành công")
            mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
            mycursor=mydatabase.cursor()
            sql="""Insert into congnhanvien (MaKyCong, MaNV, HoTen, Ngay, Thu, ThoiGianVao, ThoiGianRa) 
                    Values (%s, %s, %s, %s, %s, %s, %s)"""
            tuan = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
            values=(KCHienTai,infoNhanVien[0],infoNhanVien[1],day,tuan[datetime.now().weekday()],dateTime,"")
            mycursor.execute(sql,values)
            mydatabase.commit()
            # đánh dấu ngày điểm danh vào kycongchitiet
            sql2 = f"UPDATE kycongchitiet SET Day{str(datetime.now().day)}=%s, SoNgayCong=SoNgayCong+%s Where MaKyCong=%s and MaNV=%s"
            values2 = ("+", 0.5,KCHienTai,infoNhanVien[0])
            mycursor.execute(sql2,values2)
            mydatabase.commit()
            mycursor.close()
        elif (typeTime==2):
            label_ThongBao.configure(text=f"Thông báo: điểm danh {infoNhanVien[1]} ra về thành công")
            mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
            mycursor=mydatabase.cursor()
            sql="""Update congnhanvien set ThoiGianRa=%s Where MaKyCong=%s and MaNV=%s and Ngay=%s"""
            values=( dateTime,KCHienTai,infoNhanVien[0],day)
            mycursor.execute(sql,values)
            mydatabase.commit()
            # đánh dấu ngày điểm danh vào kycongchitiet lần 2 để điểm danh full ngày
            sql2 = f"UPDATE kycongchitiet SET Day{str(datetime.now().day)}=%s, SoNgayCong=SoNgayCong+%s Where MaKyCong=%s and MaNV=%s"
            values2 = ("X", 0.5,KCHienTai,infoNhanVien[0])
            mycursor.execute(sql2,values2)
            mydatabase.commit()
            mycursor.close()
        elif( typeTime==0):
            label_ThongBao.configure(text=f"Thông báo: {dateTime}")
            pass
        label_MaNV.configure(text=f"Mã Nhân Viên: {infoNhanVien[0]}")
        label_HoTen.configure(text=f"Họ và Tên: {infoNhanVien[1]}")
        label_NgaySinh.configure(text=f"Ngày Sinh: {infoNhanVien[2]}")
        label_Sdt.configure(text=f"Số Điện Thoại: {infoNhanVien[3]}")
        label_ThoiGian.configure(text=f"Thời Gian: {dateTime}")

        pass

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

                face_recognition.compare_faces(encodeListKnow,encodeFace)
                faceDis=face_recognition.face_distance(encodeListKnow,encodeFace)
                matchIndex=np.argmin(faceDis) 
                if faceDis[matchIndex] < 0.5:
                    if( flag == False):
                        name=classNames[matchIndex] # tên ảnh
                        hienThongTinDiemDanhThanhCong(name[:-1])
                        flag=True
                    success_count += 1
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
            if(success_count>=10):
                break
        cap.release()
        cv2.destroyAllWindows()
        CuaSoDiemDanh.destroy()
    label_Khung=LabelFrame(left_window_Cam,width=450,height=450)
    label_Khung.pack(pady=15,padx=10)  
    label_Cam=Label(label_Khung)
    label_Cam.pack()
    label_ThongBao=Label(left_window_ThongBao,text="",font=("Arial",15),foreground="green")
    label_ThongBao.pack(pady=15)
    showCam()

