#!/usr/bin/env python3
# coding: utf-8

import sys

###############################################################################
# 형태소 분석 결과로부터 형태소와 품사들을 알아냄
# return value : (형태소, 품사)로 구성된 tuple들의 list
def get_morphs_tags(tagged):
    result = []
    word = ''
    morp = ''
    change = 0  # change가 0이면 word에 추가, 1이면 형태소(morp)에 추가
    for i in range(len(tagged)):
        if tagged[i] == '+' and tagged[i-1] != '+':
            result.append((word,morp))
            word = ''
            morp = ''
            change = 0
        else:
            if tagged[i] != '/':
                if change == 0:
                    word += tagged[i]
                else:
                    morp += tagged[i]
            elif tagged[i] ==  tagged[i+1] == '/':
                if change == 0:
                    word += tagged[i]
                else:
                    morp += tagged[i]
            else:
                change = 1
    result.append((word, morp))
    return result
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1], encoding='utf-8') as fin:

        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2:
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())

            for morph, tag in result:
                print(morph, tag, sep='\t')
