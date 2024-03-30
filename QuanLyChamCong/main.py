from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from customtkinter import *
import time
import capCheck
import cv2
import numpy as np
import face_recognition
def canGiuaCuaSo(window,width,height):
    window.resizable(width=False,height=False)
    screen_width=window.winfo_screenwidth()
    screen_height=window.winfo_screenheight()
    x=(screen_width-width)//2
    y=(screen_height-height)//2
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

def clock(frame):
    def update_clock():
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        day = time.strftime("%d") + "/" + time.strftime("%m") + "/" + time.strftime("%Y")
        clock_label.config(text=hour + ":" + minute + ":" + second + "\t" + day)
        frame.after(1000, update_clock)

    clock_label = Label(frame, text="", font=("Arial", 14), bg="white")
    clock_label.pack(anchor="w")
    update_clock()

def login_window():
    login_window = Tk()
    login_window.title("Đăng nhập")

    window_width=900

    window_height=600
    canGiuaCuaSo(login_window,window_width,window_height)
    
    # frame đăng nhập trái và frame hình ảnh nền phải
    left_frame=Frame(login_window,bg="white",width=window_width*0.5,height=window_height)
    right_frame=Frame(login_window,bg="white",width=window_width*0.5,height=window_height)

    left_frame.grid(column=0,row=0,sticky="nsew")
    right_frame.grid(column=1,row=0,sticky="nsew")
    login_window.grid_columnconfigure(0, weight=1)
    login_window.grid_columnconfigure(1, weight=1)
    login_window.grid_rowconfigure(0, weight=2)

    # right_frame với hình ảnh
    login_pic=Image.open("QuanLyChamCong/img/login.png")
    logic_pic_resized=login_pic.resize((450,600),Image.BICUBIC)
    new_pic=ImageTk.PhotoImage(logic_pic_resized)
    label_img=Label(right_frame,image=new_pic)
    label_img.pack()


    # left frame với login
    #đồng hồ và icon login
    left_frame_top=Frame(left_frame,bg="white",height=window_height*0.2,width=window_width*0.5)
    left_frame_top.pack(fill="both")

    clock(left_frame_top)
    img_login=ImageTk.PhotoImage(Image.open("QuanLyChamCong/img/loginIcon.png"))
    label_img_login=Label(left_frame_top,image=img_login,bg="white")
    label_img_login.pack(pady=30)


    # left frame với đăng nhập + mật khẩu
    left_frame_mid=Frame(left_frame,bg="white",height=window_height*0.6,width=window_width*0.5)
    left_frame_mid.pack(fill="both")

    user_label=Label(left_frame_mid,text="Tài khoản:",font=("arial",14),bg="white")
    user_label.grid(row=1,column=0,padx=20,pady=30,sticky="w")
    user_text=CTkEntry(left_frame_mid,font=("arial",14),width=300,height=40,fg_color="white",text_color="black",placeholder_text="Tên đăng nhập....",)
    user_text.grid(row=1,column=1)
    pass_label=Label(left_frame_mid,text="Mật khẩu:",font=("arial",14),bg="white")
    pass_label.grid(row=2,column=0,padx=20,pady=30,sticky="w")
    pass_text=CTkEntry(left_frame_mid,show="*",font=("arial",14),width=300,height=40,fg_color="white",text_color="black",placeholder_text="Mật khẩu....")
    pass_text.grid(row=2,column=1)


    # left frame với 2 nút nhấn
    left_frame_bot=Frame(left_frame,bg="white",height=window_height*0.2,width=window_width*0.5)
    left_frame_bot.pack(fill="both")

    # xử lý đăng nhập
    def dangNhap(event):
        loginAccess("Đăng Nhập")
    def loginAccess(text):
        if (text=="Đăng Nhập"):
            username = user_text.get()
            password = pass_text.get()
            if ( username=="admin" and password=="admin"):
                messagebox.showinfo("Thông báo","Đăng nhập thành công ^^")
                login_window.destroy()
                main_window()
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
        elif(text=="Chấm Công"):
            capCheck.chuanBi()
            capCheck.runCam()
            #messagebox.showinfo("Thông báo","Đây là giao diện chấm công")
    login_btn=CTkButton(left_frame_bot,text="Đăng Nhập",font=("Arial",18),corner_radius=32,fg_color="#4158D0",hover_color="light green",text_color="white",height=50,width=300,command=lambda: loginAccess("Đăng Nhập"))
    login_btn.pack(pady=40,padx=20)

    diemdanh_btn=CTkButton(left_frame_bot,text="Chấm công",font=("Arial",18),corner_radius=32,fg_color="#4158D0",hover_color="light blue",text_color="white",height=50,width=300,command=lambda: loginAccess("Chấm Công"))
    diemdanh_btn.pack(pady=0,padx=20)

    login_window.bind('<Return>', dangNhap)
    login_window.mainloop()



