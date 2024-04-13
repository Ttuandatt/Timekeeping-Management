from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from customtkinter import *
import time, face_recognition, cv2 
import capCheck
import numpy as np
import TrangChuGUI, DangKyGUI, QuanLyGUI,LichChamCongGUI, ThongKeGUI # import các giao diện


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



def Login_Window():
    login_window = Tk()
    login_window.title("Đăng nhập")

    window_width=1000

    window_height=650
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
    login_pic=Image.open("QuanLyChamCong/img/loginImage.png")
    logic_pic_resized=login_pic.resize((int(window_width*0.5+80),window_height),Image.BICUBIC)
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
    user_text=CTkEntry(left_frame_mid,font=("arial",14),width=280,height=40,fg_color="white",text_color="black",placeholder_text="Tên đăng nhập....",)
    user_text.grid(row=1,column=1)
    pass_label=Label(left_frame_mid,text="Mật khẩu:",font=("arial",14),bg="white")
    pass_label.grid(row=2,column=0,padx=20,pady=30,sticky="w")
    pass_text=CTkEntry(left_frame_mid,show="*",font=("arial",14),width=280,height=40,fg_color="white",text_color="black",placeholder_text="Mật khẩu....")
    pass_text.grid(row=2,column=1)


    # left frame với 2 nút nhấn
    left_frame_bot=Frame(left_frame,bg="white",height=window_height*0.2,width=window_width*0.5)
    left_frame_bot.pack(fill="both")

    # xử lý đăng nhập
    def dangNhap(event):
        loginAccess("Đăng Nhập")
    def loginAccess(text):
        global stop_clock
        if (text=="Đăng Nhập"):
            username = user_text.get()
            password = pass_text.get()
            if ( username=="admin" and password=="admin"):
                messagebox.showinfo("Thông báo","Đăng nhập thành công ^^")
                login_window.withdraw()
                Main_Window(login_window)
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
        elif(text=="Chấm Công"):
            capCheck.chuanBi()
            capCheck.runCam(login_window)

    login_btn=CTkButton(left_frame_bot,text="Đăng Nhập",font=("Arial",18),corner_radius=32,fg_color="#4158D0",hover_color="light green",text_color="white",height=50,width=300,command=lambda: loginAccess("Đăng Nhập"))
    login_btn.pack(pady=40,padx=20)

    diemdanh_btn=CTkButton(left_frame_bot,text="Chấm công",font=("Arial",18),corner_radius=32,fg_color="#4158D0",hover_color="light blue",text_color="white",height=50,width=300,image=CTkImage(Image.open("QuanLyChamCong/img/camera.png"),size=(40,40)),command=lambda: loginAccess("Chấm Công"))
    diemdanh_btn.pack(pady=0,padx=20)

    login_window.bind('<Return>', dangNhap)
    login_window.mainloop()
   



def Main_Window(login_window):
    window = Toplevel(login_window)
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


    # frame giữa - trái là MenuTask
    def EventButtonClick(event):
        if( event=="Đăng Xuất"):    
            window.withdraw()
            login_window.deiconify()
        elif (event=="Nhân Viên Mới"):
            giaoDienDangKy()
        elif( event=="Quản Lý Nhân Viên"):
            giaoDienQuanly()
        elif( event=="Lịch Chấm Công"):
            giaoDienLichChamCong()
        elif( event=="Thống Kê"):
            giaoDienThongKe()
            # tạo button trái Task
    dangky_btn=CTkButton(left_frame,text="Nhân Viên Mới",width=200,height=60,image=CTkImage(Image.open("QuanLyChamCong/img/thongtin.png"),size=(50,50)),anchor="w",command=lambda :EventButtonClick("Nhân Viên Mới"))
    qlnhanvien_btn=CTkButton(left_frame,text="Quản Lý Nhân Viên",width=200,height=60,image=CTkImage(Image.open("QuanLyChamCong/img/taikhoan.png"),size=(50,50)),anchor="w",command=lambda :EventButtonClick("Quản Lý Nhân Viên"))
    thongke_btn=CTkButton(left_frame,text="Thống Kê",width=200,height=60,image=CTkImage(Image.open("QuanLyChamCong/img/thongke.png"),size=(50,50)),anchor="w",command=lambda :EventButtonClick("Thống Kê"))
    chamcong_btn=CTkButton(left_frame,text="Lịch Chấm Công",width=200,height=60,image=CTkImage(Image.open("QuanLyChamCong/img/chamcong.png"),size=(50,50)),anchor="w",command=lambda :EventButtonClick("Lịch Chấm Công"))
    dangxuat_btn=CTkButton(left_frame,text="Đăng Xuất",width=200,height=60,image=CTkImage(Image.open("QuanLyChamCong/img/dangxuat.png"),size=(50,50)),anchor="w",command=lambda :EventButtonClick("Đăng Xuất"))
    dangky_btn.pack(pady=10,padx=20)
    qlnhanvien_btn.pack(pady=10,padx=20)
    thongke_btn.pack(pady=10,padx=20)
    chamcong_btn.pack(pady=10,padx=20)
    dangxuat_btn.pack(pady=100,padx=20)
    

    # Giao diện phải
    def giaoDienDangKy():
        # thông tin nhân viên + chụp hình + lưu
        for widget in right_frame.winfo_children():
            widget.destroy()
        right_frame.grid_propagate(False)
        DangKyGUI.DangKyLayout(right_frame)

    def giaoDienQuanly():
        right_frame.grid_propagate(False)
        for widget in right_frame.winfo_children():
            widget.destroy()

        QuanLyGUI.QuanLyLayout(right_frame)
    
    def giaoDienLichChamCong():
        right_frame.grid_propagate(False)
        for widget in right_frame.winfo_children():
            widget.destroy()
        LichChamCongGUI.LichChamCongLayout(right_frame)

    def giaoDienThongKe():
        right_frame.grid_propagate(False)
        for widget in right_frame.winfo_children():
            widget.destroy()
        ThongKeGUI.ThongKeLayout(right_frame)
        
    def on_closing():
        window.destroy()  # Đóng cửa sổ
        login_window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()


Login_Window()


