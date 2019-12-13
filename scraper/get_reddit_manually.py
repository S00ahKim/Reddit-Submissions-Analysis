#!/usr/bin/env python3.6
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

def cal_end_by_start(start):
    '''
    시작 시간을 인자로 주면 한달 뒤의 시간을 문자열로 리턴한다.
    '''
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
        for month in range(1, 13):
            if year == st_yy:
                if month < st_mm:
                    continue
            if year == ed_yy:
                if month > ed_mm:
                    break
            dt = datetime(year, month, 1)
            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
            arr.append(int(timestamp))
    return arr

def get_reddit(start_time, end_time, subreddit):
    '''
    r/subreddit의 submissions를 start_time부터 end_time까지 긁는다.
    argument 타입은 모두 string
    end_time: 크롤링이 끝나는 시점
    '''
    arr = []
    base_url = 'https://api.pushshift.io/reddit/submission/search/?subreddit={subreddit}&after={start}&before={end}&sort=asc'
    get_all = False

    dtm = datetime.fromtimestamp(int(start_time))
    yy = str(dtm.year)
    mm = str(dtm.month)
    last_get_time = 0

    while not get_all:
        next_time = cal_time(start_time, 10)
        url = base_url.format(subreddit=subreddit, start=start_time, end=next_time)
        try:
            r = requests.get(url).json()
        except:
            print(requests.get(url))

        if len(r['data']) == 0:
            if int(last_get_time) >= int(end_time):
                get_all = True
            else:
                start_time = next_time
                next_time = cal_time(start_time, 10)
        
        else:
            for submission in r['data']:
                # 날짜 분리
                timestamp = int(submission['created_utc'])
                d = datetime.fromtimestamp(timestamp)
                date = str(d.year)+'-'+str(d.month)+'-'+str(d.day)

                # 문자열에 대해 인코딩 처리
                sbr = encode_roman(submission['subreddit'])
                sbr_id = encode_roman(submission['subreddit_id'])
                uid = encode_roman(submission['id'])
                domain = encode_roman(submission['domain'])
                title = encode_roman(submission['title'])
                full_link = encode_roman(submission['full_link'])
                author = encode_roman(submission['author'])
                try:
                    if submission['selftext']:
                        selftext = encode_roman(submission['selftext'])
                    else:
                        selftext = ''
                except:
                    selftext = ''

                try:
                    if submission['thumbnail']:
                        thumbnail = encode_roman(submission['thumbnail'])
                    else:
                        thumbnail = ''
                except:
                    thumbnail = ''

                try:
                    if submission['media']['oembed']:
                        for e in submission['media']['oembed']:
                            media_provider = encode_roman(e['provider_name'])
                            media_thumbnail = encode_roman(e['thumbnail_url'])
                            media_title = encode_roman(e['title'])
                            media_description = encode_roman(e['description'])
                            media_url = encode_roman(e['url'])
                            break
                except:
                    media_provider = ''
                    media_thumbnail = ''
                    media_title = ''
                    media_description = ''
                    media_url = ''

                over_18 = str(submission['over_18'])

                # 데이터 저장
                if len(arr)>1 and d.month != arr[-1][4]:
                    get_all = True
                else:
                    tmp = [sbr, sbr_id, date, d.year, d.month, d.day, d.hour, uid, domain, title, full_link, 
                            author, submission['created_utc'], selftext, submission['num_comments'], 
                            submission['score'], over_18, thumbnail, media_provider,
                            media_thumbnail, media_title, media_description, media_url]
                    arr.append(tmp)

                # 마지막 날짜 기록용
                last_get_time = submission['created_utc']

            start_time = last_get_time
            next_time = cal_time(start_time, 10)

    df_save = pd.DataFrame(arr)
    df_save.columns = ['sbr', 'sbr_id', 'date', 'year', 'month', 'hour', 'day', 'id', 
                        'domain', 'title', 'full_link', 'author', 'created', 'selftext', 
                        'num_comments', 'score', 'over_18', 'thumbnail', 'media_provider',
                        'media_thumbnail', 'media_title', 'media_description', 'media_url']
    
    if len(mm) < 2:
        mm = '0'+mm

    path = '../data/scrapped/{dirname}/'.format(dirname = subreddit)
    save_file_name = path + '{yy}-{mm}.csv'.format(yy=yy, mm=mm)
    df_save.to_csv(save_file_name, encoding='cp949')


start_times = get_start_times('2016-07', '2019-11')
for start_time in start_times:
    print(start_time)
    end_time = cal_end_by_start(start_time)
    get_reddit(start_time, end_time, 'BlackPink')