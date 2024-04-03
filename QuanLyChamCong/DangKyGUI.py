from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from customtkinter import *
import face_recognition, cv2 
import numpy as np



def DangKyLayout(right_frame):
        left_frame_dk = Frame(right_frame, bg="pink",width=600,height=800)
        right_frame_dk = Frame(right_frame, bg="orange",width=600,height=800)
        left_frame_dk.grid(row=0,column=0,sticky="nsew")

        right_frame_dk.grid(row=0,column=1,sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        def showHinhAnh():
            cap=cv2.VideoCapture(0)
            dem=0
            while True:
                ret, frame= cap.read()
                frame=cv2.resize(frame,(350,350))
                img=cv2.flip(frame,1)
                img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                img3=ImageTk.PhotoImage(Image.fromarray(img1))
                if  len(face_recognition.face_encodings(img1)) >0:
                    dem+=1
                    cv2.imwrite(f"QuanLyChamCong/imgCheck/{nhapTen.get()}{dem}.png",frame)
                    print("được")
                label_hinhAnh.configure(image=img3,width=360,height=360)
                right_frame_dk.update() 
                if(dem==10):
                    break

            cap.release()
            cv2.destroyAllWindows()
    
        # nhập tên, chụp ảnh
        label_Khung=LabelFrame(right_frame_dk,bg="white",borderwidth=5)
        label_Khung.pack(pady=29)
        label_hinhAnh=Label(label_Khung, bg="light gray",text="",width=50,height=30)
        label_hinhAnh.pack()
        nhapTen=Entry(right_frame_dk,width=20, font=("arial", 15), borderwidth=3)
        nhapTen.pack(pady=20)
        btn_dangky=CTkButton(right_frame_dk,text="Chụp Ảnh",command=showHinhAnh,width=100,height=50)
        btn_dangky.pack()

        # left_frame_dk chứa các thành phần để nhập thông tin nhân viên
        label_ten = Label(left_frame_dk, text="Họ tên", width=19, height=3, font=("Arial", 15))
        label_ten.grid(row=0, column=0, pady=8)
        text_ten = Entry(left_frame_dk, font=("Arial", 15), borderwidth=3)
        text_ten.grid(row=0, column=1)
        label_ngaysinh = Label(left_frame_dk, text="Ngày sinh: ", width=19, height=3, font=("Arial", 15))
        label_ngaysinh.grid(row=1,column=0, pady=8)
        text_ngaysinh = Entry(left_frame_dk, font=("Arial", 15), borderwidth=3)
        text_ngaysinh.grid(row=1,column=1)
        label_sdt = Label(left_frame_dk, text="Số điện thoại: ", width=19, height=3, font=("Arial", 15))
        label_sdt.grid(row=2, column=0, pady=8)
        text_sdt = Entry(left_frame_dk, font=("Arial", 15), borderwidth=3)
        text_sdt.grid(row=2, column=1)
        label_gioitinh = Label(left_frame_dk, text="Giới tính: ", width=19, height=3, font=("Arial", 15))
        label_gioitinh.grid(row=3,column=0, pady=8)
        value_gioitinh = ["Nam", "Nữ"]
        combobox_gioitinh = ttk.Combobox(left_frame_dk, values=value_gioitinh, font=("Arial", 15), state="readonly")
        combobox_gioitinh["width"] = 19
        combobox_gioitinh.grid(row=3, column=1)
        label_chucvu = Label(left_frame_dk, text="Chức vụ: ", width=19, height=3, font=("Arial", 15))
        label_chucvu.grid(row=4,column=0, pady=8)
        value_chucvu = ["Quản lý", "Nhân viên", "Thực tập"]
        combobox_chucvu = ttk.Combobox(left_frame_dk, values=value_chucvu, font=("Arial", 15), state="readonly")
        combobox_chucvu["width"] = 19
        combobox_chucvu.grid(row=4, column=1)
        label_email = Label(left_frame_dk, text="Email: ", width=19, height=3, font=("Arial", 15))
        label_email.grid(row=5, column=0, pady=8)
        text_email = Entry(left_frame_dk, font=("Arial", 15), borderwidth=3)
        text_email.grid(row=5, column=1)


        # hàm clear các textfield, combobox
        def button_clear():
            text_ten.delete(0, END)
            text_ngaysinh.delete(0, END)
            text_sdt.delete(0, END)
            text_email.delete(0, END)
            combobox_chucvu.set('')
            combobox_gioitinh.set('')

        button_lammoi = CTkButton(left_frame_dk, text="Làm mới", width=100, height=50, command=button_clear)
        button_lammoi.grid(row=6, column=1, pady=52)
        button_xacnhan = CTkButton(left_frame_dk, text="Xác nhận", width=100, height=50)
        button_xacnhan.grid(row=6, column=2, pady=52)