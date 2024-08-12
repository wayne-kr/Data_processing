#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations


###############################################################################
def print_word_freq(filename, word_freq):
    with open(filename, "wt", encoding='utf-8') as outfin:
        for w, freq in sorted(word_freq.items()):
            print("%s\t%d" % (w, freq), file=outfin)

###############################################################################
#Total 설정하기
def get_coword_freq(filename):
    word_freq = defaultdict(int)
    word_context_size = defaultdict(int)
    coword_freq = defaultdict(int)
    word_freq["#Total"] = 0

    #word_context_size
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin.readlines():
            for i in set(line.split()):
                word_context_size[i] += len(set(line.split()))

    #word_freq
    with open(filename, "r", encoding='utf-8') as fin:
        context_split = fin.read().split()
        for word in context_split:
            word_freq[word] += 1
            word_freq["#Total"] += 1

    #coword_freq
    #중복 제거(set) / 조합 이용
    with open(filename, "r", encoding='utf-8') as fin:
        for line in fin.readlines():
            items = set(line.split())
            comb = list(combinations(items, 2))
            for target, coword in comb:
                if target < coword:
                    coword_freq[(target,coword)] += 1
                else:
                    coword_freq[(coword,target)] += 1

    return word_freq, coword_freq, word_context_size

###############################################################################
def print_coword_freq(filename, coword_freq):
    with open(filename, "wt", encoding='utf-8') as outfin:
        for cw, freq in sorted(coword_freq.items()):
            word_1, word_2 = cw
            print(f"{word_1}\t{word_2}\t{freq}", file=outfin)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:

        print('processing %s' % input_file, file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos]  # ex) "2017.tag.context" -> "2017"

        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem + ".1gram", word_freq)

        # bigram(co-word) 출력
        print_coword_freq(file_stem + ".2gram", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem + ".1gram_context", word_context_size)
