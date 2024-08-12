import json

# JSON 형식의 데이터 불러오기
with open('new_data.JSON', 'r', encoding='utf-8') as f:
    data = json.load(f)
contents = []
with open('new_text.txt', 'r', encoding='utf-8') as file:
    for line in file:
        contents.append(line.replace('\n', ''))
# 텍스트 파일에 저장할 문자열 초기화
output_text = ""

# 각 문장에 대해 처리
for content, sentence in zip(contents, data['sentences']):
    if content != "공백":
        origin = content
        tagged = sentence['tokens'][0]['tagged']  # 형태소 분석 결과
        if "VCN" in tagged:
            tagged = tagged.replace("VCN", "VCP")
        elif "MMA" in tagged:
            tagged = tagged.replace("MMA", "MM")
        elif "MMN" in tagged:
            tagged = tagged.replace("MMN", "MM")
        elif "MMD" in tagged:
            tagged = tagged.replace("MMD", "MM")
        elif "JKC" in tagged:
            tagged = tagged.replace("JKC", "JKS")
        elif "JC" in tagged:
            tagged = tagged.replace("JC", "JKB")
        elif "EF" in tagged:
            tagged = tagged.replace("EF", "EM")
        elif "EC" in tagged:
            tagged = tagged.replace("EC", "EM")
        elif "XR" in tagged:
            tagged = tagged.replace("XR", "NNG")
        else:
            pass
        output_text += f"{origin}\t{tagged}\n"
    else:
        output_text += "\n"


#가공된 문자열을 텍스트 파일에 저장
with open('smaple06.txt', 'w', encoding='utf-8') as f:
    f.write(output_text)


#VCN -> VCP
#MMN/MMA/MMD -> MM
#JKC -> JKS
#JC -> JKB
#EF/EC -> EM
#XR -> NNG