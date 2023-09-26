from .exts import db


# mysql读取的数据模型
class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_time = db.Column(db.DateTime)  #######################################################
    sip = db.Column(db.String(15))  #######################################################
    user = db.Column(db.String(64))  #######################################################
    # serial_num = db.Column(db.String(128))
    # sipv6 = db.Column(db.String(40))
    # sport = db.Column(db.Integer)
    # dip = db.Column(db.String(15))
    # dipv6 = db.Column(db.String(40))
    # dport = db.Column(db.Integer)
    # proto = db.Column(db.String(64))
    # passwd = db.Column(db.String(64))
    # info = db.Column(db.String(64))
    # db_type = db.Column(db.String(16))
    # normal_ret = db.Column(db.String(16))
    # vendor_id = db.Column(db.String(128))
    # device_id = db.Column(db.String(15))
    # mpls_label = db.Column(db.String(256))
    # sess_id = db.Column(db.String(32))
    # user_def = db.Column(db.String(512))  # define
    # ine = db.Column(db.String(128))  # define


class WebAccess(db.Model):
    __talbename__ = 'webaccess'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_time = db.Column(db.DateTime)  #######################################################
    sip = db.Column(db.String(15))  #######################################################
    uri = db.Column(db.String(512))  #######################################################
    host = db.Column(db.String(512))  #######################################################
    # serial_num = db.Column(db.String(128))
    # sipv6 = db.Column(db.String(40))
    # sport = db.Column(db.Integer)
    # dip = db.Column(db.String(15))
    # dipv6 = db.Column(db.String(40))
    # dport = db.Column(db.Integer)
    # uri_md5 = db.Column(db.String(32))
    # host_md5 = db.Column(db.String(32))
    # origin = db.Column(db.String(512))
    # cookie = db.Column(db.String(512))
    # agent = db.Column(db.String(128))
    # referer = db.Column(db.String(128))
    # xff = db.Column(db.String(128))
    # data = db.Column(db.String(2048))
    # method = db.Column(db.String(16))
    # status = db.Column(db.Integer)
    # setcookie = db.Column(db.String(512))
    # content_type = db.Column(db.String(128))
    # accept_language = db.Column(db.String(128))
    # vendor_id = db.Column(db.String(128))
    # device_id = db.Column(db.String(15))
    # url_category = db.Column(db.Integer)
    # mpls_label = db.Column(db.String(256))
    # res_body = db.Column(db.String(2048))  # bytes
    # sess_id = db.Column(db.String(32))
    # user_define = db.Column(db.String(512))  # define
    # accept = db.Column(db.String(128))  # Content


# class Terminal(db.Model):
#     __tablename__ = 'terminal'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     pc = db.Column(db.String(17))  # mac地址
#     ip = db.Column(db.String(15))

class Terminal(db.Model):
    __tablename__ = 'terminal'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smac = db.Column(db.String(17))
    sip = db.Column(db.String(15))
    staff = db.Column(db.Text, nullable=True)  # db.Text：字段类型是text
    staff_group = db.Column(db.Text)
    cascadecode = db.Column(db.Text)
    # domain_id = db.Column(db.Integer)
    domain_id = db.Column(db.String(10))
    domain_name = db.Column(db.Text)


# # mysql统计数据模型
class UserUrl(db.Model):
    __tablename__ = 'user-url'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    user = db.Column(db.String(64))
    date = db.Column(db.DateTime)
    ip = db.Column(db.String(15))  # sip
    pc = db.Column(db.String(17))


class UserTermial(db.Model):
    __tablename__ = 'user-terminal'
    pc = db.Column(db.String(17), primary_key=True, nullable=True)
    ip = db.Column(db.String(15))  # sip
    staff = db.Column(db.Text, nullable=True)
    staff_group = db.Column(db.Text)
    cascadecode = db.Column(db.Text)
    domain_id = db.Column(db.Integer)
    domain_name = db.Column(db.Text)


class UrlUserCount(db.Model):
    __tablename__ = 'url-user-count'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    user = db.Column(db.String(64), nullable=True)
    date = db.Column(db.DateTime)
    pc = db.Column(db.String(17))  # ip
    count = db.Column(db.Integer)
    one = db.Column(db.Integer)
    two = db.Column(db.Integer)
    three = db.Column(db.Integer)
    four = db.Column(db.Integer)


class UrlUserHeightLow(db.Model):
    __tablename__ = 'url-user-height-low'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    user_count = db.Column(db.Integer)
    date = db.Column(db.DateTime)


class UrlUserLow(db.Model):
    __tablename__ = 'url-user-low'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(1024))
    user = db.Column(db.String(64), nullable=True)
    date = db.Column(db.Date)
    pc = db.Column(db.String(17))
    count = db.Column(db.Integer)
    one = db.Column(db.Integer)
    two = db.Column(db.Integer)
    three = db.Column(db.Integer)
    four = db.Column(db.Integer)


class UserLogin(db.Model):
    __tablename__ = 'user-login'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(64), nullable=True)
    date = db.Column(db.DateTime)
    pc = db.Column(db.String(17))
    count = db.Column(db.Integer)
    one = db.Column(db.Integer)
    two = db.Column(db.Integer)
    three = db.Column(db.Integer)
    four = db.Column(db.Integer)


# 某PC当前登陆的用户
class UserActive(db.Model):
    __tablename__ = 'user-active'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(64))
    ip = db.Column(db.String(15))  # sip
