import pandas as pd
import glob
import os
from nltk.tokenize import word_tokenize
import re

def find_keyword(subreddit, keyword):
    '''
    디렉토리 안에 있는 csv 파일에 대해 제목/본문에 대해 keyword(소문자) 유무를 열로 추가
    '''
    os.chdir('./data/combined/')
    data = pd.read_csv('./'+ subreddit + '.csv', header=0)

    # NaN 수정
    data['title'].fillna('', inplace = True)
    data['selftext'].fillna('', inplace=True)

    # 제목과 내용 합침
    data['total'] = data['title'] + data['selftext']

    # 키워드 유무를 보여주는 칼럼 생성용 리스트
    is_keyword = []

    for idx, row in data.iterrows():
        # 숫자를 검색할 수 있기 때문에 배제하지 않음
        txt = row['total'].lower()
        txt_tokens = word_tokenize(txt)
            
        # 키워드 카운팅
        if keyword in txt_tokens:
            is_keyword.append(1) 
        else:
            is_keyword.append(0) 
      
    # 열 추가
    txt_column = 'keyword_{}'.format(keyword)
    data[txt_column] = is_keyword

    # 저장 (TODO 파일 이름과 경로 수정해야)
    data.to_csv('../keyword/{}-{}.csv'.format(subreddit, keyword), encoding='cp949')


find_keyword('twice', 'sana')