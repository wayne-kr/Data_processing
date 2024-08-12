#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt

###############################################################################
def cosine_similarity(t_vector, c_vector):
    all_keys = set(t_vector.keys()).union(set(c_vector.keys()))

    dot_product = 0
    magnitude1 = 0
    magnitude2 = 0

    for key in all_keys:
        value1 = t_vector.get(key, 0)
        value2 = c_vector.get(key, 0)

        dot_product += value1 * value2
        magnitude1 += value1 ** 2
        magnitude2 += value2 ** 2

    magnitude1 = math.sqrt(magnitude1)
    magnitude2 = math.sqrt(magnitude2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)
###############################################################################
#제약 사항
# - 관련어 후보는 대상어의 공기어들과 공기어들의 공기어들로 한정함
# - 코사인 유사도가 0.001보다 큰 경우만 저장
# - 관련어 후보가 대상어와 같으면 출력하지 않음
# - 관련어 후보가 대상어에 포함되면 출력하지 않음 예) 개인정보/정보 *, 교육부장관/장관 *, 인사청문회/청문회 *
def most_similar_words(word_vectors, target, topN=10):

    result = {}
    for coword1 in word_vectors[target]: #target = 0011호 / coword1 = '노영어'
        if coword1 not in target:
            for coword2 in word_vectors[coword1]:   #coword2 = '어선'/  노영어 {'어선': 4.994, '중국': 4.584, '선원': 4.237, '해경': 4.237, '급': 3.831, '나포': 3.463, '해상': 3.304, '불법': 3.253, '오전': 3.202, '0012호': 3.162, '50987호': 3.162, '2척': 2.998, '조업': 2.993, '서쪽': 2.638, '경찰관': 2.631, '0011호': 2.449, '인천해양경찰서': 2.449, '저인망': 2.449, '선적': 2.447, '선장': 2.441, '칼': 2.428, '소속': 2.372, '쑹허우모': 2.236, '경비함': 2.235, '쌍끌이': 2.235, '옹진군': 2.234, '침범': 2.23, '3명': 2.171, '혐의': 2.068, '과정': 1.915}
                if coword2 not in target:
                    cosine_score = cosine_similarity(word_vectors[target],word_vectors[coword2])
                    if cosine_score > 0.001:
                        result[coword2] = cosine_score
            cosine_score = cosine_similarity(word_vectors[target],word_vectors[coword1])
            result[coword1] = cosine_score


    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]
#0011호	{'노영어': 2.449, '어선': 2.447, '중국': 2.311}
#노영어 {'어선': 4.994, '중국': 4.584, '선원': 4.237, '해경': 4.237, '급': 3.831, '나포': 3.463, '해상': 3.304, '불법': 3.253, '오전': 3.202, '0012호': 3.162, '50987호': 3.162, '2척': 2.998, '조업': 2.993, '서쪽': 2.638, '경찰관': 2.631, '0011호': 2.449, '인천해양경찰서': 2.449, '저인망': 2.449, '선적': 2.447, '선장': 2.441, '칼': 2.428, '소속': 2.372, '쑹허우모': 2.236, '경비함': 2.235, '쌍끌이': 2.235, '옹진군': 2.234, '침범': 2.23, '3명': 2.171, '혐의': 2.068, '과정': 1.915}

###############################################################################
def print_words(words):
    for word, score in words:
        print("%s\t%.3f" %(word, score))
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)

    while True:

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    
        try:
            query = input()
            
        except EOFError:
            print('프로그램을 종료합니다.', file=sys.stderr)
            break
    
        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN=30)
        
        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')
