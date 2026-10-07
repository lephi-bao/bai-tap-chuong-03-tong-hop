# bai-tap-chuong-03-tong-hop

# Sổ điểm lớp học

## Giới thiệu

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

## 1.Kết quả flask --app sodiem routes

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

## 2.Dòng trạng thái và body (hoặc header quan trọng) của từng lệnh curl

curl.exe -i "http://127.0.0.1:8000/sv/23T1020001"  
HTTP/1.1 301 MOVED PERMANENTLY\tong_hop>  
Location: /students/23T1020001

curl.exe -i "http://127.0.0.1:8000/students/23T1020001/export"  
HTTP/1.1 200 OK  
Content-Disposition: attachment; filename=diem_23T1020001.csv  
hoc_phan,diem  
PMMNM,8.5  
CSDL,7.0  
MMT,9.0

curl.exe "http://127.0.0.1:8000/api/students?lop=k47a&min_avg=7"  
[{
"average": 8.17,
 "lop": "K47A",
 "mssv": "23T1020001",
 "name": "Nguyễn Văn An",
 "rank": "Khá",
 "scores": {
 "CSDL": 7.0,
 "MMT": 9.0,
 "PMMNM": 8.5
 }
 }
 ]

curl.exe -i "http://127.0.0.1:8000/api/students?min_avg=abc"  
HTTP/1.1 400 BAD REQUEST  
{  
 "detail": "min_avg phải là một số.",  
 "error": "Dữ liệu không hợp lệ"  
 }

curl.exe -i "http://127.0.0.1:8000/api/students/999"  
HTTP/1.1 404 NOT FOUND  
{  
 "detail": "Không có sinh viên với MSSV = 999.",  
 "error": "Không tìm thấy"  
 }

curl.exe -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/web?score=9"  
HTTP/1.1 201 CREATED  
{  
 "average": 9.0,  
 "course": "WEB",  
 "mssv": "23T1020005",  
 "score": 9.0  
 }

curl.exe -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=7.5"  
HTTP/1.1 200 OK  
{  
 "average": 7.5,  
 "course": "WEB",  
 "mssv": "23T1020005",  
 "score": 7.5  
 }

curl.exe -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=11"  
HTTP/1.1 400 BAD REQUEST  
{  
 "detail": "score phải nằm trong khoảng từ 0 đến 10.",  
 "error": "Dữ liệu không hợp lệ"  
 }

curl.exe -i -X DELETE "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB"  
HTTP/1.1 204 NO CONTENT

curl.exe -i -X POST "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB"  
HTTP/1.1 405 METHOD NOT ALLOWED  
{  
 "detail": "The method is not allowed for the requested URL.",  
 "error": "Phương thức không được hỗ trợ"  
 }

curl.exe -i -X POST "http://127.0.0.1:8000/students"  
HTTP/1.1 405 METHOD NOT ALLOWED
