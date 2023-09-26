from App.models import *
import pandas as pd


def data_summary_table():
    # 获取登录日志和web访问日志的数据
    login_es = Login()
    login = login_es.query.all()
    web_access_es = WebAccess()
    web_access = web_access_es.query.all()

    """
    # 假数据
    login = [Login() for i in range(5)]
    login[0].user, login[0].sip, login[0].access_time = 'abc', '1.1.1.1', '10'
    login[1].user, login[1].sip, login[1].access_time = 'bcd', '1.1.1.2', '11'
    login[2].user, login[2].sip, login[2].access_time = 'cde', '1.1.1.1', '20'
    login[3].user, login[3].sip, login[3].access_time = 'abc', '1.1.1.1', '40'
    login[4].user, login[4].sip, login[4].access_time = 'abc', '1.1.1.1', '50'
    web_access = [WebAccess() for i in range(5)]
    web_access[0].sip, web_access[0].host, web_access[0].uri, web_access[
        0].access_time = '1.1.1.1', 'asdf', '/index.html', '9'
    web_access[1].sip, web_access[1].host, web_access[1].uri, web_access[
        1].access_time = '1.1.1.2', 'asrfydkdf', '/aerhindex.html', '12'
    web_access[2].sip, web_access[2].host, web_access[2].uri, web_access[
        2].access_time = '1.1.1.1', 'asdfguo;', '/iaehndex.html', '29'
    web_access[3].sip, web_access[3].host, web_access[3].uri, web_access[
        3].access_time = '1.1.1.1', 'asftldf', '/indexdfyk.html', '39'
    web_access[4].sip, web_access[4].host, web_access[4].uri, web_access[
        4].access_time = '1.1.1.1', 'asq34ydf', '/indeszrjx.html', '59'
    terminal_mac = [Terminal() for i in range(2)]
    terminal_mac[0].ip, terminal_mac[0].pc = '1.1.1.1', 'pc01'
    terminal_mac[1].ip, terminal_mac[1].pc = '1.1.1.2', 'pc02'
    user_active = [UserActive() for i in range(2)]
    user_active[0].user, user_active[0].ip = 'aerh', '1.1.1.1'
    user_active[1].user, user_active[1].ip = 'dylu', '1.1.1.2'
    """

    # 将表数据转为DataFrame
    df_login = pd.DataFrame(columns=['user', 'sip', 'access_time'])
    for i in range(len(login)):
        df_login.loc[i] = [login[i].user, login[i].sip, login[i].access_time]
    df_web = pd.DataFrame(columns=['sip', 'host', 'uri', 'access_time'])
    for i in range(len(web_access)):
        df_web.loc[i] = [web_access[i].sip, web_access[i].host, web_access[i].uri, web_access[i].access_time]
    # print(df_login)
    # print(df_web)

    data_rows = pd.DataFrame(columns=['url', 'user', 'date', 'ip', 'pc'])  # mysql数据总表中的数据

    # # 登陆表按sip分组
    login_group = df_login.groupby('sip')
    for sip, group in login_group:
        group = group.reset_index(drop=True)  # 重设每个分组的索引

        # 查询sip对应的mac
        # 从数据库查mac
        terminal = Terminal()
        mac = terminal.query.filter_by(sip=sip).first().smac


        for i in range(len(group)):
            start = group.loc[i]['access_time']
            if i == len(group) - 1:
                # end = 99999999999999999
                end = pd.Timestamp('9999-12-31 23:59:59')
            else:
                end = group.loc[i + 1]['access_time']
            # print(start, end)

            # 遍历web日志
            for j in range(len(df_web)):
                if df_web.loc[j]['sip'] == sip and start <= df_web.loc[j]['access_time'] < end:
                    data_rows.loc[len(data_rows)] = [df_web.loc[j]['host'] + df_web.loc[j]['uri'],
                                                     group.loc[i]['user'],
                                                     df_web.loc[j]['access_time'],
                                                     sip,
                                                     mac]
                    df_web = df_web.drop(j)  # 记录一条web日志就删掉
            df_web = df_web.reset_index(drop=True)  # 重设索引

    # 剩下的web日志都是在该时间段各IP的第一条登录日志之前的数据，把剩下的web日志按sip分组
    web_group = df_web.groupby('sip')
    for sip, group in web_group:
        # 为每个group重设索引
        group.reset_index(drop=True, inplace=True)
        # 从UserActive表里找对应的用户
        user_active = UserActive()
        user = user_active.query.filter_by(ip=sip).first().user
        if not user:  # 如果UserActive表里找不到对应的用户，则不记录该web日志
            continue
        # 从Terminal表里找mac地址
        terminal = Terminal()
        mac = terminal.query.filter_by(sip=sip).first().smac
        # 遍历各组的web日志
        for i in range(len(group)):
            data_rows.loc[len(data_rows)] = [group.loc[i]['host'] + group.loc[i]['uri'],
                                             user,
                                             group.loc[i]['access_time'],
                                             sip,
                                             mac]
            df_web = df_web.drop(i)  # 记录一条就删一条
        df_web.reset_index(drop=True, inplace=True)  # 重设索引
        df_web = df_web.reset_index(drop=True)

    # 更新UserActive表
    for sip, group in login_group:
        group.reset_index(drop=True, inplace=True)
        current_user = group.loc[len(group) - 1]['user']  # 获取分组的最后一条数据中的用户
        user_active = UserActive()
        new_user = user_active.query.filter_by(ip=sip).first()
        if new_user:  # 如果user_active表中有记录
            new_user.user = current_user
            db.session.commit()
        else:  # 没有记录就创建
            new_user = UserActive(ip=sip, user=current_user)
            db.session.add(new_user)
            db.session.commit()

    print(data_rows)
    print(df_web)

    # DataFrame转入MySQL
    # data_rows.to_sql('user-url', con=db.engine, if_exists='append', index=False)
    new_data = []
    for i in range(len(data_rows)):
        row = UserUrl()
        row.url = data_rows.loc[i]['url']
        row.user = data_rows.loc[i]['user']
        row.date = data_rows.loc[i]['date']
        row.ip = data_rows.loc[i]['ip']
        row.pc = data_rows.loc[i]['pc']
        new_data.append(row)
    print(new_data)
    try:
        db.session.add_all(new_data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # 回滚
        db.session.flush()
        print(e)
        # return 'fail' + str(e)


if __name__ == "__main__":
    data_summary_table()
