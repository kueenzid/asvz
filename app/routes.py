from flask import Blueprint, redirect, render_template, request, url_for
from app.services import asvz_service

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "POST":
        result = asvz_service.loginAndStoreCreds(
            request.form["username"], request.form["password"]
        )
        if result[1] == 200:
            return redirect(url_for("main.index"))
        else:
            error_message = "Invalid username or password. Please try again."

    return render_template("login.html", error_message=error_message)


@bp.route("/enroll/<int:id>")
def enroll(id):
    status, message = asvz_service.enroll(id)
    if status:
        return message, 200
    else:
        return message, 500


@bp.route("/unenroll/<int:id>")
def unenroll(id):
    status, message = asvz_service.unenroll(id)
    if status:
        return message, 200
    else:
        return message, 500


@bp.route("/my_enrollment/<int:id>")
def my_enrollment(id):
    return asvz_service.enrollment(id)


@bp.route("/status/<int:id>")
def status(id):
    return asvz_service.status(id)


@bp.route("/enrollments")
def enrollments():
    return render_template("enrollments.html")


@bp.route("/scheduler")
def scheduler():
    return render_template("scheduler.html")


@bp.route("/get_enrollments")
def get_enrollments():
    return asvz_service.get_enrollments()


@bp.route("/get_scheduler_summary")
def get_scheduler_summary():
    return asvz_service.get_summary()


@bp.route("/get_scheduled_courses")
def get_sheduled_courses():
    return asvz_service.get_scheduled_courses()


@bp.route("/get_lesson/<int:id>")
def get_lesson(id):
    return asvz_service.lesson(id)


@bp.app_context_processor
def inject_user_status():
    userName = asvz_service.me()
    if userName:
        return {"logged_in": True, "username": userName}
    else:
        return {"logged_in": False, "username": None}
