﻿# Reddit-Submissions-Analysis

### 2019-11-29
- [x] 기본 API 구성
- [x] 데이터 수집 (2019년 1월 ~ 2019년 10월)

### 2019-11-30
- [x] YYYY-MM 으로 인자 주고 데이터 크롤링 하는 방법으로 수정
- [x] 데이터 수집 (2018년 1월 ~ 2018년 12월) : 수동 전처리
- [x] month 변경, 모듈화, 파일 경로 에러 처리, 빈 값 처리

### 2019-12-01 (1)
- [x] 모듈화(서브레딧 이름을 함수 인자로 넘기는 방식으로 변경)
- [x] 함수 변수 변경: end_time은 next_time으로 함수 내부에서 설정, now를 end_time으로 수정
- [x] 파일명 잘못 설정되는 오류 수정
- [x] 데이터 수집 (/r/kpop: 2013년 6월 ~ 2017년 12월, 2019년 11월)
- [x] 데이터 수집 (/r/kpoppers: 2017년 9월 ~ 2017년 12월, 2019년 11월)
- [x] 데이터 수집 (/r/bangtan: 2017년 1월 ~ 2019년 11월)
- [x] 데이터 수동 전처리 (/kpop)
- [x] 200을 수신해도 빈 배열이면 json 파싱이 안 되어 에러 발생

### 2019-12-01 (2)
- [x] 크롤러 버그 수정 (json 파싱에 대해 예외 처리)
- [x] 데이터 수집 (/r/red_velvet: 2014년 1월 ~ 2017년 12월) 
- [x] 데이터 수집 (/r/exo: 2017년 1월 ~ 2019년 11월)
- [x] 데이터 수집 (/r/bangtan: 2014년 1월 ~ 2016년 12월)
- [x] 데이터 수집 (r/twice: 2015년 5월 ~ 2019년 11월)
- [x] 데이터 수집 (r/snsd: 2010년 8월 ~ 2019년 11월)
- [x] 데이터 수집 (r/Got7: 2014년 1월 ~ 2019년 11월)
- [x] 데이터 수집 (r/aiyu: 2012년 2월 ~ 2019년 11월) (아이유)
- [x] 레드벨벳 2018년~2019년 크롤링하기

### 2019-12-02
- [x] 데이터 수집 (/r/red_velvet: 2018년 1월 ~ 2019년 11월)
- [x] 데이터 수집 (/r/MachineLearning: 2009년 8월 ~ 2019년 11월)
- [x] 데이터 수집 (/r/datascience: 2011년 8월 ~ 2016년 12월)
- [x] 데이터 수집 (/r/deeplearning: 2012년 1월 ~ 2019년 11월)
- [x] concat_csv: csv 파일 여러개 하나로 합치는 함수
- [x] 제공하고 싶은 분석 방법: 트래픽 그래프, 언급량 그래프, 워드클라우드, 키워드 연관, SQL 질의 등
- [x] 데이터사이언스 2017년~2019년 크롤링하기

### 2019-12-03
- [x] url 데이터 함께 수집
- [x] concat_csv 일부 수정
- [x] 수집한 데이터에 대해 하나로 결합
- [x] 데이터 수집 (/r/datascience: 2017년 ~ 2019년)
- [x] 데이터 수집 (/r/tensorflow: 2015년 ~ 2019년)
- [x] 데이터 수집 (/r/computercience: 2011년 ~ 2019년)

### 2019-12-05
- [x] find_keyword 작성
- [x] 데이터 저장 경로 수정
- [x] url을 수집한 데이터와 아닌 데이터를 합칠 때 예외처리
- [x] 단어 파싱한 것을 저장해야 할까?
- [x] 글쓴이별 타이틀 + 문서 학습 => 유사도 구하기 (활동이 비슷한 유저)
- [x] find_keyword 키워드 select용 폴더를 따로 만들어서 거기에 저장하는 식으로 수정

### 2019-12-06
- [x] 데이터 수집 (/r/BlackPink: 2016년 ~ 2019년)
- [x] 데이터 수집 (/r/Futurology: 2012년 ~ 2019년)

### 2019-12-07
- [x] 수집한 데이터 전체 HDFS에 업로드
- [x] word2vec_keyword_similarity.py 스킵그램 모델 학습 후 키워드에 대해 유사한 키워드 출력
- [x] doc2vec_user_recommendation.py 문서별 학습 후 유사 키워드와 추천 사용자 출력

### 2019-12-08
- [x] word_cloud.py 파싱한 단어 기반으로 워드 클라우드
- [x] 언급량 그래프 그리려면 title or selftext 처럼 하나에만 있는 게 나으니 수정
- [x] 트래픽 그래프 왜 이상치 들어가는지 확인 (옵션을 제대로 주지 않아서)
- [x] VM에 주피터 노트북 설치 CORS 오류 확인
- [x] 합친 데이터에 대해 date 별로 볼 수 있는 방법 확인

