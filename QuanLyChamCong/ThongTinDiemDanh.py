from tkinter import *
from tkinter import ttk
from datetime import timedelta
from customtkinter import *
import numpy as np
import mysql.connector  
def loadDuLieu(table,listDiemDanh):
    for item in table.get_children():
        table.delete(item)
    dem=1
    for info in listDiemDanh:
        trangThai=""
        if(info[5] > timedelta(hours=7, minutes=30)):
            trangThai="Trễ"
        else: trangThai="Đúng Giờ"

        if(dem%2==0):
            table.insert("","end",iid=dem,text="",values=(info[0],info[1],info[2],info[3],info[4],info[5],info[6],trangThai),tags=('oddrow',))
        else:
            table.insert("","end",iid=dem,text="",values=(info[0],info[1],info[2],info[3],info[4],info[5],info[6],trangThai),tags=('evenrow',))
        dem+=1
def timKiemThongTin(table,listDiemDanh,text):
    kq=[]
    for noiDung in listDiemDanh:
        if( text in noiDung[0] or # mã kỳ công 
            text in noiDung[1] or # mã nhân viên
            text in noiDung[2] or # họ tên
            text in noiDung[3].strftime("%Y-%m-%d")):  # ngày
            kq.append(noiDung)
    loadDuLieu(table,kq)    
    pass



def ThongTinDiemDanhLayout(right_frame):
    # load dữ liệu
    DuLieuDiemDanh=LabelFrame(right_frame,background="white",height=700,width=1300)
    DuLieuDiemDanh.grid(row=0,column=0,sticky="nsew")
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=1)
    mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
    mycursor=mydatabase.cursor()
    mycursor.execute("SELECT * FROM congnhanvien")
    result=mycursor.fetchall()
    listDiemDanh=[]
    for info in (result):
        listDiemDanh.append(info)
    mycursor.close()
    chucNang=Frame(DuLieuDiemDanh,background="white",height=50,width=1300)
    chucNang.pack(fill="x",pady=10)

    timKiem=CTkEntry(chucNang,font=("arial",12),fg_color="white",text_color="black",placeholder_text="Tìm kiếm thông tin nhân viên ...",bg_color="white",width=600,height=50)
    timKiem.pack(side="left",padx=50) 
    style=ttk.Style()
    style.configure("Treeview.Heading",rowheight=50, font=("Arial", 14)) 
    style.configure("Treeview", rowheight=30,font=("Arial",14))

    table_frame = Frame(DuLieuDiemDanh,width=1300)
    table_frame.pack(fill="both", expand=True)

    tbscrolly = Scrollbar(table_frame,width=20)
    tbscrolly.pack(side=RIGHT, fill="y")  

    table = ttk.Treeview(table_frame, yscrollcommand=tbscrolly,height=50) 
    table.pack()
    tbscrolly.config(command=table.yview) 

    column=("MaKyCong","MaNV","HoTen","Ngay","Thu","ThoiGianVao","ThoiGianRa","DiTre")
    table['column']=column
    table.heading("#0",text="",anchor=W)
    table.heading("MaKyCong",text="Mã Kỳ Công",anchor=CENTER)
    table.heading("MaNV",text="Mã Nhân Viên",anchor=CENTER)
    table.heading("HoTen",text="Họ Và Tên",anchor=CENTER)
    table.heading("Ngay",text="Ngày",anchor=CENTER)
    table.heading("Thu",text="Thứ",anchor=CENTER)
    table.heading("ThoiGianVao",text="Thời Gian Vào",anchor=CENTER)
    table.heading("ThoiGianRa",text="Thời Gian Ra",anchor=CENTER)
    table.heading("DiTre",text="Đi Trễ",anchor=CENTER)
    table.column("#0",width=0,stretch=NO)
    table.tag_configure('evenrow', background="white")
    table.tag_configure('oddrow', background="lightblue")
    for i in column:
        table.column(i,width=150,anchor=CENTER)   
    table.column(2,width=250,anchor=CENTER)
    table.column(3,width=120,anchor=CENTER)
    table.column(4,width=120,anchor=CENTER)
    timKiem.bind("<KeyRelease>",lambda e: timKiemThongTin(table,listDiemDanh,timKiem.get()))
    dem=1
    for info in listDiemDanh:
        trangThai=""
        if(info[5] > timedelta(hours=7, minutes=30)):
            trangThai="Trễ"
        else: trangThai="Đúng Giờ"

        if(dem%2==0):
            table.insert("","end",iid=dem,text="",values=(info[0],info[1],info[2],info[3],info[4],info[5],info[6],trangThai),tags=('oddrow',))
        else:
            table.insert("","end",iid=dem,text="",values=(info[0],info[1],info[2],info[3],info[4],info[5],info[6],trangThai),tags=('evenrow',))
        dem+=1