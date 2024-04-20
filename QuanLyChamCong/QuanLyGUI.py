import os
import re
from tkinter import *
from tkinter import messagebox, ttk
import database_manager
import numpy as np
from customtkinter import *
from PIL import Image, ImageTk
from tkcalendar import DateEntry


def QuanLyLayout(right_frame):

    center_frame = LabelFrame(right_frame, background="white", width=600, height=750)
    center_frame.grid(row=0,column=0,sticky="nsew")

    right_frame_qly = LabelFrame(right_frame, background='white', width=700, height=750)
    right_frame_qly.grid(row=0,column=1,sticky="nsew")

    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_columnconfigure(1, weight=2)
    right_frame.grid_rowconfigure(0, weight=1)

    timKiem_frame = Frame(right_frame_qly, background="white",width=700)
    timKiem_frame.pack(pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading",rowheight=50, font=("Arial", 14)) 
    style.configure("Treeview", rowheight=50)


    table_frame = Frame(right_frame_qly,width=700)
    table_frame.pack(fill="both", expand=True)

    tbscrolly = Scrollbar(table_frame)
    tbscrolly.pack(side=RIGHT, fill="y")

    table = ttk.Treeview(table_frame, yscrollcommand=tbscrolly,selectmode="extended", height=600) 
    table.pack()
    tbscrolly.config(command=table.yview)

    table['column'] = ("Mã nhân viên", "Họ tên", "Ngày sinh", "Số điện thoại", "Giới tính", "Chức vụ", "Email")
    table.column("#0", width=0, stretch=NO)
    table.column("Mã nhân viên", anchor=CENTER, width=140)
    table.column("Họ tên", anchor=CENTER, width=160)
    table.column("Ngày sinh", anchor=CENTER, width=120)
    table.column("Số điện thoại", anchor=CENTER, width=140)
    table.column("Giới tính", anchor=CENTER, width=100)
    table.column("Chức vụ", anchor=CENTER, width=100)
    table.column("Email", anchor=CENTER, width=150)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("Mã nhân viên", text="Mã nhân viên", anchor=CENTER)
    table.heading("Họ tên", text="Họ tên", anchor=W)
    table.heading("Ngày sinh", text="Ngày sinh", anchor=CENTER)
    table.heading("Số điện thoại", text="Số điện thoại", anchor=CENTER)
    table.heading("Giới tính", text="Giới tính", anchor=CENTER)
    table.heading("Chức vụ", text="Chức vụ", anchor=CENTER)
    table.heading("Email", text="Email", anchor=CENTER)

    table.tag_configure('evenrow', background="white")
    table.tag_configure('oddrow', background="lightblue")



    def select_record(e):
        text_manv.configure(state="normal")
        text_manv.delete(0, END)
        text_ten.delete(0, END)
        text_ngaysinh.delete(0, END)
        text_sdt.delete(0, END)
        text_email.delete(0, END)
        cb_chucvu.set(' ')
        cb_gioitinh.set(' ')

        selected = table.focus()
        values = table.item(selected, 'values')
        
        text_manv.insert(0, values[0])
        text_manv.configure(state="readonly")
        text_ten.insert(0, values[1])
        text_ngaysinh.insert(0, values[2])
        text_sdt.insert(0, values[3])
        text_email.insert(0, values[6])
        cb_gioitinh.set(values[4])
        cb_chucvu.set(values[5])

    def btnQuery():
        dbManager = database_manager.DatabaseManager()
        if dbManager.openConnection():
            nhanvien = dbManager.selectNhanVien()
            global count 
            count = 0
            for nv in nhanvien:
                if count % 2 == 0:
                    table.insert("", END, values=(nv[0], nv[1], nv[2], nv[3], nv[4], nv[5], nv[6]),
                             tags=('oddrow',))
                else:
                    table.insert("", END, values=(nv[0], nv[1], nv[2], nv[3], nv[4], nv[5], nv[6]),
                             tags=('evenrow',))
                count += 1
            dbManager.closeConnection()
        else:
            print("Kết nối thất bại!")

    btnQuery()
    table.bind("<ButtonRelease-1>", select_record)

    def btnTimKiem():
        table.delete(*table.get_children())
        dbManager = database_manager.DatabaseManager()
        if dbManager.openConnection():
            nhanvien = dbManager.selectNhanVien()
            tk = cb_timkiem.get()
            duLieu = text_timkiem.get().lower()
            for nv in nhanvien:
                if tk=="Mã nhân viên":
                    if duLieu in nv[0].lower():
                        table.insert("", END, values=(nv[0], nv[1], nv[2], nv[3], nv[4], nv[5], nv[6]),
                             tags=('evenrow',))
                elif tk=="Tên nhân viên":
                    if duLieu in nv[1].lower():
                        table.insert("", END, values=(nv[0], nv[1], nv[2], nv[3], nv[4], nv[5], nv[6]),
                             tags=('evenrow',))
                elif tk=="Chức vụ":
                    if duLieu in nv[5].lower():
                        table.insert("", END, values=(nv[0], nv[1], nv[2], nv[3], nv[4], nv[5], nv[6]),
                             tags=('evenrow',))
            dbManager.closeConnection()
        else:
            print("Kết nối thất bại!")
        btnLamMoi()  
    
    def btnXemTatCa():
        btnLamMoi()
        table.delete(*table.get_children())
        btnQuery()

    lb_timkiem = Label(timKiem_frame, text="Tìm kiếm theo:", font=("Helvetica", 15), foreground="red", background="white")
    lb_timkiem.grid(row=0, column=0, padx= 5, pady=10)
    value_timkiem = ["Mã nhân viên", "Tên nhân viên", "Chức vụ"]
    cb_timkiem = ttk.Combobox(timKiem_frame, values= value_timkiem, font=("Arial", 10))
    cb_timkiem.grid(row=0, column=1, padx=5, pady=10)
    text_timkiem = Entry(timKiem_frame)
    text_timkiem.grid(row=0, column=2, padx=5, pady=10)
    button_tk = CTkButton(timKiem_frame, text="Tìm kiếm", fg_color="white",text_color="black",border_color="#87CEFA",border_width=2,hover_color="#00BFFF",command=btnTimKiem)
    button_tk.grid(row=0, column=3, padx=5, pady=10)
    button_xemtatca = CTkButton(timKiem_frame, text="Xem tất cả", border_width=2,border_color="#87CEFA", text_color="white", hover_color="#00BFFF", command=btnXemTatCa)
    button_xemtatca.grid(row=0, column=4, pady=10)

# center_frame
    info_frame = Frame(center_frame, background="white",width=600)
    info_frame.pack()
    lb_info = CTkLabel(info_frame, text="Thông tin nhân viên", font=("Helvetica", 25),text_color="black")
    lb_info.grid(row=0, column=0,padx=5, pady=20, columnspan=2)

    lb_manv = CTkLabel(info_frame, text="Mã nhân viên", font=("Helvetica", 16),text_color="black")
    lb_manv.grid(row=1, column=0,padx=5, pady=10, stick="w")
    text_manv = CTkEntry(info_frame,state='readonly', font=("Helvetica", 15), width=160,corner_radius=20, text_color="black", border_width=2,fg_color="white")
    text_manv.grid(row=1, column=1, pady=10)

    lb_ten = CTkLabel(info_frame, text="Họ tên", font=("Helvetica", 16),text_color="black")
    lb_ten.grid(row=2, column=0,padx=5, pady=10, stick="w")
    text_ten = CTkEntry(info_frame, font=("Helvetica", 15), width=160, corner_radius=20, text_color="black", border_width=2,fg_color="white")
    text_ten.grid(row=2, column=1, pady=10)

    lb_ngaysinh = CTkLabel(info_frame, text="Ngày sinh", font=("Helvetica", 16),text_color="black")
    lb_ngaysinh.grid(row=3, column=0,padx=5, pady=10, stick="w")
    text_ngaysinh = DateEntry(info_frame, width=20, date_pattern='yyyy-mm-dd', font=("Helvetica", 10))
    text_ngaysinh.grid(row=3, column=1, pady=10)
    text_ngaysinh.delete(0, END)

    lb_sdt = CTkLabel(info_frame, text="Số điện thoại", font=("Helvetica", 16),text_color="black")
    lb_sdt.grid(row=4, column=0,padx=5, pady=10, stick="w")
    text_sdt = CTkEntry(info_frame, font=("Helvetica", 15), width=160, corner_radius=20, text_color="black", border_width=2,fg_color="white")
    text_sdt.grid(row=4, column=1, pady=10)

    lb_gioitinh = CTkLabel(info_frame, text="Giới tính", font=("Helvetica", 16),text_color="black")
    lb_gioitinh.grid(row=5, column=0,padx=5, pady=10, stick="w")
    values_gioitinh = ["Nam", "Nữ"]
    cb_gioitinh = ttk.Combobox(info_frame, values=values_gioitinh, font=("Helvetica", 10), width=20)
    cb_gioitinh.grid(row=5, column=1, pady=10)

    lb_chucvu = CTkLabel(info_frame, text="Chức vụ", font=("Helvetica", 16),text_color="black")
    lb_chucvu.grid(row=6, column=0,padx=5, pady=10, stick="w")
    values_chucvu = ["Quản lý", "Nhân viên", "Thực tập"]
    cb_chucvu = ttk.Combobox(info_frame, values=values_chucvu, font=("Helvetica", 10), width=20)
    cb_chucvu.grid(row=6, column=1, pady=10)

    lb_email = CTkLabel(info_frame, text="Email", font=("Helvetica", 16),text_color="black")
    lb_email.grid(row=7, column=0,padx=5, pady=10, stick="w")
    text_email = CTkEntry(info_frame, font=("Helvetica", 15), width=160, corner_radius=20, text_color="black", border_width=2,fg_color="white")
    text_email.grid(row=7, column=1, pady=10)

    def btnLamMoi():
        text_manv.configure(state="normal")
        text_manv.delete(0, END)
        text_ten.delete(0, END)
        text_ngaysinh.delete(0, END)
        text_sdt.delete(0, END)
        text_email.delete(0, END)
        cb_chucvu.set(' ')
        cb_gioitinh.set(' ')

    def ktraSdt(sdt):
        regex = r'^0\d{9}$'
        if(re.fullmatch(regex, sdt)):
            return TRUE
        else:
            return FALSE

    def ktraEmail(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(re.fullmatch(regex, email)):
            return TRUE
        else:
            return FALSE
            
    def btnCapNhat():
        selected = table.focus()
        table.item(selected, values=(text_manv.get()))
        manv = text_manv.get()
        ten = text_ten.get()
        ngaysinh = text_ngaysinh.get()
        sdt = text_sdt.get()
        gioitinh = cb_gioitinh.get()
        chucvu = cb_chucvu.get()
        email = text_email.get()
        if (selected=="" or manv==""):
            messagebox.showinfo("Thông báo", "Vui lòng chọn nhân viên!")
        else:
            if (ten=="" or ngaysinh=="" or sdt=="" or gioitinh=="" or chucvu=="" or email==""):
                messagebox.showinfo("Thông báo", "Vui lòng nhập đủ thông tin")
            else:
                if (ktraEmail(email)==FALSE or ktraSdt(sdt)==FALSE):
                    messagebox.showinfo("Thông báo", "Vui lòng nhập đúng định dạng")
                else:
                    dbManager = database_manager.DatabaseManager()
                    if dbManager.openConnection():
                        dbManager.updateNhanVien(manv, ten, ngaysinh, sdt, gioitinh, chucvu, email)
                        dbManager.closeConnection()
                    else:
                        print("Kết nối thất bại!")
                    btnLamMoi()
                    table.delete(*table.get_children())
                    btnQuery()
        
    def btnXoa():
        selected = table.focus()
        table.item(selected, text="", values=(text_manv.get()))
        manv = text_manv.get()
        if (selected=="" or manv==""):
            messagebox.showinfo("Thông báo", "Vui lòng chọn nhân viên!")
        else: 
            kq=messagebox.askyesno("Thông báo","Bạn chắc chắn muốn xóa chứ?")
            if(kq):
                dbManager = database_manager.DatabaseManager()
                if dbManager.openConnection():
                    dbManager.deleteNhanVien(manv)
                    dbManager.closeConnection()
                else:
                    print("Kết nối thất bại!")
                btnLamMoi()
        table.delete(*table.get_children())
        btnQuery()

    def btnXemAnh():
        selected = table.focus()
        table.item(selected, text="", values=(text_manv.get()))
        manv = text_manv.get()
        if (selected=="" or manv==""):
            messagebox.showinfo("Thông báo", "Vui lòng chọn nhân viên!")
        else: 
            dbManager = database_manager.DatabaseManager()
            if dbManager.openConnection():
                    nhanvien = dbManager.selectNhanVien()
                    for nv in nhanvien:
                        if manv in nv[0]:
                            folder_path = (f"C:/code/PythonWithConda/QuanLyChamCong/imgCheck/{manv}")
                            if os.path.exists(folder_path):
                                os.startfile(folder_path)
                            else: 
                                messagebox.showinfo("Thông báo", "Thư mục ảnh không tồn tại!")
                    dbManager.closeConnection()
            else:
                print("Kết nối thất bại!")
        table.delete(*table.get_children())
        btnQuery()

    #button
    button_capnhat = CTkButton(info_frame, text="Cập nhật", corner_radius=30, border_width=2,
                               border_color="#87CEFA", text_color="white", hover_color="#00BFFF", font=("Helvetica", 15), command=btnCapNhat )
    button_capnhat.grid(row=8, column=1)
    button_xoa = CTkButton(info_frame, text="Xoá", corner_radius=30, border_width=2,
                           border_color="#87CEFA", text_color="white", hover_color="#00BFFF", font=("Helvetica", 15), command=btnXoa)
    button_xoa.grid(row=8, column=0, padx=10, pady=30)

    button_lammoi = CTkButton(info_frame, text="Làm mới", corner_radius=30, border_width=2,
                               border_color="#87CEFA", text_color="white", hover_color="#00BFFF", font=("Helvetica", 15), command=btnLamMoi)
    button_lammoi.grid(row=9, column=0)
    button_xemanh = CTkButton(info_frame, text="Xem ảnh", corner_radius=30, border_width=2,
                              border_color="#87CEFA", text_color="white", hover_color="#00BFFF", font=("Helvetica", 15), command=btnXemAnh)
    button_xemanh.grid(row=9, column=1)
    
    


   