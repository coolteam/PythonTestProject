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
for book in range(1, 7):
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
words = {}
for w1 in unique_words:
    w = Word(w1)
    words[w1] = w
for k in words:
    for book in range(0, 6):
        #  print(union_list[book])
        value = union_list[book][k][1] if k in union_list[book] else 0.0
        #  print(k, value)
        words[k].freq_list.append(value)
    #  print(freq_list['frodo'][1] if 'frodo' in freq_list else 0.0)
for w in words:
    for f in words[w].freq_list:
        words[w].p_list.append(f/words[w].sum_freq())
for w in words:
    words[w].s = -(1/math.log(6))*words[w].sum_p_ln_p()
    #  print(w, words[w].s)

for w in sorted(words.values(), key=operator.attrgetter('s')):
    if w.s > 0.0 and w.s < 0.5:
        print(w.name, w.s)
# for word in unique_words:
#     if word == 'frodo':
#         sum_freq = sum(x[word][1] if word in x else 0.0 for x in union_list)
#         for freq in union_list:
#             print(freq[word][1] if word in freq else 0.0/sum_freq)
#  print(union_list[0]['the'][1]/sum(x['the'][1] for x in union_list))
