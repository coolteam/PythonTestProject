from WordInfo import WordInfo
from collections import Counter
import re
import time
import operator
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from enum import Enum
from itertools import islice


class SplitMethod(Enum):
    SIMPLE = 1
    STEMMER = 2
    LEMMATIZER = 3
    NGRAMM = 4


P = 6
minN = 30
minF = 0.000064208
useMinN = True
useMinF = True
splitMethod = SplitMethod.NGRAMM
topResult = 300
nGrammSize = 5

def read_and_prepare(file_name_param):
        file = open(file_name_param, 'r', encoding='utf-8')
        text = file.read()
        text = text.lower()
        text = re.sub(r"\s\s+", ' ', text)
        return re.sub(r"[^a-яA-Я|\s|і]|(\[)|(\])|(_)", '', text)


start_time = time.perf_counter()
general_counter = Counter()
all_text_words = []
counters = []
for book in range(1, P+1):
    #  file_name = 'D:/Research/Chapters/Chapter'+str(book)+'.txt'
    #file_name = 'D:/Research/Books/Book' + str(book) + '.txt'
    #file_name = 'D:/Research/DChapters/Chapter' + str(book) + '.txt'
    file_name = 'D:/Research/BooksUkr/Book' + str(book) + '.txt'
    prepared_text = read_and_prepare(file_name)
    all_text_words = all_text_words + prepared_text.split()
    splitted_text = []
    if splitMethod == splitMethod.NGRAMM:
        text_len = len(prepared_text)
        for shiftIndex in range(0, nGrammSize):
            for startIndex in range(shiftIndex, text_len, nGrammSize):
                splitted_text.append(prepared_text[startIndex:startIndex+nGrammSize])
    else:
        splitted_text = prepared_text.split()
        processed_text = []
        if splitMethod == SplitMethod.STEMMER:
            stemmer = PorterStemmer()
            for word in splitted_text:
                processed_text.append(stemmer.stem(word))
            splitted_text = processed_text
        if splitMethod == SplitMethod.LEMMATIZER:
            lemmatizer = WordNetLemmatizer()
            for word in splitted_text:
                processed_text.append(lemmatizer.lemmatize(word))
            splitted_text = processed_text
    counter = Counter(splitted_text)
    counters.append(counter)
    general_counter += counter
totalN = sum(general_counter.values())
print("total words =", totalN)
print("total word types =", len(general_counter))

general_counter = Counter({k: v for k, v in general_counter.items()
                           if (not useMinN or v >= minN) and (not useMinF or v / totalN >= minF)})
print("filtered word types =", len(general_counter))
words = []
totalNs = []
for x in range(0, P):
    totalNs.append(sum(counters[x].values()))
for key, value in general_counter.items():
    word = WordInfo(key)
    word.n = value
    word.f = value / totalN
    for x in range(0, P):
        word.n_list.append(counters[x][key])
        word.f_list.append(counters[x][key] / totalNs[x])
    words.append(word)
for word in words:
    word.calc_s(P)
    word.calc_s_ran(P)
    word.calc_e_nor()
sorted_words_list = sorted(words, key=operator.attrgetter('e_nor'), reverse=1)
top_words = list(islice(sorted_words_list, topResult))
pre_text = Counter(all_text_words)
#print(pre_text)
unique_list = []
for word in top_words:
    entry = Counter({k: v for k, v in pre_text.items() if (word.key.strip() in k)})
    most_comm = entry.most_common(1)
    val = ''
    if most_comm:
        val = most_comm[0][0]
    if val not in unique_list:
        unique_list.append(val)
        print(word.key, ":", word.e_nor, entry.most_common(3))
print("time elapsed", time.perf_counter()-start_time, "s")
