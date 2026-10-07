# bai-tap-chuong-03-tong-hop

# Sổ điểm lớp học

## 1. Giới thiệu

Ứng dụng quản lý sổ điểm sinh viên được xây dựng bằng Flask.

Các chức năng chính:

- Xem danh sách sinh viên
- Lọc sinh viên theo lớp
- Xem chi tiết sinh viên
- Chuyển hướng URL cũ
- Xuất bảng điểm CSV
- Tìm kiếm sinh viên
- REST API danh sách sinh viên
- REST API xem, thêm, sửa và xóa điểm
- Xử lý lỗi 400, 404, 405

---

## 2.Kết quả flask --app sodiem routes

Endpoint Methods Rule

---

api_student_detail GET /api/students <mssv>  
api_student_score DELETE, GET, PUT /api/students/<mssv>/scores/<course>
api_students GET /api/students  
export_csv GET /students/<mssv>/export  
home GET /  
old_student_url GET /sv/<mssv>  
search GET /search  
static GET /static/<path:filename>  
student_detail GET /students/<mssv>  
student_list GET /students  
(.venv) PS C:\Python\chuong_03\tong_hop>
