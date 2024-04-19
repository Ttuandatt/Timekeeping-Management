from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from customtkinter import *
import numpy as np
import calendar
import mysql.connector  
def canGiuaCuaSo(window,width,height):
    window.resizable(width=False,height=False)
    screen_width=window.winfo_screenwidth()
    screen_height=window.winfo_screenheight()
    x=(screen_width-width)//2
    y=(screen_height-height)//2
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
def loadDuLieuGoc(my_tree):
    for item in my_tree.get_children():
        my_tree.delete(item)
    mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
    mycursor=mydatabase.cursor()
    mycursor.execute("SELECT * FROM kycong")
    result=mycursor.fetchall()
    dem=1
    for info in (result):
        if( info[5]==0):
            if(dem%2==0):
                my_tree.insert("","end",iid=dem,text="",values=(dem,info[0],info[1],info[2],info[3],info[4],"Còn Hoạt Động"),tags=('oddrow',))
            else:
                my_tree.insert("","end",iid=dem,text="",values=(dem,info[0],info[1],info[2],info[3],info[4],"Còn Hoạt Động"),tags=('evenrow',))
            dem+=1
    mycursor.close()

def loadDuLieu(my_tree,listKyCong):
    # làm sạch nội dung trước khi chèn nội dung
    for item in my_tree.get_children():
        my_tree.delete(item)

    dem=1
    for info in (listKyCong):
        if( info[5]==0):
            if(dem%2==0):
                my_tree.insert("","end",iid=dem,text="",values=(dem,info[0],info[1],info[2],info[3],info[4],"Còn Hoạt Động"),tags=('oddrow',))
            else:
                my_tree.insert("","end",iid=dem,text="",values=(dem,info[0],info[1],info[2],info[3],info[4],"Còn Hoạt Động"),tags=('evenrow',))
            dem+=1
def timKiemKyCong(my_tree,listKyCong,text):
    kq=[]
    for tmp in listKyCong:
        if(text in tmp[0]): # tìm kiếm theo mã sp
            kq.append(tmp)
    loadDuLieu(my_tree,kq)
def KyCongChiTietChoNhanVien(MaKC):
    mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
    mycursor=mydatabase.cursor()
    sql = """Select * From nhanvien as nv
            Where NOT EXISTS ( Select 1 From kycongchitiet AS kc Where kc.MaNV = nv.MaNV and kc.MaKyCong=%s)"""
    mycursor.execute(sql,(MaKC,))
    result=mycursor.fetchall()
    for nv in result:
        values=(MaKC,nv[0],nv[1])
        sql="""Insert into kycongchitiet(MaKyCong, MaNV, HoTen) VALUES(%s, %s, %s)"""
        mycursor.execute(sql,values)
    mydatabase.commit()
    mycursor.close()
def themKyCong(right_frame,my_tree):
    popUp_add=Toplevel(right_frame)
    canGiuaCuaSo(popUp_add,500,400)
    popUp_add.title("Thêm kì công")
    

    thang=list(range(1, 13))
    ngay=list(range(1,32))
    label_Thang=Label(popUp_add,text="Tháng: ",font=("Arial",14))
    label_Nam=Label(popUp_add,text="Năm: ",font=("Arial",14))
    label_NgayTinhCong=Label(popUp_add,text="Ngày Tính Công: ",font=("Arial",14))
    entry_Thang=ttk.Combobox(popUp_add,value=thang,font=("Arial",14))
    entry_Nam=Entry(popUp_add,width=21,font=("Arial",14))
    entry_NgayTinhCong=ttk.Combobox(popUp_add,value=ngay,font=("Arial",14))
    label_Thang.grid(row=0,column=0,padx=10,pady=30,sticky="w")
    entry_Thang.grid(row=0,column=1,padx=20,pady=30,sticky="w")
    label_Nam.grid(row=1,column=0,padx=10,pady=30,sticky="w")
    entry_Nam.grid(row=1,column=1,padx=20,pady=30,sticky="w")
    label_NgayTinhCong.grid(row=2,column=0,padx=10,pady=30,sticky="w")
    entry_NgayTinhCong.grid(row=2,column=1,padx=20,pady=30,sticky="w")
    entry_Thang.current(0)
    entry_Nam.insert(0,datetime.now().year)
    entry_NgayTinhCong.current(0)
    def KtratonTai(maKC):
        mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
        mycursor=mydatabase.cursor()
        sql="Select * from kycong Where MaKyCong=%s"
        mycursor.execute(sql,(maKC,))
        kq=mycursor.fetchall()
        if kq:
            return True
        return False


    def KyCongMoi():
        mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
        mycursor=mydatabase.cursor()
        sql="""Insert into kycong(MaKyCong, Thang, Nam, NgayTinhCong, SoNgayCong,TrangThai) 
                Values (%s, %s, %s, %s, %s, %s)
        """
        thang = entry_Thang.get()
        if len(thang) == 1:
            thang = "0" + thang
        maKC="KC"+thang+entry_Nam.get()
        thang=int(entry_Thang.get())
        nam=int(entry_Nam.get())
        ngayTC=datetime(nam, thang, int(entry_NgayTinhCong.get()))
        ngayTC=ngayTC.strftime("%Y-%m-%d")
        SoNgayCong = calendar.monthrange(nam, thang)[1]-int(entry_NgayTinhCong.get())+1
        if(KtratonTai(maKC)==False):
            values=(maKC,str(thang),str(nam),ngayTC,SoNgayCong,0)
            mycursor.execute(sql,values)
            mydatabase.commit()
            mycursor.close()
            messagebox.showinfo("Thông báo","Thêm kỳ công mới thành công")
            KyCongChiTietChoNhanVien(maKC)
            loadDuLieuGoc(my_tree)
            popUp_add.destroy()
        else:
            messagebox.showinfo("Thông báo","Kỳ Công này đã tồn tại trong dữ liệu !!!")


    btn_Them=CTkButton(popUp_add,text="Thêm",fg_color="#4158D0",text_color="white",width=200,height=50,corner_radius=32,command=KyCongMoi)
    btn_Them.grid(row=3,column=0,columnspan=2,pady=50)

