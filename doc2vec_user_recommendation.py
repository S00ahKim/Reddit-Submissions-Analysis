# -*- coding: utf-8 -*-
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from scipy import spatial

# 데이터 로드
data = pd.read_csv('./데이터 디렉토리', header = 0)

# NaN 수정
data['title'].fillna('', inplace = True)
data['selftext'].fillna('', inplace=True)

# 제목과 내용 합침
data['total'] = data['title'] + data['selftext']

# 토크나이저: 숫자가 아닌 문자만 처리
retokenize = RegexpTokenizer("[^\d\W]+")

def reg_tokenizer(x):
    return retokenize.tokenize(x)

data['token'] = data['total'].apply(reg_tokenizer)

# 이중 리스트로 구성 (for gensim input)
sentences = data['token'].tolist()

# 도큐먼트 index - 토큰화한 도큐먼트 페어
index_document_pair = [
    (text, [f"{i}",]) for i, text in enumerate(sentences)
]

# 학습
TRAIN_documents = [TaggedDocument(words=text, tags=tags) for text, tags in index_document_pair]
model = Doc2Vec(TRAIN_documents, vector_size=5, window=3, epochs=40, min_count=0, workers=4)

# 문서 기반 학습에서 유사 키워드 찾기
model.wv.most_similar('Sana')
'''
[('Instragram', 0.9933081269264221),
 ('Seungyeon', 0.9928016662597656),
 ('lovely', 0.9915833473205566),
 ('Members', 0.9901887774467468),
 ('Elkie', 0.9897631406784058),
 ('Tzuyu', 0.9880490303039551),
 ('Kr', 0.9869959354400635),
 ('selcas', 0.9867691993713379),
 ('pretty', 0.9863753318786621),
 ('Story', 0.9860913753509521)]
'''

# 게시글을 input으로 주거나 자신에 대한 소개 input으로 문장 작성
sen = input().split() #example: I like Sana

# 모델 기반 벡터 생성
inferred_vector=model.infer_vector(sen)

# 모델 기반 유사한 문서 찾기
sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

for sim in sims[:5]:
    print(data.iloc[int(sim[0])]['author'])
    print('유사도: ', possi)
    print(data.iloc[int(sim[0])]['total'])
    print('')
