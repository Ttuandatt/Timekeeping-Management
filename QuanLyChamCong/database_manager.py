from tkinter import messagebox
from datetime import datetime
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
                database="qlchamcong",
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

    def selectNhanVien(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM NhanVien WHERE `TrangThai`=1")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(e)
            return None

    def selectAllNhanVien(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM NhanVien")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(e)
            return None

    def selectKyCongChiTiet(self, manv, makc):
        try:
            cursor = self.con.cursor()
            query = "SELECT * FROM `KyCongChiTiet` WHERE `MaNV`=%s and `MaKyCong`=%s"
            cursor.execute(query, (manv, makc))
            kq = cursor.fetchall()
            cursor.close()
            return kq
        except Exception as e:
            print(e)
            return None

    def selectSoNgayCong(self, makc):
        try:
            cursor = self.con.cursor()
            query = "SELECT `SoNgayCong` FROM `KyCong` WHERE `MaKyCong` = %s"
            cursor.execute(query, (makc,))
            kq = cursor.fetchone()[0]
            cursor.close()
            return kq
        except Exception as e:
            print(e)
            return None

    def updateNgayCong(self, ngay, makc, manv):
        try:
            cursor = self.con.cursor()
            update_query = "UPDATE `KyCongChiTiet` SET `{}`= 'P' WHERE `MaKyCong`=%s and `MaNV`=%s"
            query = update_query.format(ngay)
            values = (makc, manv)
            cursor.execute(query, values)
            self.con.commit()
            cursor.close()
            messagebox.showinfo("Thông báo", "Cập nhật thành công")
        except Exception as e:
            messagebox.showinfo("Thông báo", "Cập nhật thất bại")


    def capNhatNgayCong(self,makc,manv,ngayCong):
        cursor = self.con.cursor()
        sql="UPDATE `KyCongChiTiet` SET SoNgayCong=%s WHERE MaKyCong=%s and MaNV=%s"
        values=(ngayCong,makc,manv)
        cursor.execute(sql,values)
        self.con.commit()
        cursor.close()






    def selectInnerjoinNhanvienKyCong(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """ SELECT kycong.MaKyCong, nhanvien.MaNV, nhanvien.HoTen, nhanvien.ChucVu, 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total 
FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(e)
            return None

    def selectMacDinh(self, condition):
        try:
            cursor = self.con.cursor()
            if condition == 1:
                print("condition 1")
                cursor.execute(
                    """ SELECT 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu, 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total 
FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu""",
                )
            elif condition == 2:
                print("condition 2")
                cursor.execute(
                    """
            SELECT CNV.MaKyCong, 
                   CNV.MaNV, 
                   NV.HoTen, 
                   NV.ChucVu, 
                   SEC_TO_TIME(SUM(TIME_TO_SEC(TIMEDIFF(CNV.ThoiGianRa, '17:00:00')))) AS overtime_hours 
            FROM CongNhanVien CNV
            INNER JOIN NhanVien NV ON CNV.MaNV = NV.MaNV
            WHERE CNV.ThoiGianRa > '17:00:00' 
            GROUP BY CNV.MaNV
        """,
                )
            elif condition == 3:
                print("condition 3")
                cursor.execute(
                    """ SELECT 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu, 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total 

FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
     WHERE ChucVu like '%Quản lý%' 
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu""",
                )
            elif condition == 4:
                print("condition 4")
                cursor.execute(
                    """ SELECT 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu, 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total  
FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
     WHERE ChucVu like '%Nhân viên%'
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu""",
                )
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print(e)
            return None

    def selectTheoKhoangThoiGian(self, start, end, condition):
        condition = int(condition[0])
        try:
            start_date = datetime.strptime(start, "%d/%m/%Y").strftime("%Y-%m-%d")
            end_date = datetime.strptime(end, "%d/%m/%Y").strftime("%Y-%m-%d")
            cursor = self.con.cursor()
            if condition == 1:
                cursor.execute(
                    """ SELECT kycong.MaKyCong, nhanvien.MaNV, nhanvien.HoTen, nhanvien.ChucVu, 
     SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total  
    FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
     WHERE Ngay BETWEEN %s AND %s
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu""",
                    (start_date, end_date),
                )          
 
 
            elif condition == 2:
                cursor.execute(
                    """
        SELECT CNV.MaKyCong, 
            CNV.MaNV, 
            NV.HoTen, 
            NV.ChucVu, 
            SEC_TO_TIME(SUM(TIME_TO_SEC(TIMEDIFF(CNV.ThoiGianRa, '17:00:00')))) AS overtime_hours 
        FROM CongNhanVien CNV
        INNER JOIN NhanVien NV ON CNV.MaNV = NV.MaNV
        WHERE CNV.ThoiGianRa > '17:00:00' And Ngay BETWEEN %s AND %s
        GROUP BY CNV.MaKyCong, CNV.MaNV, NV.HoTen, NV.ChucVu
        """,
                    (start_date, end_date),
                )


            elif condition == 3:
                cursor.execute(
                    """ SELECT 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu, 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total 
FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
     WHERE Ngay BETWEEN %s AND %s and ChucVu like '%Quản lý%' And Ngay BETWEEN %s AND %s
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu""",
                    (start_date, end_date),
                )
            elif condition == 4:
                cursor.execute(
                    """ SELECT 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu, 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS giocong_total 
FROM 
    congnhanvien 
INNER JOIN 
    nhanvien ON congnhanvien.MaNV = nhanvien.MaNV 
INNER JOIN 
    kycong ON congnhanvien.MaKyCong = kycong.MaKyCong
     WHERE Ngay BETWEEN %s AND %s and ChucVu like '%Nhân viên%'
GROUP BY 
    kycong.MaKyCong, 
    nhanvien.MaNV, 
    nhanvien.HoTen, 
    nhanvien.ChucVu""",
                    (start_date, end_date),
                )
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print(e)
            return None

    def deleteNhanVien(self, manv):
        try:
            cursor = self.con.cursor()
            query = "UPDATE `NhanVien` SET  `TrangThai`=%s WHERE `MaNV`=%s"
            cursor.execute(query, ("0", manv))
            self.con.commit()
            cursor.close()
            messagebox.showinfo("Thông báo", "Xoá nhân viên thành công")
        except Exception as e:
            messagebox.showinfo("Thông báo", "Xoá nhân viên thất bại")

    def insertNhanVien(
        self, ma_nv, ho_ten, ngay_sinh, so_dien_thoai, gioi_tinh, chuc_vu, email
    ):
        try:
            cursor = self.con.cursor()
            query = "INSERT INTO NhanVien (MaNV, HoTen, NgaySinh, SoDienThoai, GioiTinh, ChucVu, Email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (
                ma_nv,
                ho_ten,
                ngay_sinh,
                so_dien_thoai,
                gioi_tinh,
                chuc_vu,
                email,
            )
            cursor.execute(query, values)
            self.con.commit()
            cursor.close()
            messagebox.showinfo("Thông báo", "Thêm nhân viên thành công")
        except Exception as e:
            messagebox.showinfo("Thông báo", "Thêm nhân viên thất bại")

    def updateNhanVien(self, manv, hoten, ngaysinh, sdt, gioitinh, chucvu, email):
        try:
            cursor = self.con.cursor()
            update_query = "UPDATE `NhanVien` SET `HoTen`=%s, `NgaySinh`=%s, `SoDienThoai`=%s, `GioiTinh`=%s, `ChucVu`=%s, `Email`=%s WHERE `MaNV`=%s"
            values = (hoten, ngaysinh, sdt, gioitinh, chucvu, email, manv)
            cursor.execute(update_query, values)
            self.con.commit()
            cursor.close()
            messagebox.showinfo("Thông báo", "Cập nhật thành công")
        except Exception as e:
            messagebox.showinfo("Thông báo", "Cập nhật thất bại")

    def countNhanVien(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("Select count(MaNV) from nhanvien")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def lateRate(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """SELECT 
    CAST((SUM(CASE WHEN ThoiGianVao IS NOT NULL AND TIME(ThoiGianVao) > '07:00:00' THEN 1 ELSE 0 END) * 100) / COUNT(*) AS SIGNED) AS late_percentage
FROM 
    CongNhanVien
WHERE 
    MONTH(Ngay) = MONTH(NOW()) AND YEAR(Ngay) = YEAR(NOW());"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def averageWorkDay(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """      SELECT 
    AVG(SoNgayCong) AS avg_work_days
FROM 
    KyCong
WHERE 
    MONTH(NgayTinhCong) = MONTH(NOW()) AND YEAR(NgayTinhCong) = YEAR(NOW());"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def overtimeRate(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """   SELECT 
    CAST((SUM(CASE WHEN ThoiGianRa IS NOT NULL AND TIME(ThoiGianRa) > '17:00:00' THEN 1 ELSE 0 END) * 100) / COUNT(*) AS SIGNED) AS overtime_percentage
FROM 
    CongNhanVien
WHERE 
    MONTH(Ngay) = MONTH(NOW()) AND YEAR(Ngay) = YEAR(NOW());"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def sumWorkHourCurrentMonth(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """SELECT 
    SUM(TIMESTAMPDIFF(SECOND, congnhanvien.ThoiGianVao, congnhanvien.ThoiGianRa)) AS total_work_seconds
FROM 
    congnhanvien 
WHERE 
    MONTH(congnhanvien.Ngay) = MONTH(CURRENT_DATE())"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def sumWorkHour(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """SELECT SUM(TIMESTAMPDIFF(SECOND, ThoiGianVao, ThoiGianRa)) AS total_work_seconds
FROM CongNhanVien
WHERE MONTH(Ngay) = MONTH(NOW());"""
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def sumOvertimeWorkHour(self):
        try:
            cursor = self.con.cursor()
            cursor.execute(
                """SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(TIMEDIFF(CNV.ThoiGianRa, '17:00:00')))) AS total_overtime_hours
                FROM CongNhanVien CNV
                INNER JOIN NhanVien NV ON CNV.MaNV = NV.MaNV
                WHERE CNV.ThoiGianRa > '17:00:00' 
                AND MONTH(CNV.Ngay) = MONTH(NOW());
                """
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def selectKyCong(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("Select * from kycong")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def selectChiTietKyCong(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("Select * from chitietkycong")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None

    def selectCongNhanVien(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("Select * from congnhanvien")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return None


# Sử dụng:
db_manager = DatabaseManager()
if db_manager.openConnection():
    print("Kết nối thành công!")
    # Thực hiện truy vấn SELECT * FROM nhanvien
    nhanvien = db_manager.selectAllNhanVien()
    db_manager.closeConnection()
else:
    print("Kết nối thất bại!")
