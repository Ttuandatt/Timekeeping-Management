from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from customtkinter import *
import numpy as np
import database_manager


def btnTimKiemThoiGian():
    return


def on_focus_out(entry):
    if entry.get() == "":
        entry.insert(0, "dd/mm/yyyy")


def on_focus_in(entry):
    if entry.get() == "dd/mm/yyyy":
        entry.delete(0, "end")




def ThongKeLayout(right_frame):

    left_fr = LabelFrame(right_frame, width=400, height=700)
    left_fr.grid(row=0, column=0, sticky="nsew")

    right_fr = LabelFrame(right_frame, background="white", width=800, height=700)
    right_fr.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_columnconfigure(1, weight=2)
    right_frame.grid_rowconfigure(0, weight=1)

    overview_frame = Frame(left_fr, background="white", width=400)
    overview_frame.pack(fill="both",expand=True)
    lb_statistic = CTkLabel(overview_frame,text="Tổng quan thống kê:",font=("Helvetica", 35),text_color="black",)
    lb_statistic.grid(row=0, column=0, padx=5, pady=20, columnspan=2)

    lb_averageworkhour = CTkLabel(overview_frame,text="Số giờ công trung bình:",font=("Helvetica", 18),text_color="black",)
    lb_averageworkhour.grid(row=1, column=0, padx=5, pady=10, stick="w")
    lb_dataaverageworkhour = CTkLabel(overview_frame,text=str(giocongtrungbinh()) + "giờ",font=("Helvetica", 18),text_color="black",)
    lb_dataaverageworkhour.grid(row=1,column=1,padx=5,pady=10,)

    lb_totalworkhour = CTkLabel(overview_frame,text="Tổng số giờ công của tháng:",font=("Helvetica", 18),text_color="black",)
    lb_totalworkhour.grid(row=2, column=0, padx=5, pady=10, stick="w")
    lb_datatotalworkhour = CTkLabel(overview_frame,text=giocongthang(),font=("Helvetica", 18),text_color="black",)
    lb_datatotalworkhour.grid(row=2,column=1,padx=5,pady=10,)
    lb_totalovertimehour = CTkLabel(overview_frame,text="Tổng số giờ tăng ca:",font=("Helvetica", 18),text_color="black",)
    lb_totalovertimehour.grid(row=3, column=0, padx=5, pady=10, stick="w")
    lb_datatotalovertimehour = CTkLabel(overview_frame,text=str(giocongOT()) + " giờ",font=("Helvetica", 18),text_color="black",)
    lb_datatotalovertimehour.grid(row=3, column=1, padx=5, pady=10)

    lb_lateratio = CTkLabel(overview_frame,text="Tỉ lệ đi trễ của nhân viên:",font=("Helvetica", 18),text_color="black",)
    lb_lateratio.grid(row=4, column=0, padx=5, pady=10, stick="w")
    lb_datalateratio = CTkLabel(overview_frame,text=str(lateRate()) + " %",font=("Helvetica", 18),text_color="black",)
    lb_datalateratio.grid(row=4, column=1, padx=5, pady=10)
    lb_overtimeratio = CTkLabel(overview_frame,text="Tỉ lệ tăng ca của nhân viên:",font=("Helvetica", 18),text_color="black",)
    lb_overtimeratio.grid(row=5,column=0,padx=5,pady=10,stick="w",)
    lb_dataovertimeratio = CTkLabel(overview_frame,text=str(overtimeRate()) + " %",font=("Helvetica", 18),text_color="black",)
    lb_dataovertimeratio.grid(row=5, column=1, padx=5, pady=10)
    lb_dayoff = CTkLabel(overview_frame,text="Trung bình ngày công tháng:",font=("Helvetica", 18),text_color="black",)
    lb_dayoff.grid(row=6,column=0,padx=5,pady=10,stick="w",)
    lb_datadayoff = CTkLabel(overview_frame,text=str(averageWorkDay()) + " ngày",font=("Helvetica", 18),text_color="black",)
    lb_datadayoff.grid(row=6,column=1,padx=5,pady=10,)

    # Right frame
    thongkeoption_frame = LabelFrame(right_fr, background="white", width=800, height=200)
    thongkeoption_frame.pack(fill="both", expand=True)
    thongkecontent_frame = LabelFrame(right_fr, width=800, height=500)
    thongkecontent_frame.pack(fill="both", expand=True)

    lb_luachon = CTkLabel(thongkeoption_frame,text="Lựa chọn dữ liệu thống kê:",font=("Helvetica", 25),text_color="black",)
    lb_luachon.grid(row=0, column=0, padx=5, pady=10)
    
    value_luachon = ["1.Tổng giờ công","2.Giờ công ngoài giờ","3.Giờ công quản lý","4.Giờ công nhân viên",]
    cb_luachon = ttk.Combobox(thongkeoption_frame,values=value_luachon,font=("Arial",10,),state="readonly",)
    cb_luachon.current(0)
    cb_luachon.grid(row=0, column=1, padx=5, pady=10)

    text_thoigianbatdau = Entry(thongkeoption_frame)
    text_thoigianbatdau.insert(0, "dd/mm/yyyy")
    text_thoigianbatdau.bind("<FocusIn>", lambda x: on_focus_in(text_thoigianbatdau))
    text_thoigianbatdau.bind("<FocusOut>", lambda x: on_focus_out(text_thoigianbatdau))
    text_thoigianbatdau.grid(row=0, column=2, padx=5, pady=10)

    text_thoigianketthuc = Entry(thongkeoption_frame)
    text_thoigianketthuc.insert(0, "dd/mm/yyyy")
    text_thoigianketthuc.grid(row=0, column=3, padx=5, pady=10)
    text_thoigianketthuc.bind("<FocusIn>", lambda x: on_focus_in(text_thoigianketthuc))
    text_thoigianketthuc.bind("<FocusOut>", lambda x: on_focus_out(text_thoigianketthuc))
    button_timkiem = Button(thongkeoption_frame, text="Tìm kiếm", command=btnTimKiemThoiGian)
    button_timkiem.grid(row=0, column=4, padx=5, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", rowheight=50, font=("Arial", 14))
    style.configure("Treeview", rowheight=50)

    table_frame = Frame(thongkecontent_frame, width=800)
    tablescroll = Scrollbar(thongkecontent_frame)
    tablescroll.pack(side=RIGHT, fill="y")
    table_frame.pack(fill=BOTH, expand=True)

    table = ttk.Treeview(table_frame,selectmode="extended",height=600,)
    table.pack(side=LEFT, fill=BOTH, expand=True)
    tablescroll.config(command=table.yview)
    table["columns"] = ("STT","Mã chấm công","Mã nhân viên","Họ tên","Chức vụ","Giờ công",)

    table.column("#0", width=0, stretch=NO)
    table.column("STT", anchor=CENTER, width=70)
    table.column("Mã chấm công", anchor=CENTER, width=140)
    table.column("Mã nhân viên", anchor=CENTER, width=140)
    table.column("Họ tên", anchor=W, width=200)
    table.column("Chức vụ", anchor=CENTER, width=120)
    table.column("Giờ công", anchor=CENTER, width=120)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("STT", text="STT", anchor=CENTER)
    table.heading("Mã chấm công", text="Mã chấm công", anchor=CENTER)
    table.heading("Mã nhân viên", text="Mã nhân viên", anchor=CENTER)
    table.heading("Họ tên", text="Họ tên", anchor=CENTER)
    table.heading("Chức vụ", text="Chức vụ", anchor=CENTER)
    table.heading("Giờ công", text="Giờ công", anchor=CENTER)

    table.tag_configure("evenrow", background="white")
    table.tag_configure("oddrow", background="lightblue")
    hienThiMacDinh(table)
    cb_luachon.bind(
        "<<ComboboxSelected>>",
        lambda _: hienThiTheoDieuKien(
            text_thoigianbatdau, text_thoigianketthuc, cb_luachon, table
        ),
    )
    pass


def hienThiMacDinh(table):
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.selectInnerjoinNhanvienKyCong()
        global count
        count = 0
        for dl in dulieu:
            if dl[4] != None:
                giocong_hours = dl[4] / 3600
                giocong_hours = "{:.2f}".format(giocong_hours)
            else:
                giocong_hours = None
            if count % 2 == 0:

                table.insert(
                    "",
                    END,
                    values=(count, dl[0], dl[1], dl[2], dl[3], giocong_hours),
                    tags=("oddrow",),
                )
            else:

                table.insert(
                    "",
                    END,
                    values=(count, dl[0], dl[1], dl[2], dl[3], giocong_hours),
                    tags=("evenrow",),
                )
            count += 1
        dbManager.closeConnection()
    else:
        print("Kết nối thất bại!")


def giocongtrungbinh():
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.countNhanVien()
        print("Kết quả count:")
        print(dulieu)
        if dulieu != None:
            total_employee = dulieu[0][0]
        else:
            total_employee = 0
        dulieu = dbManager.sumWorkHour()
        if dulieu != None:
            worksecond = dulieu[0][0]
            if worksecond is not None:
                workhours = worksecond / 3600
            else:
                workhours = 0
        else:
            workhours = None
        return round(workhours / total_employee,2)

    else:
        print("Kết nối thất bại!")

    return None

def lateRate():
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.lateRate()
        if dulieu is not None:
            late = dulieu[0][0]
        else:
            late = None
        return late
    else:
        return None

def giocongOT():
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.sumOvertimeWorkHour()
        if dulieu is not None and dulieu[0][0] is not None: # Kiểm tra dulieu và dulieu[0][0] không phải là None
            time_data = str(dulieu[0][0])
            print("Từ OT")
            print(time_data)
            try:
                time_data = datetime.strptime(time_data, "%H:%M:%S")
                total_overtime_hours = (
                    time_data.hour + (time_data.minute / 60) + (time_data.second / 3600)
                )
            except ValueError as e:
                print(f"Lỗi khi chuyển đổi giá trị {time_data}: {e}")
                total_overtime_hours = 0
        else:
            total_overtime_hours = 0
        return round(total_overtime_hours, 2)
    else:
        return None


def averageWorkDay():
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.averageWorkDay()
        if dulieu is not None:
            average = dulieu[0][0]
            average = round(average, 0)
        else:
            average = None
        return average
    else:
        return None


def giocongthang():
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.sumWorkHourCurrentMonth()
        if dulieu is not None:
            worksecond = dulieu[0][0]
            if worksecond is None:
                worksecond = 0
            workhours = worksecond / 3600
        else:
            workhours = None
        return round(workhours,2)
    else:
        print("Kết nối thất bại!")
        return None


def overtimeRate():
    dbManager = database_manager.DatabaseManager()
    if dbManager.openConnection():
        dulieu = dbManager.overtimeRate()
        if dulieu is not None:
            overtime = dulieu[0][0]
        else:
            overtime = None
        return overtime
    else:
        return None


def hienThiTheoDieuKien(eStart, eEnd, cb, table):
    table.delete(*table.get_children())
    dbManager = database_manager.DatabaseManager()
    dulieu = None
    if (eStart.get() != ""and eStart.get() != "dd/mm/yyyy"and eEnd.get() != ""and eEnd.get() != "dd/mm/yyyy"):
        if dbManager.openConnection():
            dulieu = dbManager.selectTheoKhoangThoiGian(
                eStart.get(), eEnd.get(), int(cb.get()[0])
            )
    else:
        if dbManager.openConnection():
            dulieu = dbManager.selectMacDinh(int(cb.get()[0]))

    if dulieu != None:
        global count
        count = 0
        for dl in dulieu:
            if dl[4] != None:

                time_str = str(dl[4])
                tmp_h=int(time_str)//3600
                tmp_m=(int(time_str)%3600)//60
                tmp_s=int(time_str)%60
                time_str = "{:02d}:{:02d}:{:02d}".format(tmp_h, tmp_m, tmp_s)
                time_delta = time_delta = datetime.strptime(time_str, "%H:%M:%S") - datetime(1900, 1, 1)
                # Calculate total seconds
                total_seconds = time_delta.total_seconds()
                # Convert seconds to hours
                hours = total_seconds / 3600
                hours = "{:.2f}".format(hours)
            # giocong_
            else:
                hours = None
            if count % 2 == 0:

                table.insert(
                    "",
                    END,
                    values=(count, dl[0], dl[1], dl[2], dl[3], hours),
                    tags=("oddrow",),
                )
            else:

                table.insert(
                    "",
                    END,
                    values=(count, dl[0], dl[1], dl[2], dl[3], hours),
                    tags=("evenrow",),
                )
            count += 1
        dbManager.closeConnection()
    else:
        print("Kết nối thất bại!")
