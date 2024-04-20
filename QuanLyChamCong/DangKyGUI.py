from tkinter import *
from tkinter import ttk, Label
from tkinter import messagebox
from PIL import ImageTk, Image
from customtkinter import *
import face_recognition, cv2
import numpy as np
import mysql.connector
import database_manager
from database_manager import nhanvien
import random
from datetime import datetime
import re  # Thêm import biểu thức chính quy để kiểm tra syntax của dữ liệu nhập vào
import os

# Tạo biến toàn cục để lưu trữ mã nhân viên
ma_nv_global = ""
def DangKyLayout(right_frame):
        left_frame_dk = Frame(right_frame, bg="white",width=500,height=800)
        right_frame_dk = Frame(right_frame, bg="white",width=700,height=800)
        left_frame_dk.grid(row=0,column=0,sticky="nsew")

        right_frame_dk.grid(row=0,column=1,sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        def showHinhAnh():
            count = 0   # Biến đếm để chỉ lưu vào database 1 lần đối với 1 nhân viên, nếu không sẽ bị lỗi do lưu mã nhân viên đã có
            cap = cv2.VideoCapture(0)
            dem = 0
            folderName=text_manv.get()
            os.makedirs(f"C:/Users/ACER/Dropbox/My PC (LAPTOP-UGP9QJUT)/Documents/ITstudies/Python-main/QuanLyChamCong/imgCheck/{folderName}")
            while True:
                ret, frame = cap.read()
                frame = cv2.resize(frame, (350, 350))
                img = cv2.flip(frame, 1)
                img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img3 = ImageTk.PhotoImage(Image.fromarray(img1))
                if count == 0:
                    if len(face_recognition.face_encodings(img1)) > 0:
                        img_name = f"{text_manv.get()}{dem}.png"
                        cv2.imwrite(f"C:/Users/ACER/Dropbox/My PC (LAPTOP-UGP9QJUT)/Documents/ITstudies/Python-main/QuanLyChamCong/imgCheck/{folderName}/{img_name}",frame)
                        dem += 1
                        print("được")
                        # Lưu thông tin nhân viên vào cơ sở dữ liệu
                        luuThongTinNhanVien(img_name)
                        count += 1
                    label_hinhAnh.configure(image=img3, width=360, height=360)
                    right_frame_dk.update()
                    if (dem == 10):
                        break
                else:
                    if len(face_recognition.face_encodings(img1)) > 0:
                        img_name = f"{text_manv.get()}{dem}.png"
                        cv2.imwrite(
                            f"C:/Users/ACER/Dropbox/My PC (LAPTOP-UGP9QJUT)/Documents/ITstudies/Python-main/QuanLyChamCong/imgCheck/{folderName}/{img_name}",
                            frame)
                        dem += 1
                        print("được")
                        # Lưu thông tin nhân viên vào cơ sở dữ liệu
                        count += 1
                    label_hinhAnh.configure(image=img3, width=360, height=360)
                    right_frame_dk.update()
                    if (dem == 10):
                        break

            cap.release()
            cv2.destroyAllWindows()
            img =  Image.open(f"C:/Users/ACER/Dropbox/My PC (LAPTOP-UGP9QJUT)/Documents/ITstudies/Python-main/QuanLyChamCong/imgCheck/{folderName}/{folderName}0.png")
            anhNV = ImageTk.PhotoImage(img)




        # left_frame_dk chứa các thành phần để nhập thông tin nhân viên
        label_ten = Label(left_frame_dk, text="Họ Tên", font=("Arial", 15), background="white")
        label_ten.grid(row=0, column=0, pady=30, padx=50, sticky="w")
        text_ten = Entry(left_frame_dk, font=("Arial", 15), background="white", borderwidth=3)
        text_ten.grid(row=0, column=1)
        label_ngaysinh = Label(left_frame_dk, text="Ngày Sinh: ", font=("Arial", 15), background="white")
        label_ngaysinh.grid(row=1,column=0, pady=30, padx=50, sticky="w")
        text_ngaysinh = Entry(left_frame_dk, font=("Arial", 15), background="white", borderwidth=3)
        text_ngaysinh.grid(row=1,column=1)
        label_sdt = Label(left_frame_dk, text="Số Điện Thoại: ", font=("Arial", 15), background="white")
        label_sdt.grid(row=2, column=0, pady=30, padx=50, sticky="w")
        text_sdt = Entry(left_frame_dk, font=("Arial", 15), background="white", borderwidth=3)
        text_sdt.grid(row=2, column=1)
        label_gioitinh = Label(left_frame_dk, text="Giới Tính: ", font=("Arial", 15), background="white")
        label_gioitinh.grid(row=3,column=0, pady=30, padx=50, sticky="w")
        value_gioitinh = ["Nam", "Nữ"]
        combobox_gioitinh = ttk.Combobox(left_frame_dk, values=value_gioitinh, font=("Arial", 15), background="white", state="readonly")
        combobox_gioitinh["width"] = 19
        combobox_gioitinh.grid(row=3, column=1)
        label_chucvu = Label(left_frame_dk, text="Chức Vụ: ", font=("Arial", 15), background="white")
        label_chucvu.grid(row=4,column=0, pady=30, padx=50, sticky="w")
        value_chucvu = ["Quản lý", "Nhân viên", "Thực tập"]
        combobox_chucvu = ttk.Combobox(left_frame_dk, values=value_chucvu, font=("Arial", 15), background="white", state="readonly")
        combobox_chucvu["width"] = 19
        combobox_chucvu.grid(row=4, column=1)
        label_email = Label(left_frame_dk, text="Email: ", font=("Arial", 15), background="white")
        label_email.grid(row=5, column=0, pady=30, padx=50, sticky="w")
        text_email = Entry(left_frame_dk, font=("Arial", 15), background="white", borderwidth=3)
        text_email.grid(row=5, column=1)
        label_manv = Label(left_frame_dk, text="Mã NV: ", font=("Arial", 15), background="white")
        label_manv.grid(row=6, column=0, pady=30, padx=50, sticky="w")
        text_manv = Entry(left_frame_dk, font=("Arial", 15), background="white", borderwidth=3, state="readonly")
        text_manv.grid(row=6, column=1)



        def luuThongTinNhanVien(img_name):
            ho_ten = text_ten.get()
            ngay_sinh_str = text_ngaysinh.get()  # Lấy chuỗi ngày sinh từ entry
            ngay_sinh = datetime.strptime(ngay_sinh_str, "%d/%m/%Y")  # Chuyển đổi sang đối tượng datetime
            ngay_sinh_formatted = ngay_sinh.strftime("%Y-%m-%d")  # Chuyển đổi định dạng ngày tháng

            so_dien_thoai = text_sdt.get()
            gioi_tinh = combobox_gioitinh.get()
            chuc_vu = combobox_chucvu.get()
            email = text_email.get()


            # Kết nối đến cơ sở dữ liệu
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="qlchamcong"
            )
            cursor = connection.cursor()

            # Thực hiện chèn dữ liệu vào cơ sở dữ liệu
            sql = "INSERT INTO NhanVien (`MaNV`, `HoTen`, `NgaySinh`, `SoDienThoai`, `GioiTinh`, `ChucVu`, `Email`, `HinhAnh`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (ma_nv_global, ho_ten, ngay_sinh_formatted, so_dien_thoai, gioi_tinh, chuc_vu, email, img_name)
            cursor.execute(sql, val)

            connection.commit()

            # Đóng kết nối với cơ sở dữ liệu
            cursor.close()
            connection.close()


        def taoMaNhanVien(chuc_vu, so_dien_thoai, gioi_tinh):
            global ma_nv_global  # Sử dụng biến toàn cục

            gender = ""
            if gioi_tinh == "Nam":
                gender = "M"
            elif gioi_tinh == "Nữ":
                gender = "F"
            if chuc_vu == "Quản lý":
                # Kiểm tra nếu mã nhân viên chưa được tạo hoặc là lần đầu tiên
                if not ma_nv_global:
                    ma_nv_global = "NV" + so_dien_thoai[-4:] + gender + str(random.randint(0, 9999)).zfill(4) + "0"
            if chuc_vu == "Nhân viên":
                # Kiểm tra nếu mã nhân viên chưa được tạo hoặc là lần đầu tiên
                if not ma_nv_global:
                    ma_nv_global = "NV" + so_dien_thoai[-4:] + gender + str(random.randint(0, 9999)).zfill(4) + "1"
            if chuc_vu == "Thực tập":
                # Kiểm tra nếu mã nhân viên chưa được tạo hoặc là lần đầu tiên
                if not ma_nv_global:
                    ma_nv_global = "NV" + so_dien_thoai[-4:] + gender + str(random.randint(0, 9999)).zfill(4) + "2"
            return ma_nv_global

        def check_sdt(sdt):
            result = 0
            # Kiểm tra độ dài của số điện thoại
            if len(sdt)  != 10:
                result = 1
            # Kiểm tra số điện thoại có chứa ký tự không phải là số hay không
            if not re.match(r'^\d+$', sdt):
                result = 2

            # Kiểm tra số điện thoại đã tồn tại trong cơ sở dữ liệu hay chưa
            connection = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "123456",
                database = "qlchamcong"
            )
            cursor = connection.cursor()

            # Truy vấn để kiểm tra số điện thoại trong cơ sở dữ liệu
            query = "SELECT COUNT(*) FROM NhanVien WHERE SoDienThoai = %s"
            cursor.execute(query, (sdt,))
            # Lấy kết quả truy vấn
            count = cursor.fetchone()[0]
            # Đóng kết nối với cơ sở dữ liệu
            cursor.close()
            connection.close()
            # Nếu số điện thoại đã tồn tại
            if count > 0:
                return 3  # Số điện thoại đã tồn tại
            return result

        def check_ngaysinh(ngay_sinh):
            # Biểu thức chính quy để kiểm tra định dạng ngày tháng dd/mm/yyyy
            regex = re.compile(r'^\d{2}/\d{2}/\d{4}$')

            # Kiểm tra định dạng của ngày sinh
            if not regex.match(ngay_sinh):
                return 1  # Định dạng ngày sinh không đúng

            # Tách ngày, tháng, năm từ chuỗi ngày sinh
            day, month, year = map(int, ngay_sinh.split('/'))

            # Kiểm tra năm nhuận
            def is_leap_year(year):
                if year % 4 == 0:
                    if year % 100 == 0:
                        if year % 400 == 0:
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    return False

            # Số ngày trong tháng tương ứng
            days_in_month = {
                1: 31, 2: 29 if is_leap_year(year) else 28,
                3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31,
                11: 30, 12: 31
            }

            # Kiểm tra ngày tháng năm có hợp lệ không
            if month not in days_in_month:
                return 2  # Tháng không hợp lệ
            if day < 1 or day > days_in_month[month]:
                return 3  # Ngày không hợp lệ

            return 0

        # Hàm kiểm tra thông tin trước khi cho phép chụp ảnh
        def check_full_information(hoten, ngaysinh, sdt, gioitinh, chucvu, email):
            if len(hoten) == 0 or len(ngaysinh) == 0 or len(sdt) == 0 or len(gioitinh) == 0 or len(chucvu) == 0 or len(email) == 0:
                return 1
            return 0
        def button_chupanh():
            ho_ten = text_ten.get()
            ngay_sinh = text_ngaysinh.get()
            so_dien_thoai = text_sdt.get()
            gioi_tinh = combobox_gioitinh.get()
            chuc_vu = combobox_chucvu.get()
            email = text_email.get()

            if len(ho_ten) == 0 or len(ngay_sinh) == 0 or len(so_dien_thoai) == 0 or len(gioi_tinh) == 0 or len(chuc_vu) == 0 or len(email) == 0:
                messagebox.showinfo("Thông báo", "Vui lòng nhập đủ thông tin trước khi chụp ảnh")
            else:
                showHinhAnh()
        # Hàm clear các textfield, combobox
        def button_clear():
            text_ten.delete(0, END)
            text_ngaysinh.delete(0, END)
            text_sdt.delete(0, END)
            text_email.delete(0, END)
            global ma_nv_global  # Sử dụng biến toàn cục
            ma_nv_global = ""  # Xóa mã nhân viên để tạo lại khi nhấn nút làm mới
            text_manv.config(state="normal")
            text_manv.delete(0, END)
            text_manv.config(state="readonly")
            combobox_chucvu.set('')
            combobox_gioitinh.set('')

        # hàm xử lý sự kiện lấy data từ textfield, combobox để đưa vào database
        def button_XacNhan():
            ho_ten = text_ten.get()
            ngay_sinh = text_ngaysinh.get()
            so_dien_thoai = text_sdt.get()
            gioi_tinh = combobox_gioitinh.get()
            chuc_vu = combobox_chucvu.get()
            email = text_email.get()

            if len(ho_ten) == 0 or len(ngay_sinh) == 0 or len(so_dien_thoai) == 0 or len(gioi_tinh) == 0 or len(chuc_vu) == 0 or len(email) == 0:
                messagebox.showinfo("Thông báo", "Vui lòng nhập đủ thông tin")

            elif check_sdt(so_dien_thoai) == 0 and check_ngaysinh(ngay_sinh) == 0:
                # Tạo mã nhân viên
                ma_nv_global = taoMaNhanVien(chuc_vu, so_dien_thoai, gioi_tinh)
                text_manv.config(state="normal")
                text_manv.delete(0, END)
                text_manv.insert(0, ma_nv_global)
                text_manv.config(state="readonly")
            elif check_sdt(so_dien_thoai) == 1:
                messagebox.showinfo("Thông báo", "Vui lòng nhập đủ 10 số")
            elif check_sdt(so_dien_thoai) == 2:
                messagebox.showinfo("Thông báo", "Số điện thoại chỉ chứa số")
            elif check_sdt(so_dien_thoai) == 3:
                messagebox.showinfo("Thông báo", "Số điện thoại đã tồn tại")
            elif check_ngaysinh(ngay_sinh) == 1:
                messagebox.showinfo("Thông báo", "Vui lòng nhập đúng định dạng dd/mm/yyyy")
            elif check_ngaysinh(ngay_sinh) == 2:
                messagebox.showinfo("Thông báo", "Tháng không hợp lệ")
            elif check_ngaysinh(ngay_sinh) == 3:
                messagebox.showinfo("Thông báo", "Ngày không hợp lệ")
            elif check_ngaysinh(ngay_sinh) == 2 and check_ngaysinh(ngay_sinh) == 3:
                messagebox.showinfo("Thông báo", "Ngày tháng không hợp lệ")

        # nhập tên, chụp ảnh
        label_Khung = LabelFrame(right_frame_dk, bg="white", borderwidth=5)
        label_Khung.pack(pady=29)
        label_hinhAnh = Label(label_Khung, bg="light gray", text="", width=50, height=30)
        label_hinhAnh.pack()
        btn_dangky = CTkButton(right_frame_dk, text="Chụp Ảnh", width=100, height=50, command=button_chupanh)
        btn_dangky.pack()

        button_lammoi = CTkButton(left_frame_dk, text="Làm Mới", width=100, height=50, command=button_clear)
        button_lammoi.grid(row=7, column=0)
        button_xacnhan = CTkButton(left_frame_dk, text="Xác Nhận", width=100, height=50, command=button_XacNhan)
        button_xacnhan.grid(row=7, column=1)
