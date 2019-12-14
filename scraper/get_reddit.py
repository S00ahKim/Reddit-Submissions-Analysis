# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
import datetime as dt
import pandas as pd
import urllib.request
import urllib.error
import os

# API 호출하기 (한 번의 호출당 25개 json 응답함)

def cal_time(tmstmp, hour):
    '''
    시간 계산기: 타임스탬프에 주어진 인자만큼의 시간을 더한 타임스탬프를 리턴
    '''
    tmp = int(tmstmp)
    dttime = datetime.fromtimestamp(tmp)
    wttime = dttime + dt.timedelta(hours = hour)
    return str(int(wttime.timestamp()))

def get_server_time():
    '''
    reddit 서버 시간 구하기
    '''
    date = urllib.request.urlopen('http://www.google.com').headers['Date']
    timestmp = int(time.mktime(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))
    return timestmp

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

def get_start_time(subreddit):
    meta = pd.read_csv('/home/maria_dev/project/data/metadata/data.csv', header=0)
    try:
        start = meta.loc[meta['subreddit'] == subreddit, 'last'].values[0]
    except:
        r = requests.get('https://www.reddit.com/r/{}/about.json'.format(subreddit), headers = {'User-agent': 'reddit_crawler'}).json()
        start = int(r['data']['created_utc'])
    return start

def modify_meta(subreddit, last):
    meta = pd.read_csv('/home/maria_dev/project/data/metadata/data.csv', header=0)
    try:
        meta.loc[meta['subreddit'] == subreddit, 'last'] = last
        meta.to_csv('/home/maria_dev/project/data/metadata/data.csv', index=False)
    except:
        meta = meta.append({'subreddit':subreddit, 'last':last}, ignore_index=True)
        meta = meta[['subreddit', 'last']]
        meta.to_csv('/home/maria_dev/project/data/metadata/data.csv')

def get_reddit(subreddit, end_time):
    start_time = get_start_time(subreddit)

    arr = []
    base_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&after={start}&before={end}&sort=asc'
    get_all = False

    last_get_time = 0

    while not get_all:
        next_time = cal_time(start_time, 10)
        url = base_url.format(subreddit=subreddit, start=start_time, end=next_time)
        try:
            r = requests.get(url).json()
        except:
            r = {'data':[]}
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
                last_get_time = int(submission['created_utc'])

            start_time = last_get_time
            next_time = cal_time(start_time, 10)

    df_save = pd.DataFrame(arr)
    df_save.columns = ['sbr', 'sbr_id', 'date', 'year', 'month', 'hour', 'day', 'id', 
                        'domain', 'title', 'full_link', 'author', 'created', 'selftext', 
                        'num_comments', 'score', 'over_18', 'thumbnail', 'media_provider',
                        'media_thumbnail', 'media_title', 'media_description', 'media_url']


    dtm = datetime.fromtimestamp(last_get_time)
    yy = str(dtm.year)
    mm = str(dtm.month)

    if len(mm) < 2:
        mm = '0'+mm
        
    path = '/home/maria_dev/project/data/scrapped/{dirname}/'.format(dirname = subreddit)
    save_file_name = path + '{yy}-{mm}-{last}.csv'.format(yy=yy, mm=mm, last=last_get_time)
    df_save.to_csv(save_file_name, encoding='cp949')
    modify_meta(subreddit, last_get_time)

if __name__ == '__main__':
    all_dirs = [os.path.abspath(name) for name in os.listdir(".") if os.path.isdir(name)]
    end_time = get_server_time()
    print(end_time)
    for dirc in all_dirs:
        subreddit = os.path.basename(os.path.normpath(dirc))
        print('crawling subreddit... ', subreddit)
        get_reddit(subreddit, end_time)