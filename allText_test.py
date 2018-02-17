from collections import Counter
import re


def read_main_text(file_name_param):
    file = open(file_name_param, 'r', encoding='utf-8')
    text = file.read()
    text = text.lower()
    text = text.replace("--", "")
    #text = text.replace("'", "")
    without_punctuation = re.sub(r"[^a-яA-Я|\-|\s]|(\[)|(\])|(_)|(`)", ' ', text)

    words = without_punctuation.split()
    return words


def read_stop_words(file_name_param):
    file = open(file_name_param, 'r', encoding='utf-8')
    text = file.read()
    return text.split()

file_name = 'D:/Research/OOS/On the Origin of Species (glossary).txt'
file_name_s_w = 'D:/Research/OOS/stop_list.txt'
main_text = read_main_text(file_name)
stop_words = read_stop_words(file_name_s_w)
list_a = [w for w in main_text if w not in stop_words]

print(list_a)
main_text_counter = Counter(list_a)
main_total_N = sum(main_text_counter.values())
filtered_list = Counter({x: v for x, v in main_text_counter.items() if v > 9})
print(sum(filtered_list.values()), 'tokens')
print(len(list(filtered_list)), 'unique tokens')
print(filtered_list)
