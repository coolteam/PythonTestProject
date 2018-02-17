import math


class WordInfo:
    """Class for containing word info"""

    def __init__(self, key):
        self.key = key
        self.f = 0.0
        self.f_list = []
        self.n = 0
        self.n_list = []
        self.s = 0.0
        self.s_ran = 0.0
        self.e_nor = 0.0
        self.text_words = []

    def sum_f(self):
        return sum(self.f_list)

    def sum_n(self):
        return sum(self.n_list)

    def sum_p_ln_p(self):
        result = 0.0
        for f in self.f_list:
            p = f / self.sum_f()
            result += p*math.log(p) if p > 0.0 else 0.0
        return result

    def calc_s(self, p):
        self.s = -(1.0 / math.log(p))*self.sum_p_ln_p()

    def calc_s_ran(self, p):
        self.s_ran = 1.0 - ((p - 1.0) / (2.0 * self.sum_n() * math.log(p)))

    def calc_e_nor(self):
        self.e_nor = (1.0 - self.s)/(1.0 - self.s_ran) if self.s_ran != 1.0 else 0.0