### 2019-12-09
- [x] concat_csv.py 수정: url 수집한 파일에 대해 concat 오류 없게
- [x] 수정된 concat_csv로 데이터 수합
- [x] 크롤러 수정: 스키마 수정, 날짜 알고리즘 수정
- [x] doc2vec_advanced.py 작성한 게시글 바탕으로 유사한 사용자 추천
- [x] 수집한 데이터에 대해 doc2vec 모델 생성
- [x] 'total' 스키마는 여러 분석에 공통으로 사용되므로 전처리할 때 합쳐버리기 -> 데이터 중복이라 그냥 각 단계에서 하는 걸로
- [x] 바뀐 스키마로 다시 크롤링하기 -> 크롤링 코드 하나로 조정할 것
- [x] 크롤러 수정: 디렉토리 이름 받아와서(추가로 크롤링하고 싶으면 폴더 생성해야) -> 마지막으로 저장한 시각 확인하고(없으면 about.json에서 생성 시각 받아오기) -> 거기서부터 현재까지 돌리기 (현재시각이 VM에서 찍히지 않음. 강제로 한달로 조정.)

### 2019-12-10
- [x] find_keyword.py 수정
- [x] 크롤러 멈추는 게 데이터 길이가 아예 없을 때로 수정.
- [x] 크롤러 파일 저장 이름을 수집한 달로 조정, 어떻게 업데이트할지는 고려해야 할 사안인 듯.
- [x] 크롤러에서 현재시각을 어떻게 볼 것인지 생각하기 - 레딧 서버시간
- [x] 제펠린에서 값을 binding할 수 있는 방법도 있는 듯
- [x] 만약 주피터 노트북에서 계속 CORS 에러 날 경우, 결과를 따로 저장하는 식으로 수정.
- [x] concat에서 중복값 삭제
- [x] 아카이브 데이터는 그냥 json으로 dump하는 것 고려 (양이 너무 많아서 메모리 에러)
- [x] SparkMLLib나 Mahaout 도입해서 scalable하게...
- [x] 파이프 예상 (자동화 대상: 크롤링과 전체 데이터 합치기)

* 크롤링
  + data/scrapped의 폴더 이름들을 수집할 서브레딧으로 여긴다. (추가로 크롤링하고 싶으면 이 디렉토리에 폴더 추가할 것)
  + 해당 디렉토리에 대해 마지막으로 크롤링한 시점 이후부터 현재까지 크롤링함.
  + 만약 처음 크롤링한다면 about.json을 참고해 생성지점을 받아온다.
  + 크롤링 단계에서 아스키 문자만 받아오는 전처리는 수행함.

* 전체 데이터 합치기
  + data/combined에 수집한 모든 데이터에 대해 concat 작업 수행

* 분석 (1): SQL 질의
  + 트래픽 그래프
  + find_keyword.py 를 실행하고 (이것은 때때로 바뀌므로 자동화에 포함 X) data/keyword의 파일로 언급량 그래프
  + 기타 SQL 질의

* 분석 (2): 워드클라우드
  + 많이 언급된 단어를 워드클라우드로 표현

* 분석 (3): Word2Vec 유사 키워드
  + word2vec_keyword_similarity.py 로 원하는 서브레딧에 대해 특정 키워드에 대한 연관 키워드를 표현
  + 모델: 스킵그램

* 분석 (4): Doc2Vec
  + doc2vec_user_recommendation.py 로 문서 기반 학습에 대해 유사 키워드 & 자기 소개와 유사한 게시글 출력
  + doc2vec_advanced.py 로 특정 사용자의 작성글 기반 유사한 게시글을 작성한 사용자 추천

### 2019-12-11
- [x] 데이터 수집 확장 (총 229MB => 총 317MB)
- [x] 레딧 서버시간 구하는 함수

#### TODO
- [ ] 크롤러 수정
  * 따로 저장된 파일에서 마지막으로 크롤링한 timestamp 확인
  * 마지막 ~ 현재시각까지 크롤링 / 지금처럼 인자 주고 하는 건 수동용으로 분리
  * 저장 파일이름: yy-mm-마지막timestamp
  * stop point: data의 길이가 0이고, next_time이 현재시각보다 클 때
  * data/scrapped의 폴더 이름들을 수집할 서브레딧으로 여기게 하기
  * 만약 처음 크롤링한다면 about.json을 참고해 생성지점을 받아오기
  * 메타 데이터 갱신 파트 추가
- [ ] 자동화
  * oozie / cron
  * 로컬에서 돌린다면 hdfs에 바로 dump할 수 있게...?
- [ ] 분석
  * Spark mllib 라이브러리 사용해서 작성 코드 변경
  * Angular 사용해서 Zeppline에서 값을 binding 할 수 있도록
  * 로컬에서 주피터 돌린 거 추가하기 OR python 파일 수정해서 결과 파일 저장하기
- [ ] 아카이브 데이터
  * 1만 개씩 잘라서 csv로 저장 (전체 기간에 대해 적용하는 분석)
- [ ] HDFS 폴더 구조 정리하기
- [ ] 함수 분리, main 파트 만들기
- [ ] 발표자료 만들기
- [ ] 보고서 작성하기
- [ ] README.md 파일 정리

### 2019-12-12
- [x] 데이터 수집: gilmore girls, game of thrones

### 2019-12-13
- [x] 데이터 수집: TheGoodPlace
