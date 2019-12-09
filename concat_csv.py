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
    # 헤더는 파일 전체에 대해 하나만 읽지만 row index를 갱신하지는 않는다.
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], axis=0, ignore_index=True)

    # 하나로 합친 후 csv로 저장
    filename = "../../combined/{}.csv".format(subreddit)
    combined_csv.to_csv(filename, index=False, encoding='utf-8-sig')

os.chdir('scrapped 폴더')
split_data_dirs = [os.path.abspath(name) for name in os.listdir(".") if os.path.isdir(name)]
for data_dir in split_data_dirs:
    os.chdir(data_dir)
    concat_csv(data_dir)