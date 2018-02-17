from collections import Counter
import re


def read_main_text(file_name_param):
    file = open(file_name_param, 'r', encoding='utf-8')
    text = file.read()
    text = text.lower()
    #  text = re.sub(r"\s\s+", ' ', text)
    lines = text.splitlines()
    word = ''
    newtext = ''
    for i in range(len(lines)):
        if '--' in lines[i]:
            newtext += ' ' + word + ' ' + str(lines[i])
        else:
            newtext += str(lines[i])
            p = lines[i].split()
            if p:
                word = p[0]
    print(newtext)
    return re.sub(r"[^a-яA-Я|\s]|(\[)|(\])|(_)|(`)", '', newtext)


file_name = 'D:/Research/OOS/On the Origin of Species (keywords, edited).txt'
main_text = read_main_text(file_name)
main_text_counter = Counter(main_text.split())
main_total_N = sum(main_text_counter.values())
filtered_list = Counter({x: v for x, v in main_text_counter.items() if v >= 9})
print(sum(filtered_list.values()), 'tokens')
print(len(list(filtered_list)), 'unique tokens')
