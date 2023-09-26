# 初始化文件，创建Flask应用

from flask import Flask
from .views import blue
from .exts import init_exts


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=blue)

    # 配置数据库
    # db_uri = 'sqlite:///sqlite3.db'  # sqlite
    # db_uri = 'mysql+pymysql://root:passwordofroot@box.acommongod.top:3306/url_statistics'  # mysql,格式：mysql+pymysql://用户名:密码@IP:端口/数据库名
    # db_uri = 'mysql+pymysql://root:passwordofroot@box.acommongod.top:3306/url_statistics_test'
    db_uri = 'mysql+pymysql://root:root@localhost:3306/url_statistics'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化插件
    init_exts(app)
    return app
