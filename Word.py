import math


class Word:
    """Class for containing word indicators"""
    wordCount = 0

    def __init__(self, name):
        self.name = name
        self.freq = 0.0
        self.freq_list = []
        self.p = 0.0
        self.p_list = []
        self.s = 0
        Word.wordCount += 1

    def sum_freq(self):
        return sum(self.freq_list)

    def sum_p_ln_p(self):
        result = 0
        for p in self.p_list:
            result += p*math.log(p) if p > 0 else 0
        return result
