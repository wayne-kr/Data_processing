import sys
import math # sqrt

###############################################################################
def read_frequency(filename):
    freqs = {}
    with open(filename, "r", encoding='utf-8') as file:
        for line in file.readlines():
            w, freq = line.split()
            freqs[w] = freq
    return freqs
###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):
    coword_freqs = {}
    t_scores = {}
    with open(filename, "r", encoding='utf-8') as file:
        for line in file.readlines():
            target_word, coword, freq = line.split()
            coword_freqs[(target_word,coword)] = freq
    for set_words in coword_freqs:
        st_w, co_w = set_words
        if int(coword_freqs[set_words]) >= int(cutoff) and not co_w in st_w:
            E_value = (int(unigram_context[st_w]) * int(unigrams[co_w])) / int(uni_N)
            O_value = int(coword_freqs[set_words])
            t_score = (O_value - E_value) / math.sqrt(O_value)
            if t_score>0:
                t_scores[set_words] = '%.3f'%t_score
        if int(coword_freqs[set_words]) >= int(cutoff) and not st_w in co_w:
            E_value_reverse = (int(unigram_context[co_w]) * int(unigrams[st_w])) / int(uni_N)
            O_value_reverse = int(coword_freqs[set_words])
            t_score_reverse = (O_value_reverse - E_value_reverse) / math.sqrt(O_value_reverse)
            if t_score_reverse > 0:
                t_scores[(co_w,st_w)] = '%.3f'%t_score_reverse

    return t_scores

def print_tscore(filename, t_scores):
    with open(filename, "wt", encoding="utf-8") as file:
        for set_words, freq in sorted(t_scores.items()):
            tar_word, co_word = set_words
            file.write((f"{tar_word.strip()}\t{co_word.strip()}\t{freq.strip()}\n"))

###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산
    
    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"
    
        print("\tLoading %s.1gram" %file_stem, file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")
        
        print("\tLoading %s.1gram_context" %file_stem, file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")
        
        uni_N = unigrams['#Total'] # unigram 빈도 합
        
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)
        
        print_tscore(file_stem+".tscore", t_scores)

