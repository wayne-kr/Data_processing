#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import sys
import hanja2hangeul_table

h2h_table = hanja2hangeul_table.hanja2hangeul_table

def help(arg):
    print("\n%s Option file(s)"%arg, file=sys.stderr)
    print("\n[Option]", file=sys.stderr)
    print("\t-h1: hangeul", file=sys.stderr)
    print("\t-h2: hangeul(hanja)", file=sys.stderr)
    print("\t-h3: hanja(hangeul)\n", file=sys.stderr)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 1)
# ex) 聖經에 -> 성경에
def hanja2hangeul_str1(STR):
    result = []
    
    for ch in STR:
        if ch in h2h_table: 
            result.append(h2h_table[ch][0])
        else:
            result.append(ch)
        
    return ''.join(result)
    
###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 2)
# ex) 聖經에 -> 성경(聖經)에
#제1, 我等 半島 동포에게 갱생의 길을 열어주신 천황폐하께옵서 一視同仁하시는 높고 넓으신 鴻恩에 감읍하는 바이며
#['제1', '我等', '半島', '동포에게', '갱생의', '길을', '열어주신', '천황폐하께옵서', '一視同仁하시는', '높고', '넓으신', '鴻恩에', '감읍하는', '바이며']
def hanja2hangeul_str2(STR):
    result = []
    lst1 = STR.split()  #['제1,', '我等', '半島', '동포에게', '갱생의', '길을', '열어주신', '천황폐하께옵서', '一視同仁하시는', '높고', '넓으신', '鴻恩에', '감읍하는', '바이며']
    for i in lst1:
        result2 = ''
        hanja = ''
        for j in i:
            if j in h2h_table:  #한자 발견하면 result2에 한글로 변환한 값 저장하고 한자 그 자체는 hanja 문자열에 추가
                result2 += h2h_table[j][0]
                hanja += j
            else: #만약 한글이 나오면 hanja 문자열이 비어있지 않으면 result2에 (hanja)를 추가하고 한글(->j) 추가. 그리고 hanja를 빈문자열로 초기화
                if hanja:
                    word_hanja = f"({hanja})"
                    result2 = result2 + word_hanja + j
                    hanja = ''
                else: #hanja가 빈 문자열이면 result2에 그대로 추가
                    result2 += j
        if hanja:
            result2 += f"({hanja})"
        result.append(result2)
    return ' '.join(result)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 3)
# ex) 聖經에 -> 聖經(성경)에
def hanja2hangeul_str3(STR):
    result = []
    lst1 = STR.split()
    for i in lst1:
        result2 = ''
        hangeul = ''
        for j in i:
            if j in h2h_table:
                result2 += j
                hangeul += h2h_table[j][0]
            else:
                if hangeul:
                    word_hangeul = f"({hangeul})"
                    result2 = result2 + word_hangeul + j
                    hangeul = ''
                else:
                    result2 += j
        if hangeul:
            result2 += f"({hangeul})"
        result.append(result2)
    return ' '.join(result)
####################################################################################
if __name__ == "__main__":

    if len(sys.argv) < 3:
        help(sys.argv[0])
        sys.exit()

    if sys.argv[1] == '-h1':
        func = hanja2hangeul_str1

    elif sys.argv[1] == '-h2':
        func = hanja2hangeul_str2

    elif sys.argv[1] == '-h3':
        func = hanja2hangeul_str3

    else:
        help(sys.argv[0])
        sys.exit()

    for filename in sys.argv[2:]:

        try:
            fp = open(filename, "r")
        except:
            print("File open error:", filename, file=sys.stderr)
        try:
            outfp = open(filename+".out", "w")
        except:
            print("File open error:", filename+".out", file=sys.stderr)

        print("%s -> %s"%(filename, filename+".out"), file=sys.stderr)

        for line in fp:

            result = func(line.rstrip())

            print(result, file=outfp)

        fp.close()
        outfp.close()
