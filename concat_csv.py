# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd

def concat_csv(path):
    '''
    달별로 크롤링되어 subreddit 폴더 하에 정리된 파일을 하나의 파일로 합친다.
    '''
    # 작업하는 subreddit
    subreddit = os.path.basename(path)

    # 확장자 지정 및 파일 이름 불러오기
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # 리스트의 파일 읽어서 하나의 파일로 합치기
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], axis=0, ignore_index=True)
    
    # 이전 인덱스행 삭제
    combined_csv = combined_csv.drop(combined_csv.columns[0], axis='columns')

    # 중복값이 있다면 제거한다.
    combined_csv.drop_duplicates()

    # 전처리(selftext에서 comma 제외)
    combined_csv['title'] = combined_csv['title'].str.replace(',', '')
    combined_csv['selftext'] = combined_csv['selftext'].str.replace(',', '')

    # 하나로 합친 후 csv로 저장
    filename = "/home/maria_dev/project/data/combined/{}.csv".format(subreddit)
    combined_csv.to_csv(filename)

split_data_dirs = [os.path.abspath(name) for name in os.listdir(".") if os.path.isdir(name)]
for data_dir in split_data_dirs:
    os.chdir(data_dir)
    concat_csv(data_dir)