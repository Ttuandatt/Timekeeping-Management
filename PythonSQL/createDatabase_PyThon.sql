DROP DATABASE IF EXISTS `QLChamCong`;
CREATE DATABASE IF NOT EXISTS `QLChamCong`;
USE `QLChamCong`;


/*________________________________BẢNG LIÊN QUAN TỚI NHÂN VIÊN________________________________*/

DROP TABLE IF EXISTS `NhanVien`;
CREATE TABLE IF NOT EXISTS `NhanVien` (
    `ID`  				INT UNSIGNED  	AUTO_INCREMENT	PRIMARY KEY,
    `MaNV`      		VARCHAR(50) 		UNIQUE 			NOT NULL,
    `HoTen` 			VARCHAR(255) 		NOT NULL,
    `NgaySinh`     		DATE            	NOT NULL,
    `SoDienThoai`		VARCHAR(11)     	NOT NULL,
    `GioiTinh`			ENUM('Nam', 'Nữ')	NOT NULL,
    `ChucVu`			VARCHAR(100),
    `Email`				VARCHAR(100)    	NOT NULL,
    `HinhAnh`			VARCHAR(255)
);

CREATE INDEX idx_MaNV ON `NhanVien`(`MaNV`);

/*________________________________BẢNG LIÊN QUAN TỚI KỲ CÔNG________________________________*/
DROP TABLE IF EXISTS `KyCong`;
CREATE TABLE IF NOT EXISTS `KyCong` (
    `ID`  				INT UNSIGNED  		AUTO_INCREMENT	PRIMARY KEY	,
	`MaKyCong`      	VARCHAR(50) 							NOT NULL,
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
    `Day1`				VARCHAR(10)						,
    `Day2`				VARCHAR(10)						,
    `Day3`				VARCHAR(10)						,
    `Day4`				VARCHAR(10)						,
    `Day5`				VARCHAR(10)						,
    `Day6`				VARCHAR(10)						,
    `Day7`				VARCHAR(10)						,
    `Day8`				VARCHAR(10)						,
    `Day9`				VARCHAR(10)						,
    `Day10`				VARCHAR(10)						,
    `Day11`				VARCHAR(10)						,
    `Day12`				VARCHAR(10)						,
    `Day13`				VARCHAR(10)						,
    `Day14`				VARCHAR(10)						,
    `Day15`				VARCHAR(10)						,
    `Day16`				VARCHAR(10)						,
    `Day17`				VARCHAR(10)						,
    `Day18`				VARCHAR(10)						,
    `Day19`				VARCHAR(10)						,
    `Day20`				VARCHAR(10)						,
    `Day21`				VARCHAR(10)						,
    `Day22`				VARCHAR(10)						,
    `Day23`				VARCHAR(10)						,
    `Day24`				VARCHAR(10)						,
    `Day25`				VARCHAR(10)						,
    `Day26`				VARCHAR(10)						,
    `Day27`				VARCHAR(10)						,
    `Day28`				VARCHAR(10)						,
    `Day29`				VARCHAR(10)						,
    `Day30`				VARCHAR(10)						,
    `Day31`				VARCHAR(10)						,
    `SoNgayCong`		INT								,
	CONSTRAINT MaNV FOREIGN KEY (`MaNV`) REFERENCES `NhanVien`(`MaNV`),
	CONSTRAINT 	MaKyCong FOREIGN KEY (`MaKyCong`) REFERENCES `KyCong`(`MaKyCong`)
);



/*________________________________BẢNG LIÊN QUAN TỚI CÔNG NHÂN VIÊN________________________________*/
DROP TABLE IF EXISTS `CongNhanVien`;
CREATE TABLE IF NOT EXISTS `CongNhanVien` (
    `ID`  				INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	`MaKyCong`			VARCHAR(50)				NOT NULL,
    `MaNV`      		VARCHAR(50) 			NOT NULL,
    `HoTen` 			VARCHAR(255) 			NOT NULL,
    `Ngay`     			DATETIME						,
    `Thu`				VARCHAR(11)						,
	`ThoiGianVao`		DATETIME						,
    `ThoiGianRa`		DATETIME						,
    FOREIGN KEY (`MaNV`) REFERENCES `NhanVien`(`MaNV`),
	FOREIGN KEY (`MaKyCong`) REFERENCES `KyCong`(`MaKyCong`)
);



