#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict


###############################################################################
def word_count(filename):
    word_freq = defaultdict(int)
    # word_freq = dict()

    with open(filename, "r", encoding='utf-8') as fin:
        for word in fin.read().split():
            word_freq[word] += 1

            # if word in word_freq:
            #    word_freq[word] += 1
            # else:
            #    word_freq[word] = 1

    return word_freq


###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    result = {}
    cnt = 0
    for input_file in sys.argv[1:]:

        word_freq = word_count(input_file)
        for w, freq in sorted(word_freq.items()):
            if w in result:
                result[w][cnt] = freq
            else:
                result[w] = [0 for _ in range(len(sys.argv[1:]))]
                result[w][cnt] = freq
        cnt += 1

    for w, freq in sorted(result.items()):
        print(f"{w}\t{freq}")


