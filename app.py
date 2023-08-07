import logging
from flask import Flask,g,request,abort
from error_handlers import *
import config
from blueprint.auth import bp as auth_bp

app = Flask(__name__)


# 注册状态码函数
app.errorhandler(400)(handle_400)
app.errorhandler(401)(handle_401)
app.errorhandler(403)(handle_403)
app.errorhandler(404)(handle_404)
app.errorhandler(429)(handle_429)
app.errorhandler(500)(handle_500)
app.errorhandler(Exception)(handle_exception)
app.config.from_object(config)
app.register_blueprint(auth_bp)

# 在请求之前进行日志记录
@app.before_request
def before_request():
    if hasattr(g,'uid'):
        uid=g.uid
    else:
        uid='Unknown'
    logging.info(f"User {uid} accessed: {request.path}")



if __name__ == '__main__':
    app.run(debug=True)