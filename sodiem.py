from flask import Flask, request, jsonify, redirect, url_for, abort, make_response
from markupsafe import escape
from io import StringIO
import csv

app = Flask(__name__)

app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A", "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A", "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B", "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B", "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C", "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

def average(scores):
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)

def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    if avg >= 8.5:
        return "Giỏi"
    if avg >= 7.0:
        return "Khá"
    if avg >= 5.0:
        return "Trung bình"
    return "Yếu"

def student_summary(mssv):
    student = STUDENTS[mssv]
    avg = average(student["scores"])

    return {
        "mssv": mssv,
        "name": student["name"],
        "lop": student["lop"],
        "scores": student["scores"],
        "average": avg,
        "rank": rank(avg)
    }

def layout(title, body):
    title = escape(title)

    return f"""
        <!doctype html>
        <html lang="vi">
        <head>
            <meta charset="utf-8">
            <title>{title} - Sổ điểm</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 1000px;
                    margin: 30px auto;
                    padding: 0 20px;
                }}

                nav {{
                    margin-bottom: 20px;
                }}

                nav a {{
                    margin-right: 15px;
                }}

                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}

                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                }}

                th {{
                    background: #eee;
                }}

                .filter {{
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <nav>
                <a href="{url_for('home')}">Trang chủ</a>
                <a href="{url_for('student_list')}">Sinh viên</a>
                <a href="{url_for('search')}">Tìm kiếm</a>
            </nav>
            <h1>{title} - Sổ điểm</h1>

            {body}
        </body>
    </html>
    """

@app.route("/")
def home():
    total_students = len(STUDENTS)
    total_classes = len({student["lop"] for student in STUDENTS.values()})

    body = f"""
    <p>Tổng số sinh viên: <strong>{total_students}</strong></p>
    <p>Số lớp: <strong>{total_classes}</strong></p>

    <p><a href="{url_for('student_list')}"> Xem danh sách sinh viên </a></p>
    <p><a href="{url_for('student_api')}"> Xem API sinh viên </a></p>
    """

    return layout("Trang chủ", body)

@app.route("/students")
def student_list():
    lop_filter = request.args.get("lop", "").strip()

    students = []

    for mssv, student in STUDENTS.items():
        if lop_filter:
            if student["lop"].lower() != lop_filter.lower():
                continue

        summary = student_summary(mssv)
        students.append(summary)

    classes = sorted({student["lop"]for student in STUDENTS.values()})

    rows = ""

    for student in students:
        avg = student["average"]

        if avg is None:
            avg_display = "—"
        else:
            avg_display = avg

        rows += f"""
        <tr>
            <td>
                <a href="{url_for('student_detail', mssv=student['mssv'])}">{escape(student['mssv'])}</a>
            </td>
            <td>{escape(student['name'])}</td>
            <td>{escape(student['lop'])}</td>
            <td>{avg_display}</td>
            <td>{escape(student['rank'])}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="5">
                Không có sinh viên phù hợp.
            </td>
        </tr>
        """

    filter_links = f"""
        <a href="{url_for('student_list')}">Tất cả</a>
    """

    for lop in classes:
        filter_links += f"""
    |
    <a href="{url_for('student_list', lop=lop)}">{escape(lop)}</a>
    """

    body = f"""
    <div class="filter">
        <strong>Lọc theo lớp:</strong>
        {filter_links}
    </div>

    <table>
        <thead>
            <tr>
                <th>MSSV</th>
                <th>Họ tên</th>
                <th>Lớp</th>
                <th>Điểm trung bình</th>
                <th>Xếp loại</th>
            </tr>
        </thead>

        <tbody>
            {rows}
        </tbody>
    </table>
    """

    return layout("Danh sách sinh viên", body)

@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404,description=(f"Không có sinh viên với MSSV = {mssv}."))
    student = student_summary(mssv)

    score_rows = ""
    for course, score in student["scores"].items():
        score_rows += f"""
        <tr>
            <td>{escape(course)}</td>
            <td>{score}</td>
        </tr>
        """
    if not score_rows:
        score_rows = """
        <tr>
            <td colspan="2">Chưa có điểm.</td>
        </tr>
        """
    if student["average"] is None:
        avg_display = "—"
    else:
        avg_display = student["average"]

    class_link = url_for("student_list",lop=student["lop"])

    body = f"""
    <p><strong>MSSV:</strong>{escape(student["mssv"])}</p>
    <p><strong>Họ tên:</strong>{escape(student["name"])}</p>
    <p><strong>Lớp:</strong><a href="{class_link}">{escape(student["lop"])}</a></p>
    <p><strong>Điểm trung bình:</strong>{avg_display}</p>
    <p><strong>Xếp loại:</strong>{escape(student["rank"])}</p>

    <h2>Bảng điểm</h2>

    <table>
        <thead>
            <tr>
                <th>Môn học</th>
                <th>Điểm</th>
            </tr>
        </thead>
        <tbody>{score_rows}</tbody>
    </table>

    <p><a href="{url_for('student_list')}"> ← Danh sách sinh viên</a></p>

    """
    return layout(f"Chi tiết {student['name']}",body)

@app.route("/sv/<mssv>")
def old_student_url(mssv):
    return redirect(url_for("student_detail", mssv=mssv), code=301)

@app.route("/students/<mssv>/export")
def export_csv(mssv):
    if mssv not in STUDENTS:
        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    student = STUDENTS[mssv]

    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")

    writer.writerow(["hoc_phan", "diem"])

    for course, score in student["scores"].items():
        writer.writerow([course, score])

    csv_content = output.getvalue()
    response = make_response(csv_content)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (f"attachment; filename=diem_{mssv}.csv")

    return response

@app.route("/search")
def search():
    keyword = request.args.get("q","").strip()
    results = []

    if keyword:
        keyword_lower = keyword.lower()
        for mssv, student in STUDENTS.items():
            name = student["name"]
            if (keyword_lower in name.lower()or keyword_lower in mssv.lower()):
                results.append(student_summary(mssv))

    search_form = f"""

    <form method="get"action="{url_for('search')}">
        <input
            type="text"
            name="q"
            value="{escape(keyword)}"
            placeholder="Nhập tên hoặc MSSV"
        >
        <button type="submit">Tìm kiếm</button>
    </form>
    """
    result_html = ""

    if keyword:
        result_html += f"""
        <p>
            Tìm thấy
            <strong>{len(results)}</strong>
            kết quả cho
            “{escape(keyword)}”
        </p>
        """
        if results:
            result_html += "<ul>"
            for student in results:
                result_html += f"""
                <li>
                    <a href="{url_for(
                        'student_detail',
                        mssv=student['mssv']
                    )}">
                        {escape(student['name'])}
                    </a>
                    -
                    {escape(student['mssv'])}
                </li>
                """
            result_html += "</ul>"
        else:
            result_html += """
            <p>Không có sinh viên phù hợp.</p>
            """

    body = f"""
    {search_form}
    {result_html}
    """
    return layout("Tìm kiếm", body)

@app.route("/api/students")
def student_api():
    return "API sinh viên"

if __name__ == "__main__":
    app.run(debug=True)