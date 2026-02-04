from flask import Flask, render_template, request, redirect
from timetable import TimeTable

app = Flask(__name__)
tt = TimeTable()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", schedule=tt.schedule)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        day = request.form["day"]
        time = request.form["time"]
        subject = request.form["subject"]
        faculty = request.form["faculty"]
        classroom = request.form["classroom"]
        tt.add_class(day, time, subject, faculty, classroom)
        return redirect("/view")
    return render_template("manage.html")

@app.route("/remove", methods=["POST"])
def remove():
    day = request.form["day"]
    time = request.form["time"]
    subject = request.form.get("subject")
    tt.remove_class(day, time, subject)
    return redirect("/view")

@app.route("/faculty_unavailable", methods=["POST"])
def faculty_unavailable():
    faculty = request.form["faculty"]
    tt.mark_faculty_unavailable(faculty)
    return redirect("/view")

if __name__ == "__main__":
    app.run(debug=True)
