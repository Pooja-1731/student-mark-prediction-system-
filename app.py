from flask import Flask, render_template, request, redirect, session, url_for
import pickle

app = Flask(__name__)
app.secret_key = "student_marks_secret"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ================= LOAD ML MODEL =================

with open("student_marks_model.pkl", "rb") as file:
    model = pickle.load(file)


# ================= PREDICTION HISTORY =================

predictions = []


# ================= LOGIN =================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    return render_template("login.html")


# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    total_students = 120 + len(predictions)
    total_predictions = 95 + len(predictions)

    if predictions:

        pass_count = sum(
            1 for p in predictions
            if p["status"] == "Pass"
        )

        risk_count = sum(
            1 for p in predictions
            if p["status"] == "At Risk"
        )

        pass_rate = round(
            (pass_count / len(predictions)) * 100
        )

    else:

        pass_rate = 87
        risk_count = 13

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_predictions=total_predictions,
        pass_rate=pass_rate,
        risk_count=risk_count,
        predictions=predictions
    )


# ================= STUDENTS =================

@app.route("/students")
def students():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template(
        "students.html",
        predictions=predictions
    )


# ================= PREDICT =================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        student_name = request.form["student_name"]

        attendance = float(
            request.form["attendance"]
        )

        assignment_marks = float(
            request.form["assignment_marks"]
        )

        previous_exam_marks = float(
            request.form["previous_exam_marks"]
        )


        # ML Prediction

        prediction = model.predict([[
            attendance,
            assignment_marks,
            previous_exam_marks
        ]])


        predicted_marks = round(
            prediction[0], 2
        )


        # Status

        if predicted_marks >= 50:
            status = "Pass"
        else:
            status = "At Risk"


        # Save prediction

        predictions.append({

            "student_name": student_name,

            "marks": predicted_marks,

            "status": status

        })


        return render_template(
            "result.html",

            student_name=student_name,

            predicted_marks=predicted_marks,

            status=status
        )


    return render_template("predict.html")


# ================= REPORTS =================

@app.route("/reports")
def reports():

    if "admin" not in session:
        return redirect(url_for("login"))


    total_predictions = len(predictions)

    pass_count = sum(
        1 for p in predictions
        if p["status"] == "Pass"
    )

    risk_count = sum(
        1 for p in predictions
        if p["status"] == "At Risk"
    )


    if total_predictions > 0:

        pass_rate = round(
            (pass_count / total_predictions) * 100
        )

    else:

        pass_rate = 0


    return render_template(

        "reports.html",

        predictions=predictions,

        total_predictions=total_predictions,

        pass_count=pass_count,

        risk_count=risk_count,

        pass_rate=pass_rate

    )


# ================= SETTINGS =================

@app.route("/settings")
def settings():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("settings.html")


# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(
        url_for("login")
    )


# ================= RUN APP =================

if __name__ == "__main__":

    app.run(debug=True)