from Word import Word
import re
from collections import Counter
import math
import operator


    def sort_by_s(word):
    return word.get_s()


union_list = []
unique_words = []
P = 6
for book in range(1, P+1):
    file_name = 'D:/Research/Books/Book'+str(book)+'.txt'
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
        #  if v > 10:
            freq_list[k] = (v, v/N)
            if k not in unique_words:
                unique_words.append(k)
    union_list.append(freq_list)
#  print(len(unique_words))
words = {}
for w1 in unique_words:
    w = Word(w1)
    for book in range(0, P):
        value0 = union_list[book][w1][0] if w1 in union_list[book] else 0.0
        value1 = union_list[book][w1][1] if w1 in union_list[book] else 0.0
        w.n_list.append(value0)
        w.freq_list.append(value1)
    words[w1] = w
    #  print(words[w1].name, words[w1].n_list, words[w1].freq_list, words[w1].sum_n())
for w in words:
    for f in words[w].freq_list:
        words[w].p_list.append(f/words[w].sum_freq() if words[w].sum_freq() > 0 else 0.0)
for w in words:
    words[w].s = -(1.0/math.log(P))*words[w].sum_p_ln_p()
for w in words:
    words[w].s_ran = 1.0 - ((P - 1.0)/(2.0*words[w].sum_n()*math.log(P)))
for w in words:
    words[w].e_nor = (1.0 - words[w].s)/(1.0 - words[w].s_ran) if words[w].s_ran != 1.0 else 0.0
for w in sorted(words.values(), key=operator.attrgetter('e_nor'), reverse=1):
    if 0.0 < w.s < 0.9999:  # and 1.5 < w.e_nor: #  <= 0.6:
        print(w.name,  w.s, w.s_ran, w.e_nor, w.sum_freq())
#   print(words[w].name, words[w].n_list, words[w].freq_list, words[w].sum_n())
