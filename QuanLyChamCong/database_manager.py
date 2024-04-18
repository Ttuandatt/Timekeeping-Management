from tkinter import messagebox
import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.dbUrl = "localhost"
        self.username = "root"
        self.password = "dora1808"
        self.con = None

    # Hàm thiết lập kết nối với database. Trả về True nếu thành công, False nếu thất bại.
    def openConnection(self):
        try:
            self.con = mysql.connector.connect(
                host=self.dbUrl,
                user=self.username,
                password=self.password,
                database="qlchamcong"
            )
            return True
        except Exception as e:
            print(e)
            return False

    # Hàm đóng kết nối với database.
    def closeConnection(self):
        try:
            if self.con is not None:
                self.con.close()
        except Exception as e:
            print(e)

    # Thực hiện truy vấn SELECT * FROM nhanvien và trả về kết quả
    def selectAllNhanVien(self):

        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM `nhanvien`")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(e)
            return None

    def insertNhanVien(self, ma_nv, ho_ten, ngay_sinh, so_dien_thoai, gioi_tinh, chuc_vu, email):
        try:
            cursor = self.con.cursor()
            query = "INSERT INTO `nhanvien` (MaNV, HoTen, NgaySinh, SoDienThoai, GioiTinh, ChucVu, Email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (ma_nv, ho_ten, ngay_sinh, so_dien_thoai, gioi_tinh, chuc_vu, email)
            cursor.execute(query, values)
            self.con.commit()
            cursor.close()
            messagebox.showinfo("Thông báo", "Thêm nhân viên thành công")
        except Exception as e:
            messagebox.showinfo("Thông báo", "Thêm nhân viên thất bại")

    def updateNhanVien(self, manv, hoten, ngaysinh, sdt, gioitinh, chucvu, email):
        try:
            cursor = self.con.cursor()
            update_query = "UPDATE `nhanvien` SET `HoTen`=%s, `NgaySinh`=%s, `SoDienThoai`=%s, `GioiTinh`=%s, `ChucVu`=%s, `Email`=%s WHERE `MaNV`=%s"
            values = (manv, hoten, ngaysinh, sdt, gioitinh, chucvu, email)
            cursor.execute(update_query, values)
            self.con.commit()
            self.con.close()
            messagebox.showinfo("Thông báo", "Cập nhật thành công")
        except Exception as e:
            messagebox.showinfo("Thông báo", "Cập nhật thất bại")

# Sử dụng:
db_manager = DatabaseManager()
if db_manager.openConnection():
    print("Kết nối thành công!")
    # Thực hiện truy vấn SELECT * FROM nhanvien
    nhanvien = db_manager.selectAllNhanVien()
    if nhanvien:
        for nv in nhanvien:
            print(nv)
    db_manager.closeConnection()
else:
    print("Kết nối thất bại!")
