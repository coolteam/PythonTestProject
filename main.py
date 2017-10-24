from Word import Word
import re
from collections import Counter
import math
import operator


def distinct(sequence):
    seen = set()
    for s in sequence:
        if s not in seen:
            seen.add(s)
            yield s


union_list = []
unique_words = []
P = 6
for book in range(1, P+1):
    file_name = './Book'+str(book)+'.txt'
    file = open(file_name, 'r', encoding='utf-8')
    text = file.read()
    text = text.lower()
    text = re.sub(r"\s\s+", ' ', text)
    text = re.sub(r"[^a-яA-Я|\s]|(\[)|(\])|(_)", '', text)
    split = text.split()
    items = Counter(split)  # .most_common(100)
    N = len(split)
    freq_list = {}
    for k, v in items.items():
        if v > 30:
            freq_list[k] = (v, v/N)
            if k not in unique_words:
                unique_words.append(k)
    union_list.append(freq_list)
#  print(len(unique_words))
words = {}
for w1 in unique_words:
    w = Word(w1)
    words[w1] = w
for k in words:
    for book in range(0, P):
        #  print(union_list[book])
        value0 = union_list[book][k][0] if k in union_list[book] else 0.0
        value1 = union_list[book][k][1] if k in union_list[book] else 0.0
        #  print(k, value)
        words[k].n_list.append(value1)
        words[k].freq_list.append(value1)
    #  print(freq_list['frodo'][1] if 'frodo' in freq_list else 0.0)
for w in words:
    for f in words[w].freq_list:
        words[w].p_list.append(f/words[w].sum_freq())
for w in words:
    words[w].s = -(1/math.log(P))*words[w].sum_p_ln_p()
    #  print(w, words[w].s)


# for word in unique_words:
#     if word == 'frodo':
#         sum_freq = sum(x[word][1] if word in x else 0.0 for x in union_list)
#         for freq in union_list:
#             print(freq[word][1] if word in freq else 0.0/sum_freq)
#  print(union_list[0]['the'][1]/sum(x['the'][1] for x in union_list))
for w in words:
    words[w].s_ran = 1 - ((P - 1)/2*words[w].sum_n()*math.log(P))
for w in words:
    words[w].e_nor = (1 - words[w].s)/(1 - words[w].s_ran)
for w in sorted(words.values(), key=operator.attrgetter('e_nor')):
    if 0.0 < w.s and 1.5 < w.e_nor: #  <= 0.6:
        print(w.name,  w.s, w.s_ran, w.e_nor,)
