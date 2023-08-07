# status_handlers.py
from flask import jsonify, abort
from werkzeug.exceptions import HTTPException

# 处理不同状态码的函数，abort中message会传递给e.description
def handle_400(e):
    message = e.description
    if message is None:
        message = 'Invalid input'
    return jsonify({'status': 'error', 'message': message, 'data': None}), 400


def handle_401(e):
    message = e.description
    if message is None:
        message = 'Authentication required'
    return jsonify({'status': 'error', 'message': message,'data':None}), 401


def handle_403(e):
    message = e.description
    if message is None:
        message = 'Access denied'
    return jsonify({'status': 'error', 'message': message,'data':None}), 403


def handle_404(e):
    message = e.description
    if message is None:
        message = 'Resource not found'
    return jsonify({'status': 'error', 'message': message,'data':None}), 404


def handle_429(e):
    message = e.description
    if message is None:
        message = 'Too many requests. Try again later.'
    return jsonify({'status': 'error', 'message': message,'data':None}), 429


def handle_500(e):
    message = e.description
    if message is None:
        message = 'Something went wrong'
    return jsonify({'status': 'error', 'message': message,'data':None}), 500


# 处理所有异常的函数
def handle_exception(e):
    # 处理由abort()抛出的异常
    if isinstance(e, HTTPException):
        return e.get_response()
    return jsonify({'status': 'error', 'message': 'An unexpected status occurred','data':None}), 500
