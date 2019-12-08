# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
import pandas as pd
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
retokenize = RegexpTokenizer("[^\d\W]+")

def reg_tokenizer(x):
    return retokenize.tokenize(x)

# 데이터 로드
data = pd.read_csv('./데이터 디렉토리', header = 0)

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

# 시각화
fig = plt.figure(figsize=(10, 10))
plt.imshow(array, interpolation="bilinear")
plt.axis("off")
plt.show()