def xoaKyCong(my_tree):
    selection = my_tree.selection()
    kycong=my_tree.item(selection[0],'values')
    kq=messagebox.askyesno("Thông báo","Bạn chắc chắn muốn xóa chứ ?")
    if(kq):
        mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
        mycursor=mydatabase.cursor()
        sql="Update kycong Set TrangThai=%s Where MaKyCong=%s"
        mycursor.execute(sql,('1',kycong[1]))
        mydatabase.commit()
        loadDuLieuGoc(my_tree)
        mycursor.close()



def LichChamCongLayout(right_frame):
    # chia làm 2 là chức năng + tìm kiếm ở trên, table ở dưới
    ChucNangChamCong=Frame(right_frame,background="white",height=150,width=1300)
    DuLieuChamCong=Frame(right_frame,background="white",height=600,width=1300)
    ChucNangChamCong.grid(row=0,column=0,sticky="nsew")
    DuLieuChamCong.grid(row=1,column=0,sticky="nsew")
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_rowconfigure(1, weight=2)
    # load dữ liệu
    mydatabase=mysql.connector.connect(user='root',password='dora1808',host='localhost',database="qlchamcong")
    mycursor=mydatabase.cursor()
    mycursor.execute("SELECT * FROM kycong")
    result=mycursor.fetchall()
    listKyCong=[]
    for info in (result):
        listKyCong.append(info)
    mycursor.close()

    # chức năng
    timKiem=CTkEntry(ChucNangChamCong,font=("arial",12),fg_color="white",text_color="black",placeholder_text="Tìm kiếm mã kì công",bg_color="white",width=600,height=50)
    timKiem.pack(padx=10,pady=20,side="left")
    

    btn_ThemKyCong=CTkButton(ChucNangChamCong,text="Kì Công Mới",font=("Arial", 14),fg_color="#4158D0",text_color="white",width=150,height=50,border_width=2,command=lambda: themKyCong(right_frame,my_tree))
    btn_XoaKyCong=CTkButton(ChucNangChamCong,text="Xóa",font=("Arial", 14),fg_color="white",text_color="#FE6D73",width=100,height=50,border_width=2,command=lambda: xoaKyCong(my_tree))
    btn_XoaKyCong.pack(padx=10,pady=20,side="right")
    btn_ThemKyCong.pack(padx=10,pady=20,side="right")


    # TreeView dùng để hiển thị dữ liệu bản 
    style=ttk.Style()
    style.configure("Treeview.Heading",rowheight=50, font=("Arial", 14)) 
    style.configure("Treeview", rowheight=50,font=("Arial",14))
    tree_frame=Frame(DuLieuChamCong)
    tree_frame.pack()
    my_tree=ttk.Treeview(tree_frame) 
    my_tree.grid(row=0,column=0)

    column=("STT","MaKyCong","Thang","Nam","ngayTinhCong","SoNgayCong","TrangThai")
    my_tree['columns']=column
    my_tree.heading("#0",text="",anchor=W)
    my_tree.heading("STT",text="STT",anchor=CENTER)
    my_tree.heading("MaKyCong",text="Mã Kỳ Công",anchor=CENTER)
    my_tree.heading("Thang",text="Tháng",anchor=CENTER)
    my_tree.heading("Nam",text="Năm",anchor=CENTER)
    my_tree.heading("ngayTinhCong",text="Ngày Tính công",anchor=CENTER)
    my_tree.heading("SoNgayCong",text="Số Ngày Công",anchor=CENTER)
    my_tree.heading("TrangThai",text="Trạng Thái",anchor=CENTER)
    my_tree.column("#0",width=0,stretch=NO)
    my_tree.tag_configure('evenrow', background="white")
    my_tree.tag_configure('oddrow', background="lightblue")
    for i in column:
        my_tree.column(i,width=200,anchor=CENTER)
    my_tree.column("STT",anchor=CENTER,width=60)
    loadDuLieu(my_tree,listKyCong)

    timKiem.bind("<KeyRelease>",lambda e: timKiemKyCong(my_tree,listKyCong,timKiem.get()))
