# 路由+视图函数
from flask import Blueprint
from .models import *
from App.statistics import data_summary_table, url_user_count_table, urluserlow, logintable, terminaltable

# 蓝图
blue = Blueprint('user', __name__)  # 第一个参数为蓝图名称


@blue.route('/')
def index():
    return 'index'


@blue.route('/url_statistics/')
def url_statistics():
    data_summary_table.data_summary_table()
    return "数据总表已生成"


@blue.route("/url_user_count/")
def url_user_count():
    url_user_count_table.url_user_count()
    return 'url_user_count已生成'


@blue.route('/urluserlow/')
def url_user_low():
    urluserlow.urluserlow()
    return 'url_user_low已完成'


@blue.route('/userlogin/')
def user_login():
    logintable.userlogin()
    return 'userlogin已完成'


@blue.route('/terminaltable/')
def terminal_table():
    terminaltable.terminalInfo()
    return 'terminaltable已完成'
