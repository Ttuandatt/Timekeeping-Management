USE `QLChamCong`;

/* Dữ liệu bảng NhanVien */
INSERT INTO `NhanVien` (`MaNV`, `HoTen`, `NgaySinh`, `SoDienThoai`, `GioiTinh`, `ChucVu`, `Email`, `HinhAnh`) VALUES 
('NV001', 'Nguyễn Văn A', '2004-08-18', '0359197777', 'Nam', 'Nhân viên', 'nva@gmail.com', 'HinhAnh1.png'),
('NV002', 'Lê Văn B', '2002-02-07', '03591955555', 'Nữ', 'Thực tập', 'lvb@gmail.com', 'HinhAnh2.png'),
('NV003', 'Trần Thị C', '2003-09-09', '03591966666', 'Nữ', 'Quản lý', 'ttc@gmail.com', 'HinhAnh3.png');



/* Dữ liệu bảng KyCong */
INSERT INTO `KyCong` (`MaKyCong`, `Thang`, `Nam`, `NgayTinhCong`, `SoNgayCong`, `TrangThai`) VALUES 
('KC022024', '2', '2024', '2024-02-01', '29', true),
('KC032024', '3', '2024', '2024-03-01', '31', false),
('KC042024', '4', '2024', '2024-04-01', '30', false); 



/* Dữ liệu bảng CongNhanVien */
INSERT INTO `CongNhanVien` (`MaKyCong`, `MaNV`, `HoTen`, `Ngay`, `Thu`, `ThoiGianVao`, `ThoiGianRa`) VALUES 
('KC032024', 'NV002', 'Lê Văn B', '2024-03-18', 'Thứ 2', '07:10:20', '17:02:05'),
('KC032024', 'NV001', 'Nguyễn Văn A', '2024-03-18', 'Thứ 2', '07:05:20', NULL);
