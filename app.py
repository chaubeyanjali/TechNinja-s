from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# ---------- HOME ----------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ---------- STUDENT ----------
@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        return render_template("student.html")
    return redirect(url_for("home"))


# ---------- TEACHER ----------
@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        return render_template("teacher.html")
    return redirect(url_for("home"))


# ---------- ADMIN ----------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        return render_template("admin.html")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
