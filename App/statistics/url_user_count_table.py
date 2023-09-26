from App.models import *
import pandas as pd
from datetime import datetime, timedelta, time


def url_user_count():
    # 获取url-user-count表中最后（即最新）一条数据
    latest = UrlUserCount.query.order_by(UrlUserCount.date.desc()).first()
    # print(latest)

    # 如果url-user-count表为空，则根据user-url中时间最早的一条数据的日期创建一条数据
    if not latest:
        first = UserUrl().query.order_by(UserUrl.date).first()
        date = datetime.combine(first.date, time())
        # print(date)
        new_data = UrlUserCount(user=first.user, url=first.url, date=first.date, pc=first.ip,
                                count=0, one=0, two=0, three=0, four=0)
        db.session.add(new_data)
        db.session.commit()

    # 获取url-user-count表中最后（即最新）一条数据
    latest = UrlUserCount.query.order_by(UrlUserCount.date.desc()).first()
    current_time = datetime.now()  # 代码开始执行的时间
    start = latest.date
    if start.hour % 2 == 1:
        end = start + timedelta(hours=1)
    else:
        end = start + timedelta(hours=2)
    end = end.replace(minute=0, second=0)
    if start.date() != end.date():
        end = end.replace(hour=0)
    date = start.replace(hour=0, minute=0, second=0)  # 当天日期，时间设为0

    while start < current_time:
        user_url = UserUrl.query.filter(start <= UserUrl.date, UserUrl.date < end).all()  # 从user_url表查询本时间段2小时内的数据
        # 查询结果转DataFrame
        df_user_url = pd.DataFrame([(res.id, res.url, res.user, res.date, res.ip, res.pc) for res in user_url],
                                   columns=UserUrl.__table__.columns.keys())
        # 按user、url、ip分组
        groups_user_url = df_user_url.groupby(['user', 'url', 'ip'])
        for title, group in groups_user_url:  # 遍历user_url
            print(title, type(title))  # title为元组(user,url,ip)
            group = group.reset_index(drop=True)  # 重设索引
            # 查询该user、url、date是否已经记录
            item = UrlUserCount().query.filter(UrlUserCount.user == title[0],
                                               UrlUserCount.url == title[1],
                                               UrlUserCount.pc == title[2],
                                               date <= UrlUserCount.date,
                                               UrlUserCount.date < date + timedelta(days=1)).first()
            if item:  # 如果已经记录
                for _, row in group.iterrows():
                    if item.count != 0:
                        continue
                    item.count += 1
                    item.date = row['date']
                    if 0 <= row['date'].hour < 6:
                        item.one += 1
                    elif 6 <= row['date'].hour < 12:
                        item.two += 1
                    elif 12 <= row['date'].hour < 18:
                        item.three += 1
                    else:
                        item.four += 1
                    db.session.commit()  # 提交修改
            else:  # 如果没有记录
                item = UrlUserCount(user=title[0], url=title[1], pc=title[2],
                                    count=0, one=0, two=0, three=0, four=0)  # 新建数据
                for _, row in group.iterrows():
                    item.date = row['date']
                    item.count += 1
                    if 0 <= row['date'].hour < 6:
                        item.one += 1
                    elif 6 <= row['date'].hour < 12:
                        item.two += 1
                    elif 12 <= row['date'].hour < 18:
                        item.three += 1
                    else:
                        item.four += 1
                    db.session.add(item)
                    db.session.commit()  # 提交修改

        # 更新查询时间段
        start = end
        end = start + timedelta(hours=2)
        date = start.replace(hour=0, minute=0, second=0)
        print('start:', start)
        print('end:', end)

        # break
