# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timezone
import time
from dateutil.relativedelta import relativedelta
import datetime as dt
import pandas as pd

# API 호출하기 (한 번의 호출당 25개 json 응답함)
# 필요한 기간: 2019년 9월 1일 ~ 현재 (timestamp: 1567263600 ~ now)
# now = int(datetime.now().timestamp())

def cal_time(tmstmp, hour):
    '''
    시간 계산기: 타임스탬프에 주어진 인자만큼의 시간을 더한 타임스탬프를 리턴
    '''
    tmp = int(tmstmp)
    dttime = datetime.fromtimestamp(tmp)
    wttime = dttime + dt.timedelta(hours = hour)
    return str(int(wttime.timestamp()))

def encode_roman(x):
    '''
    인코딩할 수 없는 문자열 제거
    '''
    return str(x).encode('ascii', 'ignore').decode('ascii')

def get_kpop(now, start_time, end_time):
    '''
    r/kpop 처리
    '''
    kpop = []
    kpop_base_url = 'https://api.pushshift.io/reddit/submission/search/?subreddit=kpop&after={start}&before={end}&sort=asc'
    kpop_done = False

    while not kpop_done:
        kpop_url = kpop_base_url.format(start = start_time, end = end_time)
        kpop_r = requests.get(kpop_url).json()

        if int(end_time) > int(now):
            kpop_done = True

        if len(kpop_r['data']) == 0:
            if int(end_time) >= int(now):
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
                if len(kpop)>1 and d.month != kpop[-1][2]:
                    kpop_done = True
                else:
                    tmp = [date, d.year, d.month, d.day, d.hour, uid, title, author, kr['created_utc'], selftext, kr['num_comments'], kr['score']]
                    kpop.append(tmp)

                # 마지막 날짜 기록용
                end_created = kr['created_utc']

            start_time = end_created
            end_created = cal_time(start_time, 10)

    kpop_save = pd.DataFrame(kpop)
    kpop_save.columns = ['date', 'year', 'month', 'hour', 'day', 'id', 'title', 'author', 'created', 'selftext', 'num_comments', 'score']
    dtm = datetime.fromtimestamp(int(start_time))
    yy = str(dtm.year)
    mm = str(dtm.month)
    if len(mm) < 2:
        mm = '0'+mm
    save_file_name = './kpop/{yy}-{mm}.csv'.format(yy=yy, mm=mm)
    kpop_save.to_csv(save_file_name, encoding='cp949')



def get_kpoppers(now, start_time, end_time):
    '''
    r/kpoppers 처리
    '''
    kpoppers = []
    kpoppers_base_url = 'https://api.pushshift.io/reddit/submission/search/?subreddit=kpoppers&after={start}&before={end}&sort=asc'
    kpoppers_done = False

    while not kpoppers_done:
        kpoppers_url = kpoppers_base_url.format(start= start_time, end= end_time)
        kpoppers_r = requests.get(kpoppers_url).json()

        if int(end_time) > int(now):
            kpoppers_done = True

        if len(kpoppers_r['data']) == 0:
            if int(end_time) >= int(now):
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
                if len(kpoppers) > 1 and d.month != kpoppers[-1][2]:
                    kpoppers_done = True
                else:
                    tmp = [date, d.year, d.month, d.day, d.hour, uid, title, author, kp['created_utc'], selftext, kp['num_comments'], kp['score']]
                    kpoppers.append(tmp)

                # 마지막 날짜 기록용
                end_created = kp['created_utc']

            start_time = end_created
            end_created = cal_time(start_time, 10)
            
    kpoppers_save = pd.DataFrame(kpoppers)
    kpoppers_save.columns = ['date', 'year', 'month', 'day', 'hour', 'id', 'title', 'author', 'created', 'selftext', 'num_comments', 'score']
    dtm = datetime.fromtimestamp(int(start_time))
    yy = str(dtm.year)
    mm = str(dtm.month)
    if len(mm) < 2:
        mm = '0'+mm
    save_file_name = './kpoppers/{yy}-{mm}.csv'.format(yy=yy, mm=mm)
    kpoppers_save.to_csv(save_file_name, encoding='cp949')

def cal_now_by_start(start):
    tmp = int(start)
    dttime = datetime.fromtimestamp(tmp)
    wttime = dttime + relativedelta(months=1)
    return str(int(wttime.timestamp()))

def get_start_times(wanted_start, wanted_end):
    '''
    파라미터는 YYYY-MM 형태로, 얻어오려고 하는 기간을 설정함.
    '''
    arr = []
    st_yy = int(wanted_start.split('-')[0])
    st_mm = int(wanted_start.split('-')[1])
    ed_yy = int(wanted_end.split('-')[0])
    ed_mm = int(wanted_end.split('-')[1])

    for year in range(st_yy, ed_yy+1):
        for month in range(st_mm, ed_mm+1):
            dt = datetime(year, month, 1)
            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
            arr.append(int(timestamp))
    return arr

#start_times = get_start_times('2013-06', '2017-12')
start_times = get_start_times('2017-01', '2017-11')
for start_time in start_times:
    print(start_time)
    end_time = cal_time(start_time, 10)
    now = cal_now_by_start(start_time)

    get_kpop(now, start_time, end_time)
    get_kpoppers(now, start_time, end_time)