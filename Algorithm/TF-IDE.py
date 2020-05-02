import pandas as pd # 데이터프레임 사용을 위해
from math import log # IDF 계산을 위해
from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()
# pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))
# pprint(kkma.nouns(u'커다란 에어컨 덕분에 끊는 부대찌개 앞에서도 매우 시원하다. 부대찌개 햄이 매우 맛있음'))
docs = []
# print(kkma.nouns(u'커다란 에어컨 덕분에 끊는 부대찌개 앞에서도 매우 시원하다. 부대찌개 햄이 매우 맛있음'))
docs.append(' '.join(kkma.nouns(u'커다란 에어컨 덕분에 끊는 부대찌개 앞에서도 매우 시원하다. 부대찌개 햄이 매우 맛있음')))
docs.append(' '.join(kkma.nouns(u'가성비 좋고 진짜 맛있는 부대찌개 간만에 먹네요. 가성비 짱! 짱! 짱!')))
docs.append(' '.join(kkma.nouns(u'부대찌개와 햄버거 둘 다 맛있었어요 옛날 맛이었어요  다만 비싼 가격이 아쉬워요')))
# print(docs)
vocab = list(set(w for doc in docs for w in doc.split()))
vocab.sort()

N = len(docs) # 총 문서의 수

def tf(t, d):
    return d.count(t)

def idf(t):
    df = 0
    for doc in docs:
        df += t in doc
    return log(N/(df + 1))

def tfidf(t, d):
    return tf(t,d)* idf(t)

result = []
for i in range(N): # 각 문서에 대해서 아래 명령을 수행
    result.append([])
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]        
        result[-1].append(tf(t, d))

tf_ = pd.DataFrame(result, columns = vocab)
# print(tf_)

result = []
for j in range(len(vocab)):
    t = vocab[j]
    result.append(idf(t))

idf_ = pd.DataFrame(result, index = vocab, columns = ["IDF"])
# print(idf_)

result = []
for i in range(N):
    result.append([])
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]

        result[-1].append(tfidf(t,d))

tfidf_ = pd.DataFrame(result, columns = vocab)
print(tfidf_)