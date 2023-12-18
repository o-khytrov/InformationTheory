import math

import numpy as np
import pandas as pd


def distance(word1, word2):
    """
    Дистанція Хемінга

    :param word1:
    :param word2:
    :return:
    """
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))
    d = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            d += 1
    return d


def build_distance_matrix(codes: []) -> [[]]:
    """
    Побудова матриці кодових відстаней

    :param codes: Список кодових комбінацій
    :return: Матриця кодових відстаней
    """
    distance_matrix = []
    for i, a in enumerate(codes):
        distance_matrix.append([])
        for j, a1 in enumerate(codes):
            dist = distance(a, a1)
            distance_matrix[i].append(dist)
    return distance_matrix


def build_channel_matrix(codes: [], pe: float) -> [[]]:
    """
    Побудова канальної матриці P(bj/ai)

    :param codes: список кодових комбінацій
    :param pe:ймовірність спотворення елементарного символу в каналі зв'зку
    :return: матриця P(bj/ai)
    """
    channel_matrix = np.zeros((len(codes), len(codes)))
    for i, code_a in enumerate(codes):
        for j, code_b in enumerate(codes):
            if i != j:
                d = distance(code_a, code_b)
                n = len(code_b)
                probability = pe ** d * (1 - pe) ** (n - d)
                channel_matrix[i][j] = probability

    for i in range(len(codes)):
        column_sum = 0
        for j in range(len(codes)):
            column_sum += channel_matrix[j][i]
        channel_matrix[i][i] = 1 - (column_sum - channel_matrix[i][i])
    return channel_matrix


def get_undetected_error_probabilities(channel_matrix: [[]]) -> []:
    """
    ймовірність невиявленої помилки Pнп для заданого кодового відображення.

    :param channel_matrix:
    :return: Канальна матриця P(bj/ai)
    """
    undetected_error_probabilities = []
    for i in range(len(channel_matrix)):
        undetected_error_probabilities.append(1 - channel_matrix[i][i])
    return undetected_error_probabilities


def build_conditional_entropy_matrix(channel_matrix):
    conditional_entropy_matrix = np.zeros((len(channel_matrix), len(channel_matrix)))
    for i in range(len(channel_matrix)):
        for j in range(len(channel_matrix)):
            conditional_entropy_matrix[i][j] = math.log2(channel_matrix[i][j]) * channel_matrix[i][j] * -1
    return conditional_entropy_matrix


def save_latex(df: pd.DataFrame, name, columns={}, index={}):
    temp_df = df.rename(columns=columns, index=index)
    with open(f'./latex_tables/{name}.tex', 'w') as tf:
        tf.write(temp_df.to_latex())


# Python3 program for Shannon Fano Algorithm


# declare structure node
class node:
    def __init__(self) -> None:
        # for storing symbol
        self.sym = ''
        # for storing probability or frequency
        self.pro = 0.0
        self.arr = [0] * 20
        self.top = 0

    def code(self):
        c = ""
        for j in range(self.top + 1):
            c += str(self.arr[j])
        return c


p = [node() for _ in range(20)]


# function to find shannon code
def shannon(l, h, p):
    pack1 = 0;
    pack2 = 0;
    diff1 = 0;
    diff2 = 0
    if ((l + 1) == h or l == h or l > h):
        if (l == h or l > h):
            return
        p[h].top += 1
        p[h].arr[(p[h].top)] = 0
        p[l].top += 1
        p[l].arr[(p[l].top)] = 1

        return

    else:
        for i in range(l, h):
            pack1 = pack1 + p[i].pro
        pack2 = pack2 + p[h].pro
        diff1 = pack1 - pack2
        if (diff1 < 0):
            diff1 = diff1 * -1
        j = 2
        while (j != h - l + 1):
            k = h - j
            pack1 = pack2 = 0
            for i in range(l, k + 1):
                pack1 = pack1 + p[i].pro
            for i in range(h, k, -1):
                pack2 = pack2 + p[i].pro
            diff2 = pack1 - pack2
            if (diff2 < 0):
                diff2 = diff2 * -1
            if (diff2 >= diff1):
                break
            diff1 = diff2
            j += 1

        k += 1
        for i in range(l, k + 1):
            p[i].top += 1
            p[i].arr[(p[i].top)] = 1

        for i in range(k + 1, h + 1):
            p[i].top += 1
            p[i].arr[(p[i].top)] = 0

        # Invoke shannon function
        shannon(l, k, p)
        shannon(k + 1, h, p)


# Function to sort the symbols
# based on their probability or frequency
def sortByProbability(n, p):
    temp = node()
    for j in range(1, n):
        for i in range(n - 1):
            if p[i].pro > p[i + 1].pro:
                temp.pro = p[i].pro
                temp.sym = p[i].sym

                p[i].pro = p[i + 1].pro
                p[i].sym = p[i + 1].sym

                p[i + 1].pro = temp.pro
                p[i + 1].sym = temp.sym


# function to display shannon codes
def display(n, p):
    print("\n\n\n\tSymbol\tProbability\tCode", end='')
    for i in range(n - 1, -1, -1):
        print("\n\t", p[i].sym, "\t\t", p[i].pro, "\t", end='')
        print(p[i].code())
        #for j in range(p[i].top + 1):
        #    print(p[i].arr[j], end='')
