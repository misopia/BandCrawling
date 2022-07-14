
import csv

import re
import nltk
import csv
from nltk.corpus import stopwords
from konlpy.tag import Okt

from collections import defaultdict
from collections import Counter
import pandas as pd


from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from datetime import datetime 
import time
from nltk.corpus import stopwords


####텍스트 읽어오기####
##한국어 텍스트##
# 딕셔너리 리스트 생성
dictData = defaultdict(list)

with open('./write2022-07-09_014016.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        if len(row) > 1 :
            #line.append(row[1])
            if row[1].find("가입했습니다") == -1 and row[1] != "":
                # 전체 데이터 수집
                dictData['ALL'].append([row[1]])

                # 동일 년도별 데이터 구분 ex)2022년 문장 모음
                findIdx = row[0].find("-")
                dictData[row[0][0:findIdx]].append([row[1]])

                # 동일 월별 데이터 구분 ex)2022-07 문장 모음
                findIdx = row[0].find("-", 5)
                dictData[row[0][0:findIdx]].append([row[1]])

print('csv파일 읽기 끝')


###특수문자 제거하기###
compile = re.compile("[^ ㄱ-ㅣ가-힣A-Za-z]+")
for datalist in dictData:
    datamaxIdx = len(dictData[datalist])
    for dataIdx in range(0, datamaxIdx) :
        dictData[datalist][dataIdx][0] = compile.sub("",dictData[datalist][dataIdx][0])
        #line[i] = a

print('특수문자 제거하기 끝')


###문장분석###
##한국어##
okt = Okt()
final_result = defaultdict(list)
for datalist in dictData:
    datamaxIdx = len(dictData[datalist])
    
    final_result[datalist].append([])
    for dataIdx in range(0, datamaxIdx) :
        result = []

        dataLine = dictData[datalist][dataIdx][0].lower()

        result = okt.nouns(dataLine)

        for dataResult in result:
            final_result[datalist][0].append(dataResult)
        

print('문장분석 끝')



###불용어 제거하기###
stopwords = ['이', '있', '하', '것', '들', '그', '되', '수', '이', '보', '않', '없', '나', '사람', '주', '아니', 
             '등', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', '말', '일', '그렇', '위하', '및', '시', '건', '월', '돈', '광고', '투데이', 
             '출처', '제품', '뉴스', '후', '위', '중', '더', '회', '감']
for final_resultTmp in final_result:
    clean_words = [] 
        

    for token in final_result[final_resultTmp][0] :
        if token not in stopwords: #불용어 제거
            clean_words.append(token)

    final_result[final_resultTmp][0] = clean_words


print('불용어 제거하기 끝')



###텍스트에서 많이 나온 단어###

#많이 사용한 단어 csv저장
f = open("Keword_{0}.csv".format(datetime.now().strftime('%Y-%m-%d_%H%M%S')),'w', newline='')
wr = csv.writer(f)



###텍스트에서 많이 나온 단어###
for finalResultTmp in final_result:
    korean = pd.Series(final_result[finalResultTmp][0]).value_counts().head(30)
    
    print("{0} Top 30".format(finalResultTmp))
    print(korean)
    print("\n")

    wr.writerow([finalResultTmp,korean])

    dtKorean = korean.to_frame()


    c = Counter(final_result[finalResultTmp][0])

    wc = WordCloud(font_path='malgun', width=400, height=400, scale=2.0, max_font_size=150, background_color='white')
    gen = wc.generate_from_frequencies(c)
    plt.figure()
    plt.imshow(gen)
    wc.to_file('{0}.png'.format(finalResultTmp))



f.close()


print('끝')

출처: https://kjk92.tistory.com/91 [IT_NOTEPAD:티스토리]