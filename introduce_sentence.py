# -*- coding: utf-8 -*-
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from scipy import spatial
import sys

def reg_tokenizer(x):
    retokenize = RegexpTokenizer("[^\d\W]+")
    return retokenize.tokenize(x)

def introduce_sentence(subreddit):
    # 모델이 있으면 모델 불러오기
    try:
        model = Doc2Vec.load('/home/maria_dev/project/doc2vec/{}'.format(subreddit))

    # 없을 경우 모델 생성
    except:
        # 데이터 로드
        data = pd.read_csv('/home/maria_dev/project/data/combined/{}'.format(subreddit), header = 0)

        # NaN 수정
        data['title'].fillna('', inplace = True)
        data['selftext'].fillna('', inplace=True)

        # 제목과 내용 합침
        data['total'] = data['title'] + data['selftext']

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

    # 게시글을 input으로 주거나 자신에 대한 소개 input으로 문장 작성
    print("게시글을 input으로 주거나 나에 대한 소개글을 작성하세요. ex. I like Sana.")
    sen = input(">>").split()

    # 모델 기반 벡터 생성
    inferred_vector=model.infer_vector(sen)

    # 모델 기반 유사한 문서 찾기
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

    for sim in sims[:5]:
        print(data.iloc[int(sim[0])]['author'])
        print('')

if __name__ == "__main__":
    # 실행 방법: python introduce_sentence.py "subreddit"
    if len(sys.argv) != 2:
        print("Error! Argument should be 1 strings: subreddit")
        sys.exit(-1)
    sbr = sys.argv[1]
    introduce_sentence(sbr) 