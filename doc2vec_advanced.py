# -*- coding: utf-8 -*-
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from scipy import spatial

def reg_tokenizer(x):
    retokenize = RegexpTokenizer("[^\d\W]+")
    return retokenize.tokenize(x)

def user_recommendation(subreddit, username):
    # 데이터 로드
    data = pd.read_csv('./data/combined/{}.csv'.format(subreddit), header = 0, low_memory = False)

    # NaN 수정
    data['title'].fillna('', inplace = True)
    data['selftext'].fillna('', inplace=True)

    # 제목과 내용 합침
    data['total'] = data['title'] + data['selftext']

    # 모델이 있으면 모델 불러오기
    try:
        model = Doc2Vec.load('./doc2vec/{}'.format(subreddit))

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
        model.save('./doc2vec/{}'.format(subreddit))

    # 사용자가 작성한 글의 인덱스 찾기
    idx_list = data[data['author'] == username].index.tolist()

    # 인덱스에 해당하는 selftext의 inferred_vector 구하기
    vectors = []
    for idx in idx_list:
        st = [data.iloc[idx]['selftext']]
        vectors.append(model.infer_vector(st))

    # 모델 기반 유사한 문서 찾고 해당 문서 작성자를 순위별로 딕셔너리화
    user_dict = {key: set() for key in [x for x in range(1,21)]}
    for inferred_vector in vectors:
        sims = model.docvecs.most_similar([inferred_vector], topn=20)
        idx = 0
        for sim in sims:
            idx += 1
            user_dict[idx].add(data.iloc[int(sim[0])]['author'])

    # 딕셔너리에서 본인과 삭제된 사용자를 제외한 유저네임 top 5를 출력
    top5 = []
    for idx in user_dict.keys():
        if len(top5) == 5:
            break
        users = user_dict[idx]
        for u in users:
            if u == username:
                pass
            elif u == '[deleted]':
                pass
            else:
                top5.append(u)

    print(top5)

user_recommendation('twice', 'axinld') #example