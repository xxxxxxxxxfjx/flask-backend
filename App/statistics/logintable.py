import datetime

from App.models import *
import pandas as pd


# select user, data, sip, smac from login join terminal on login.sip == terminal.sip
def userlogin():
    # 登录表查询结果
    result = Login.query.all()
    # 终端表查询结果
    result_t = Terminal.query.all()
    # 统计的登陆表查询结果
    # result_userlogin = UserLogin.query.all()
    # 查询结果转成为DataFrame
    df_res_login = pd.DataFrame([(res.user, res.access_time, res.sip) for res in result], columns=['user', 'date', 'ip'])
    df_res_terminal = pd.DataFrame([(res.smac, res.sip) for res in result_t], columns=['pc', 'ip'])
    # df_res_userlogin = pd.DataFrame([(res.user, res.date, res.pc, res.count, res.one, res.two, res.three, res.four) for res in result_userlogin], columns=['user', 'date', 'pc', 'count', 'one', 'two', 'three', 'four'])

    # 每个用户登录
    # df_login = pd.DataFrame(columns=['user', 'date', 'pc', 'count', 'one', 'two', 'three', 'four'])
    user = ''
    pc = ''

    for i in range(len(df_res_login)):
        # 找到mac
        pc = Terminal.query.filter(Terminal.sip == df_res_login.loc[i]['ip']).first().smac

        # 找到这个用户当天的登录记录
        # result_userlogin = UserLogin().query.filter(UserLogin.user == df_res_login.loc[i]['user']).filter(UserLogin.pc == pc).filter(UserLogin.date == df_res_login.loc[i]['date'].date()).first()
        result_userlogin = UserLogin().query.filter(UserLogin.user == df_res_login.loc[i]['user'],
                                                    UserLogin.pc == pc,
                                                    UserLogin.date == df_res_login.loc[i]['date'].date()).first()
        df_res_userlogin = pd.DataFrame(columns=['user', 'date', 'pc', 'count', 'one', 'two', 'three', 'four'])
        if result_userlogin:  # 能找到一条
            # 转为DataFrame
            # df_res_userlogin = pd.DataFrame([(res.user, res.date, res.pc, res.count, res.one, res.two, res.three, res.four) for res in result_userlogin], columns=['user', 'date', 'pc', 'count', 'one', 'two', 'three', 'four'])
            # df_res_userlogin = df_res_userlogin[df_res_userlogin['date'].date() == df_res_login.loc[i]['date'].date()]
            # 当天登录过，更新数据库
            # 用户登录的时间段
            if 0 < df_res_login.loc[i]['date'].hour <= 6:
                result_userlogin.one += 1
            elif 6 < df_res_login.loc[i]['date'].hour <= 12:
                result_userlogin.two += 1
            elif 12 < df_res_login.loc[i]['date'].hour <= 18:
                result_userlogin.three += 1
            else:
                result_userlogin.four += 1
            result_userlogin.count += 1
            db.session.commit()

        # 当天没登录过
        else:  # 没找到，新增一条数据
            one, two, three, four, count = 0, 0, 0, 0, 1
            user = df_res_login.loc[i]['user']
            date = df_res_login.loc[i]['date'].date()

            # 用户登录的时间段
            if 0 < df_res_login.loc[i]['date'].hour <= 6:
                one = 1
            elif 6 < df_res_login.loc[i]['date'].hour <= 12:
                two = 1
            elif 12 < df_res_login.loc[i]['date'].hour <= 18:
                three = 1
            else:
                four = 1
            df_res_userlogin.loc[0] = [user, date, pc, count, one, two, three, four]
            df_res_userlogin.to_sql('user-login', con=db.engine, if_exists='append', index=False)