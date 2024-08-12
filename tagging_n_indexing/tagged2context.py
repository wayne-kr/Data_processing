#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import get_morphs_tags as mf
#NNG(일반명사), NNP(고유명사), NR(수사), NNB(의존명사), SL(외국어; 영어), SH(한자), SN(숫자)
#NNG, NNP, SH, SL은 단일어로도 색인어로 추출함(단, SL이 복합어에 속하는 경우 단일어로는 색인어로 추출하지 않음)
#NR, NNB, SN은 단일어로는 색인어로 추출하지 않음
#해결 리스트
#단일어 추출 가능한 것들
#단일어 추출 불가능한 것들 -> 색인어 추출 품사와 만나면 함께 추출 단 짝궁 품사가 단일어 추출 가능한 품사면 먼저 색인어 추가
###############################################################################
# 색인어 (명사, 복합명사 등) 추출
def get_index_terms(mt_list):
    nouns = []
    keep = ''
    cnt = 0
    for i in range(len(mt_list)):

        tag = mt_list[i][1]
        word = mt_list[i][0]

        if tag in ["NNG", "NNP", "SH"]:
            nouns.append(word)
            keep += word
            cnt += 1
        elif tag == "SL":
            keep += word
            cnt += 1
        elif tag in ["NR", "NNB", "SN"]:
            keep += word
            cnt -= 1
        else:
            if keep in nouns:
                keep =''
                cnt = 0
            else:
                if cnt != -1:
                    nouns.append(keep)
                else:
                    keep = ''
                    cnt = 0
    if keep and cnt != -1:
        if not keep in nouns:
            nouns.append(keep)
            keep = ''
            cnt = 0
    else:
        keep = ''
        cnt = 0
    new_nouns = []
    for i in nouns:
        if not i:
            continue
        else:
            new_nouns.append(i)

    return new_nouns

###############################################################################
# Converting POS tagged corpus to a context file
def tagged2context( input_file, output_file):
    try:
        fin = open( input_file, "r", encoding='utf-8')
    except:
        print( "File open error: ", input_file, file=sys.stderr)
        sys.exit()

    try:
        fout = open( output_file, "w", encoding='utf-8')
    except:
        print( "File open error: ", output_file, file=sys.stderr)
        sys.exit()

    for line in fin.readlines():

        # 빈 라인 (문장 경계)
        if line[0] == '\n':
            print("", file=fout)
            continue

        try:
            ej, tagged = line.split(sep='\t')
        except:
            print(line, file=sys.stderr)
            continue

        # 형태소, 품사 추출
        # result : list of tuples
        result = mf.get_morphs_tags(tagged.rstrip())

        # 색인어 추출
        terms = get_index_terms(result)

        # 색인어 출력
        for term in terms:
            print(term, end=" ", file=fout)

    fin.close()
    fout.close()

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".context"
        print( 'processing %s -> %s' %(input_file, output_file), file=sys.stderr)

        # 형태소 분석 파일 -> 문맥 파일
        tagged2context( input_file, output_file)
