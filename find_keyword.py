import pandas as pd
import glob
import os
from nltk.tokenize import word_tokenize
import re

def find_keyword(dir, keyword):
    '''
    디렉토리 안에 있는 csv 파일에 대해 제목/본문에 대해 keyword(소문자) 유무를 열로 추가
    '''
    os.chdir(dir)
    extension = 'csv'
    files = [i for i in glob.glob('*.{}'.format(extension))]

    for file in files:
        df = pd.read_csv(file, header=0)
        is_keyword_title = []
        is_keyword_selftext = []
        
        for index, row in df.iterrows():
            try:
                title = row["title"].lower() 
            except:
                title = ''
            try:
                selftext = row["selftext"].lower()
            except:
                selftext = ''
        
            title_tokens = word_tokenize(title)
            selftext_tokens = word_tokenize(selftext)
            
            # 키워드 카운팅
            if keyword in title_tokens:
                is_keyword_title.append(1) 
            else:
                is_keyword_title.append(0) 

            if keyword in selftext_tokens:
                is_keyword_selftext.append(1)
            else:
                is_keyword_selftext.append(0)
      

        # 열 추가
        title_column = '{}_title'.format(keyword)
        txt_column = '{}_txt'.format(keyword)
        df[title_column] = is_keyword_title 
        df[txt_column] = is_keyword_selftext

        # 저장 (TODO 파일 이름과 경로 수정해야)
        df.to_csv('./{}-add.csv'.format(file[0:-3]), encoding='cp949')


find_keyword('./example', 'sana')