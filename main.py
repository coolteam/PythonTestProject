import re
from collections import Counter


def distinct(sequence):
    seen = set()
    for s in sequence:
        if s not in seen:
            seen.add(s)
            yield s


union_list = []
unique_words = []
for book in range(1, 7):
    file_name = '../Book'+str(book)+'.txt'
    file = open(file_name, 'r', encoding='utf-8')
    text = file.read()
    text = text.lower()
    text = re.sub(r"\s\s+", ' ', text)
    text = re.sub(r"[^a-яA-Я|\s]|(\[)|(\])|(_)", '', text)
    split = text.split()
    items = Counter(split).most_common(60)
    N = len(split)
    freq_list = {}
    for k, v in items:
        freq_list[k] = (v, v/N)
        if k not in unique_words:
            unique_words.append(k)
    union_list.append(freq_list)
    #  print(freq_list['frodo'][1] if 'frodo' in freq_list else 0.0)
print(unique_words)
for word in unique_words:
    if word == 'the':
        sum_freq = sum(x[word][1] for x in union_list)
        for freq in union_list:
            print(freq[word][1]/sum_freq)
#  print(union_list[0]['the'][1]/sum(x['the'][1] for x in union_list))
