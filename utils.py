import jwt
from config import SECRET_KEY
from datetime import datetime, timedelta
from functools import wraps
from flask import request,g,abort
import logging


logging.basicConfig(filename='app.log',level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 返回数据的模版
def response_template(data=None,message=None, status='success', code=200):
    return {
        'status': status,
        'message': message,
        'data': data
    }, code

# 生成token
def generate_token(uid, algoritm ='HS256'):
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=1),
        'uid': uid,
    }
    token = jwt.encode(payload,key=SECRET_KEY, algorithm=algoritm)
    return token

# 装饰器，用于验证token
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401,'token不存在')
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
            g.uid = payload.get('uid')
        except jwt.ExpiredSignatureError:
            abort(401,'token已过期')
        except jwt.DecodeError:
            abort(401,'token认证失败')
        except jwt.InvalidTokenError:
            abort(401,'非法的token')
        return func(*args, **kwargs)
    return wrapper
