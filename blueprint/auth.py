from flask import Blueprint, jsonify, abort
from utils import *


bp = Blueprint('auth', __name__,url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    pass


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTEzODY2NjksInVpZCI6M30.PVmBTriJZBwzMgRA83WHdviRvZAF-jKIHkb2LSsfweQ


@bp.route('/login', methods=['POST'])
def login():
    # abort
    data = {}
    data['token'] = generate_token(3)
    return response_template(data=data,message='Login success')

@bp.route('/create', methods=['POST'])
@token_required
def create():
    print('create')
    return response_template(message='create success')




