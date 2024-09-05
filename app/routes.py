from flask import Blueprint, render_template, request, jsonify
from app.services import asvz_service

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
    return render_template('login.html')

@bp.route('/enroll/<int:id>')
def enroll(id):
    response = asvz_service.enroll(id)
    if response:
        return "Success", 200
    else:
        return "Failure", 500
    
@bp.route('/unenroll/<int:id>')
def unenroll(id):
    response = asvz_service.unenroll(id)
    if response:
        return "Success", 200
    else:
        return "Failure", 500
    
@bp.route('/my_enrollment/<int:id>')
def my_enrollment(id):
    return asvz_service.enrollment(id)


@bp.route('/enrollments')
def enrollments():
    return render_template('enrollments.html')

@bp.route('/get_lesson/<int:id>')
def get_lesson(id):
    return asvz_service.lesson(id)


@bp.app_context_processor
def inject_user_status():
    user_data = asvz_service.me()
    if user_data:
        return {'logged_in': True, 'username': user_data['firstName']}
    else:
        return {'logged_in': False, 'username': None}