def main_window():

    window = Tk()
    window.title("Quản Lý Chấm Công")
    window_width=1500
    window_height=900
    window.resizable(width=False,height=False)
    window.geometry(f"{window_width}x{window_height}")
    #canGiuaCuaSo(window,window_width,window_height)

    # frame tiêu đề top, frame navigation trái, frame nội dung phải
    top_frame = Frame(window,bg="light gray",width=window_width,height=150)
    left_frame = Frame(window, bg="light blue", width=300, height=750)
    right_frame = Frame(window, bg="white", width=1300, height=750)

    top_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")
    left_frame.grid(row=1, column=0, sticky="nsew")
    right_frame.grid(row=1, column=1, sticky="nsew")
    # Thiết lập trọng số cho cột và hàng để chúng co giãn khi cửa sổ thay đổi kích thước
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=4)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=4)
    # frame trên thời gian và tiêu đề
    clock(top_frame)
    label_tieude=Label(top_frame,text="Hệ Thống Quản Lý Chấm Công",font=("Arial",20),bg="light gray")
    label_tieude.pack(pady=10)


    # frame giữa - trái là thanh điều hướng
            # sự kiện ấn nút
    def EventButtonClick(event):
        if( event=="Đăng Xuất"):
            window.destroy()
            login_window()
        elif( event=="Trang Chủ"):
            giaoDienTrangChu()
        elif (event=="Nhân Viên Mới"):
            giaoDienDangKy()
        elif( event=="Quản Lý Nhân Viên"):
            giaoDienQuanly()
        elif( event=="Thống Kê"):
            giaoDienThongKe()
        

            # tạo button trái điều hướng
    trangchu_btn=CTkButton(left_frame,text="Trang Chủ",width=200,height=60,command=lambda :EventButtonClick("Trang Chủ"))
    dangky_btn=CTkButton(left_frame,text="Nhân Viên Mới",width=200,height=60,command=lambda :EventButtonClick("Nhân Viên Mới"))
    qlnhanvien_btn=CTkButton(left_frame,text="Quản Lý Nhân Viên",width=200,height=60,command=lambda :EventButtonClick("Quản Lý Nhân Viên"))
    thongke_btn=CTkButton(left_frame,text="Thống Kê",width=200,height=60,command=lambda :EventButtonClick("Thống Kê"))
    dangxuat_btn=CTkButton(left_frame,text="Đăng Xuất",width=200,height=60,command=lambda :EventButtonClick("Đăng Xuất"))
    
    # Giao diện phải
    def giaoDienTrangChu():
        for widget in right_frame.winfo_children():
            widget.destroy()
        right_frame.config(bg="red")
        right_frame.grid_propagate(False)
        
    def giaoDienDangKy():
        # thông tin nhân viên + chụp hình + lưu
        for widget in right_frame.winfo_children():
            widget.destroy()
        right_frame.config(bg="blue")
        right_frame.grid_propagate(False)
        
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
    
        # bên trái, bên phải
            
        label_Khung=LabelFrame(right_frame_dk,bg="white",borderwidth=5)
        label_Khung.pack(pady=50)
        label_hinhAnh=Label(label_Khung, bg="light gray",text="",width=50,height=25)
        label_hinhAnh.pack()
        nhapTen=Entry(right_frame_dk,width=20)
        nhapTen.pack(pady=20)
        btn_dangky=CTkButton(right_frame_dk,text="Chụp Ảnh",command=showHinhAnh,width=100,height=100)
        btn_dangky.pack()


    def giaoDienQuanly():
        right_frame.grid_propagate(False)
        for widget in right_frame.winfo_children():
            widget.destroy()
        right_frame.config(bg="gray")
        
    def giaoDienThongKe():
        right_frame.grid_propagate(False)
        for widget in right_frame.winfo_children():
            widget.destroy()
        # thống kê điểm danh của nhân viên riêng, tất cả nhân viên theo tháng
        right_frame.config(bg="yellow")
        

    trangchu_btn.pack(pady=10,padx=20)
    dangky_btn.pack(pady=10,padx=20)
    qlnhanvien_btn.pack(pady=10,padx=20)
    thongke_btn.pack(pady=10,padx=20)
    dangxuat_btn.pack(pady=50,padx=20)
    window.mainloop()


login_window()


