# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
import pandas as pd
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
import sys

def reg_tokenizer(x):
    retokenize = RegexpTokenizer("[^\d\W]+")
    return retokenize.tokenize(x)

def word_cloud(subreddit):
    # 데이터 로드
    data = pd.read_csv('/home/maria_dev/project/data/combined/{}.csv'.format(subreddit), header = 0)

    # NAN 처리
    data['title'].fillna('', inplace = True)
    data['selftext'].fillna('', inplace=True)

    # 제목과 내용 합침
    data['total'] = data['title'] + data['selftext']

    # 토큰화
    data['token'] = data['total'].apply(reg_tokenizer)

    # 워드클라우드 설정
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        width = 800,
        height = 800,
        background_color="white")

    # 텍스트 만들기
    text = data['total'].tolist()
    text = ''.join(text)

    # 워드클라우드 생성
    wordcloud = wordcloud.generate_from_text(text)

    # 시각화하기 위한 배열화
    array = wordcloud.to_array()

    # 워드클라우드 저장
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(array, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    plt.savefig('/home/maria_dev/project/data/wordcloud/{}.png'.format(subreddit), dpi=300)

if __name__ == "__main__":
    # 실행 방법: python word_cloud.py "subreddit"
    if len(sys.argv) != 2:
        print("Error! Argument should be 1 string.")
        sys.exit(-1)
    sbr = sys.argv[1]
    word_cloud(sbr)