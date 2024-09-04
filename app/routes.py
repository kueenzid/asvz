from flask import Blueprint, render_template, request, jsonify
from .api_client import make_api_call

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api_call', methods=['POST'])
def api_call():
    data = request.json
    response = make_api_call(data)
    return jsonify(response)
