# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import datetime as dt
import pandas as pd

# 베이스 url
kpop_base_url = 'https://api.pushshift.io/reddit/submission/search/?subreddit=kpop&after={start}&before={end}&sort=asc'
kpoppers_base_url = 'https://api.pushshift.io/reddit/submission/search/?subreddit=kpoppers&after={start}&before={end}&sort=asc'

# API 호출하기 (한 번의 호출당 25개 json 응답함)
# 필요한 기간: 2019년 9월 1일 ~ 현재 (timestamp: 1567263600 ~ now)
# now = int(datetime.now().timestamp())
now = 1530403200

# 시간 계산기
def cal_time(tmstmp, hour):
    tmp = int(tmstmp)
    dttime = datetime.fromtimestamp(tmp)
    wttime = dttime + dt.timedelta(hours = hour)
    return str(int(wttime.timestamp()))

# 인코딩할 수 없는 문자열 제거
def encode_roman(x):
    return str(x).encode('ascii', 'ignore').decode('ascii')

kpop_done = False
kpoppers_done = False

# r/kpop 처리
kpop = []
start_time = '1527811200'  #초기값
end_time = cal_time(1527811200, 10)

while not kpop_done:
    kpop_url = kpop_base_url.format(start = start_time, end = end_time)
    kpop_r = requests.get(kpop_url).json()

    if int(end_time) > now:
        break

    if len(kpop_r['data']) == 0:
        if int(end_time) >= now:
            kpop_done = True
        else:
            start_time = cal_time(end_time, 1)
            end_time = cal_time(start_time, 10)
    else:
        end_created = 0
        for kr in kpop_r['data']:
            # 날짜 분리
            timestamp = int(kr['created_utc'])
            d = datetime.fromtimestamp(timestamp)
            date = str(d.year)+'-'+str(d.month)+'-'+str(d.day)

            # 문자열에 대해 인코딩 처리
            uid = encode_roman(kr['id'])
            title = encode_roman(kr['title'])
            author = encode_roman(kr['author'])
            try:
                if kr['selftext']:
                    selftext = encode_roman(kr['selftext'])
                else:
                    selftext = ''
            except:
                print(kr)

            # 데이터 저장
            tmp = [date, d.year, d.month, d.day, d.hour, uid, title, author, kr['created_utc'], selftext, kr['num_comments'], kr['score']]
            kpop.append(tmp)

            # 마지막 날짜 기록용
            end_created = kr['created_utc']

        start_time = end_created
        end_created = cal_time(start_time, 10)

        kpop_save = pd.DataFrame(kpop)
        kpop_save.columns = ['date', 'year', 'month', 'hour', 'day', 'id', 'title', 'author', 'created', 'selftext', 'num_comments', 'score']
        kpop_save.to_csv('./kpop/2018-06.csv', encoding='cp949')


# r/kpoppers 처리
kpoppers = []
start_time = '1527811200'  #초기값
end_time = cal_time(1527811200, 10)

while not kpoppers_done:
    kpoppers_url = kpoppers_base_url.format(start= start_time, end= end_time)
    kpoppers_r = requests.get(kpoppers_url).json()

    if int(end_time) > now:
        break

    if len(kpoppers_r['data']) == 0:
        if int(end_time) >= now:
            kpoppers_done = True
        else:
            start_time = cal_time(end_time, 1)
            end_time = cal_time(start_time, 10)
    else:
        end_created = 0
        for kp in kpoppers_r['data']:
            # 날짜 분리
            timestamp = int(kp['created_utc'])
            d = datetime.fromtimestamp(timestamp)
            date = str(d.year)+'-'+str(d.month)+'-'+str(d.day)

            # 문자열에 대해 인코딩 처리
            uid = encode_roman(kp['id'])
            title = encode_roman(kp['title'])
            author = encode_roman(kp['author'])
            try:
                if kp['selftext']:
                    selftext = encode_roman(kp['selftext'])
                else:
                    selftext = ''
            except:
                print(kp)

            # 데이터 저장
            tmp = [date, d.year, d.month, d.day, d.hour, uid, title, author, kp['created_utc'], selftext, kp['num_comments'], kp['score']]
            kpoppers.append(tmp)

            # 마지막 날짜 기록용
            end_created = kp['created_utc']

        start_time = end_created
        end_created = cal_time(start_time, 10)

        kpoppers_save = pd.DataFrame(kpoppers)
        kpoppers_save.columns = ['date', 'year', 'month', 'day', 'hour', 'id', 'title', 'author', 'created', 'selftext', 'num_comments', 'score']
        kpoppers_save.to_csv('./kpoppers/2018-06.csv', encoding='cp949')