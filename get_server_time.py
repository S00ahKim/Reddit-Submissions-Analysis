#-*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time

def get_server_time():
    '''
    reddit 서버 시간 구하기
    '''
    date = urllib.request.urlopen('http://www.reddit.com').headers['Date']
    timestmp = int(time.mktime(time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')))
    return timestmp