#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle

###############################################################################
def vector_indexing(filename):
    word_vectors = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            st_w, co_w, t_sco = line.split()
            if st_w not in word_vectors:
                word_vectors[st_w] = {}
                word_vectors[st_w][co_w] = float(t_sco)
            else:
                word_vectors[st_w][co_w] = float(t_sco)
    return word_vectors
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 3:
        print( "[Usage] %s in-file out-file(pickle)" %sys.argv[0], file=sys.stderr)
        sys.exit()

    filename = sys.argv[1]
    print("processing %s ..." %filename, file=sys.stderr)
    
    # 공기어 벡터 저장 (dictionary of dictionary)
    word_vectors = vector_indexing(filename)

    print("# of entries = %d" %len(word_vectors), file=sys.stderr)

    with open(sys.argv[2],"wb") as fout:
        print("saving %s" %sys.argv[2], file=sys.stderr)
        pickle.dump(word_vectors, fout)
