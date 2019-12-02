# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd

def concat_csv(subreddit):
    '''
    달별로 크롤링되어 subreddit 폴더 하에 정리된 파일을 하나의 파일로 합친다.
    '''
    # 작업할 디렉토리 위치 변경
    directory = "./{}".format(subreddit)
    os.chdir(directory)

    # 확장자 지정 및 파일 이름 불러오기
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # 리스트의 파일 읽어서 하나의 파일로 합치기
    # 헤더는 파일 전체에 대해 하나만 읽지만 row index를 갱신하지는 않는다.
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    # 하나로 합친 후 csv로 저장
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')