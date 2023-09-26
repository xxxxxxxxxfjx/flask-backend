from App.models import *
import pandas as pd


def urluserlow():
    res_urlusercount = UrlUserCount.query.all()

    df_res_urlusercount = pd.DataFrame(
        [(res.url, res.date, res.pc, res.count, res.one, res.two, res.three, res.four) for res in res_urlusercount],
        columns=['url', 'date', 'pc', 'count', 'one', 'two', 'three', 'four'])
    url_count_sum = df_res_urlusercount.groupby('url').agg({'count': 'sum'})  # 计算url分组中count的总和
    conform = url_count_sum[url_count_sum['count'] < 60]  # 筛选小于阈值的，return dataframe(url, count)
    # conform['url']=conform.index
    # conform.reset_index(drop=True, inplace=True)
    # for i in range(len(conform)):
    #     res_res = df_res_urlusercount[df_res_urlusercount['url'] == conform.loc[i]['url']]
    #     res_res.to_sql('url-user-low', con=db.engine, if_exists='append', index=False)
    for url, _ in conform.iterrows():
        res_res = df_res_urlusercount[df_res_urlusercount['url'] == url]
        res_res.to_sql('url-user-low', con=db.engine, if_exists='append', index=False)