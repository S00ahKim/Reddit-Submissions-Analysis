import pandas as pd
import glob
import os
from nltk.tokenize import word_tokenize
import re
import sys

def find_keyword(subreddit, keyword):
    '''
    디렉토리 안에 있는 csv 파일에 대해 제목/본문에 대해 keyword(소문자) 유무를 열로 추가
    '''
    data = pd.read_csv('/home/maria_dev/project/data/combined/{}.csv'.format(subreddit), header=0)

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

    # 저장 
    data.to_csv('/home/maria_dev/project/data/keyword/{}-{}.csv'.format(subreddit, keyword), encoding='cp949')

if __name__ == "__main__":
    # 실행 방법: python find_keyword.py "subreddit" "keyword"
    if len(sys.argv) != 3:
        print("Error! Argument should be 2 strings: subreddit, keyword")
        sys.exit(-1)
    sbr = sys.argv[1]
    kwd = sys.argv[2]
    find_keyword(sbr, kwd)