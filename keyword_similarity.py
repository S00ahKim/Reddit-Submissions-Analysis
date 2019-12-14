# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
from nltk.tokenize import RegexpTokenizer
from gensim.models import Word2Vec
import sys

def reg_tokenizer(x):
    # 토크나이저: 숫자가 아닌 문자만 처리
    retokenize = RegexpTokenizer("[^\d\W]+")
    return retokenize.tokenize(x)

def keyword_similarity(subreddit, keyword, model):
    # 데이터 로드
    data = pd.read_csv('/home/maria_dev/project/data/combined/{}.csv'.format(subreddit), header = 0)

    # NaN 수정
    data['title'].fillna('', inplace = True)
    data['selftext'].fillna('', inplace=True)

    # 제목과 내용 합침
    data['total'] = data['title'] + data['selftext']

    # 토크나이저 적용
    data['token'] = data['total'].apply(reg_tokenizer)

    # 이중 리스트로 구성 (for gensim input)
    sentences = data['token'].tolist()

    if model == "word":
        # Word2Vec
        Skip_Gram_model = Word2Vec(sentences, size=100, window=2, min_count=10, workers=8, iter=1000, sg=1)
        words = Skip_Gram_model.wv.index2word
        vectors = Skip_Gram_model.wv.vectors

        # 학습한 데이터에서 키워드에 대해 유사도 높은 단어
        ms = Skip_Gram_model.wv.most_similar(keyword)
        '''
        [('Dahyun', 0.40760713815689087),
        ('Mina', 0.3778870701789856),
        ('No', 0.3690928816795349),
        ('Jihyo', 0.35880550742149353),
        ('smiling', 0.35619568824768066),
        ('Acuvue', 0.35459190607070923),
        ('cute', 0.35317373275756836),
        ('Momo', 0.32426917552948),
        ('selca', 0.31829380989074707),
        ('Chaeyoung', 0.31558603048324585)]
        '''
        # 출력
        for s in ms:
            print('by word2vec: keyword: ', s[0], ' similarity: ', s[1])
    else:
        # 모델이 있으면 모델 불러오기
        try:
            model = Doc2Vec.load('/home/maria_dev/project/doc2vec/{}'.format(subreddit))

        # 없을 경우 모델 생성
        except:
            # 토크나이저: 숫자가 아닌 문자만 처리
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

            # 모델 저장
            model.save('/home/maria_dev/project/doc2vec/{}'.format(subreddit))
        
        # doc2vec 모델에서 유사한 키워드
        ms = model.wv.most_similar(keyword)

        # 출력
        for s in ms:
            print('by word2vec: keyword: ', s[0], ' similarity: ', s[1])

if __name__ == "__main__":
    # 실행 방법: python word2vec_keyword_similarity.py "subreddit" "keyword" "model"
    if len(sys.argv) != 4:
        print("Error! Argument should be 3 strings: subreddit, keyword, model")
        sys.exit(-1)
    sbr = sys.argv[1]
    kwd = sys.argv[2]
    mdl = sys.argv[3]
    keyword_similarity(sbr, kwd, mdl)