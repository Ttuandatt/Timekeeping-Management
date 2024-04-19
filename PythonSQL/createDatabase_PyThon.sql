DROP DATABASE IF EXISTS `QLChamCong`;
CREATE DATABASE IF NOT EXISTS `QLChamCong`;
USE `QLChamCong`;


/*________________________________BẢNG LIÊN QUAN TỚI NHÂN VIÊN________________________________*/

DROP TABLE IF EXISTS `NhanVien`;
CREATE TABLE IF NOT EXISTS `NhanVien` (
    `MaNV`      		VARCHAR(50) 		NOT NULL	PRIMARY KEY,
    `HoTen` 			VARCHAR(255) 		NOT NULL,
    `NgaySinh`     		DATE            	NOT NULL,
    `SoDienThoai`		VARCHAR(11)     	NOT NULL,
    `GioiTinh`			ENUM('Nam', 'Nữ')	NOT NULL,
    `ChucVu`			VARCHAR(100),
    `Email`				VARCHAR(100)    	NOT NULL,
    `HinhAnh`			VARCHAR(255),
    `TrangThai`     	TINYINT         	NOT NULL DEFAULT 1
);

CREATE INDEX idx_MaNV ON `NhanVien`(`MaNV`);

/*________________________________BẢNG LIÊN QUAN TỚI KỲ CÔNG________________________________*/
DROP TABLE IF EXISTS `KyCong`;
CREATE TABLE IF NOT EXISTS `KyCong` (
	`MaKyCong`      	VARCHAR(50) 							NOT NULL	PRIMARY KEY,
    `Thang` 			VARCHAR(50) 							NOT NULL,
    `Nam`     		    VARCHAR(50)            					NOT NULL,
	`NgayTinhCong`		DATE	 								NOT NULL,
    `SoNgayCong`		INT										NOT NULL,
    `TrangThai`			BOOLEAN									NOT NULL	DEFAULT false
);
CREATE INDEX idx_MaKyCong  ON `KyCong`(`MaKyCong`);

/*________________________________BẢNG LIÊN QUAN TỚI KỲ CÔNG CHI TIẾT________________________________*/
DROP TABLE IF EXISTS `KyCongChiTiet`;
CREATE TABLE IF NOT EXISTS `KyCongChiTiet` (
	`MaKyCong`      	VARCHAR(50) 			NOT NULL,
	`MaNV`      		VARCHAR(50) 			NOT NULL,
    `HoTen` 			VARCHAR(255) 			NOT NULL,
    `Day1`				VARCHAR(10)				DEFAULT '',
    `Day2`				VARCHAR(10)				DEFAULT '',
    `Day3`				VARCHAR(10)				DEFAULT '',
    `Day4`				VARCHAR(10)				DEFAULT '',
    `Day5`				VARCHAR(10)				DEFAULT '',
    `Day6`				VARCHAR(10)				DEFAULT '',
    `Day7`				VARCHAR(10)				DEFAULT '',
    `Day8`				VARCHAR(10)				DEFAULT '',
    `Day9`				VARCHAR(10)				DEFAULT '',
    `Day10`				VARCHAR(10)				DEFAULT '',
    `Day11`				VARCHAR(10)				DEFAULT '',
    `Day12`				VARCHAR(10)				DEFAULT '',
    `Day13`				VARCHAR(10)				DEFAULT '',
    `Day14`				VARCHAR(10)				DEFAULT '',
    `Day15`				VARCHAR(10)				DEFAULT '',
    `Day16`				VARCHAR(10)				DEFAULT '',
    `Day17`				VARCHAR(10)				DEFAULT '',
    `Day18`				VARCHAR(10)				DEFAULT '',
    `Day19`				VARCHAR(10)				DEFAULT '',
    `Day20`				VARCHAR(10)				DEFAULT '',
    `Day21`				VARCHAR(10)				DEFAULT '',
    `Day22`				VARCHAR(10)				DEFAULT '',
    `Day23`				VARCHAR(10)				DEFAULT '',
    `Day24`				VARCHAR(10)				DEFAULT '',
    `Day25`				VARCHAR(10)				DEFAULT '',
    `Day26`				VARCHAR(10)				DEFAULT '',
    `Day27`				VARCHAR(10)				DEFAULT '',
    `Day28`				VARCHAR(10)				DEFAULT '',
    `Day29`				VARCHAR(10)				DEFAULT '',
    `Day30`				VARCHAR(10)				DEFAULT '',
    `Day31`				VARCHAR(10)				DEFAULT '',
    `SoNgayCong`		DOUBLE						DEFAULT 0,
	CONSTRAINT MaNV FOREIGN KEY (`MaNV`) REFERENCES `NhanVien`(`MaNV`),
	CONSTRAINT 	MaKyCong FOREIGN KEY (`MaKyCong`) REFERENCES `KyCong`(`MaKyCong`)
);



/*________________________________BẢNG LIÊN QUAN TỚI CÔNG NHÂN VIÊN________________________________*/
DROP TABLE IF EXISTS `CongNhanVien`;
CREATE TABLE IF NOT EXISTS `CongNhanVien` (
	`MaKyCong`			VARCHAR(50)				NOT NULL,
    `MaNV`      		VARCHAR(50) 			NOT NULL,
    `HoTen` 			VARCHAR(255) 			NOT NULL,
    `Ngay`     			DATE						,
    `Thu`				VARCHAR(11)						,
	`ThoiGianVao`		TIME							,
    `ThoiGianRa`		TIME							,
    FOREIGN KEY (`MaNV`) REFERENCES `NhanVien`(`MaNV`),
	FOREIGN KEY (`MaKyCong`) REFERENCES `KyCong`(`MaKyCong`)
);



