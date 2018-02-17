from collections import Counter
from os.path import join
from itertools import islice
import re
import os
import math
import operator
import time


printFc = True
printTfIdf = False
minN = 30
minF = 0.0#0.000064208
topResult = 1000


def read_main_text(file_name_param):
    file = open(file_name_param, 'r', encoding='utf-8')
    text = file.read()
    text = text.lower()
    text = re.sub(r"\s\s+", ' ', text)
    return re.sub(r"[^a-яA-Я|\s]|(\[)|(\])|(_)|(`)", '', text)


def read_corpora(main_folder_path):
    texts = []
    for root, dirs, files in os.walk(main_folder_path):
        for name in files:
            file = open(join(root, name), 'r', encoding='utf-8')
            text = file.read()
            text = text.lower()
            text = re.sub(r"\s\s+", ' ', text)
            texts.append(re.sub(r"[^a-яA-Я|\s]|(\[)|(\])|(_)|(`)", '', text))
    return texts


def write_tesult(file_name_param, result_list):
    file = open(file_name_param, 'w', encoding='utf-8')
    file.writelines(result_list)

start_time = time.perf_counter()
file_name = 'D:/Research/eng_corpora_short/Charles Darwin/On the Origin of Species.txt'
corpora_path = 'D:/Research/eng_corpora_short'
main_text = read_main_text(file_name)
main_text_counter = Counter(main_text.split())
main_total_N = sum(main_text_counter.values())
texts = read_corpora(corpora_path)
counters = []
universe_counter = main_text_counter;
N = len(texts)
for text in texts:
    c = Counter(text.split())
    counters.append(c)
    universe_counter = universe_counter + c
freq_by_avg_freq_list = {}
tf_idf_list = {}
count = 0
main_list = ({x: v for x, v in main_text_counter.items() if v >= minN and v/main_total_N >= minF})
corpora_word_tokens_count = sum(universe_counter.values())
print(corpora_word_tokens_count)
for word in main_list:
    f_i = main_text_counter[word]/main_total_N
    avg = 1.0 / corpora_word_tokens_count
    value = f_i / avg
    #if value == N:
    #    value = main_text_counter[word]
    freq_by_avg_freq_list[word] = value
    doc_count = sum(1 for x in counters if word in x)
    idf = math.log(N / doc_count)
    tf_idf_list[word] = f_i * idf
    count += (1 if value >= N else 0)
print(count)
result = []
filtered_counter = freq_by_avg_freq_list if printFc else tf_idf_list
print(filtered_counter)
sorted_dict = sorted(filtered_counter.items(), key=operator.itemgetter(1), reverse=1)
mult = sum(v for k, v in islice(sorted_dict, topResult))
result.append("word, rang, value, weighted_value\n")
i = 1
for k, v in islice(sorted_dict, topResult):
    result.append("{}, {}, {}, {}\n".format(k, i, v, v * (1.0/mult)))
    print(k, ":", v * (1.0/mult))
    i = i + 1
file_name_fi_fc = 'D:/Research/relative_fi_fc_LOTR.txt'
file_name_tf_idf = 'D:/Research/relative_tf_idf_LOTR.txt'
write_tesult(file_name_fi_fc if printFc else file_name_tf_idf, result)
print("time elapsed", time.perf_counter()-start_time, "s")
