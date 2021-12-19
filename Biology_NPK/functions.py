from config import *
from exceptions import *
from typing import Optional
import numpy as np


# TODO -> Добавить комментарии в функции
# TODO -> Обработка ошибок(кастомных)
def count_cell_score(s1: str, s2: str, mode: int = 0) -> Optional[int]:
    """Функция для подсчёта стоимости текущей ячейки."""

    """ВАЖНО! Передаются только символы, а не строки"""
    # TODO -> Сделать список в конфиге возможных таблиц выравнивания(режимов)(Возможно) + режими - не номера, а слова[Union]
    # TODO -> Либо гарантировать, что сюда передаются только символы(Сомнительно)
    if len(s1) != 1 or len(s2) != 1 or mode not in [0, 1]:
        # TODO -> Делать что-то другое. Возможно добавить свой обработчик ошибок!
        return None

    if mode == 1:
        """Используем базовую схему"""
        if '*' in [s1, s2]:
            return -1
        elif s1 == s2:
            return 1
        else:
            return -1
    elif mode == 0:
        """Используем BLOSUM62"""
        # TODO -> Хранить в коде не как словарь, а выгружать из файла(Возможно)
        # TODO -> Добавить значение по умолчанию!
        align = {'A': {'A': '4', 'R': '-1', 'N': '-2', 'D': '-2', 'C': '0', 'Q': '-1', 'E': '-1', 'G': '0', 'H': '-2', 'I': '-1', 'L': '-1', 'K': '-1', 'M': '-1', 'F': '-2', 'P': '-1', 'S': '1', 'T': '0', 'W': '-3', 'Y': '-2', 'V': '0', 'B': '-2', 'Z': '-1', 'X': '0', '*': '-4'},
                 'R': {'A': '-1', 'R': '5', 'N': '0', 'D': '-2', 'C': '-3', 'Q': '1', 'E': '0', 'G': '-2', 'H': '0', 'I': '-3', 'L': '-2', 'K': '2', 'M': '-1', 'F': '-3', 'P': '-2', 'S': '-1', 'T': '-1', 'W': '-3', 'Y': '-2', 'V': '-3', 'B': '-1', 'Z': '0', 'X': '-1', '*': '-4'},
                 'N': {'A': '-2', 'R': '0', 'N': '6', 'D': '1', 'C': '-3', 'Q': '0', 'E': '0', 'G': '0', 'H': '1', 'I': '-3', 'L': '-3', 'K': '0', 'M': '-2', 'F': '-3', 'P': '-2', 'S': '1', 'T': '0', 'W': '-4', 'Y': '-2', 'V': '-3', 'B': '3', 'Z': '0', 'X': '-1', '*': '-4'},
                 'D': {'A': '-2', 'R': '-2', 'N': '1', 'D': '6', 'C': '-3', 'Q': '0', 'E': '2', 'G': '-1', 'H': '-1', 'I': '-3', 'L': '-4', 'K': '-1', 'M': '-3', 'F': '-3', 'P': '-1', 'S': '0', 'T': '-1', 'W': '-4', 'Y': '-3', 'V': '-3', 'B': '4', 'Z': '1', 'X': '-1', '*': '-4'},
                 'C': {'A': '0', 'R': '-3', 'N': '-3', 'D': '-3', 'C': '9', 'Q': '-3', 'E': '-4', 'G': '-3', 'H': '-3', 'I': '-1', 'L': '-1', 'K': '-3', 'M': '-1', 'F': '-2', 'P': '-3', 'S': '-1', 'T': '-1', 'W': '-2', 'Y': '-2', 'V': '-1', 'B': '-3', 'Z': '-3', 'X': '-2', '*': '-4'},
                 'Q': {'A': '-1', 'R': '1', 'N': '0', 'D': '0', 'C': '-3', 'Q': '5', 'E': '2', 'G': '-2', 'H': '0', 'I': '-3', 'L': '-2', 'K': '1', 'M': '0', 'F': '-3', 'P': '-1', 'S': '0', 'T': '-1', 'W': '-2', 'Y': '-1', 'V': '-2', 'B': '0', 'Z': '3', 'X': '-1', '*': '-4'},
                 'E': {'A': '-1', 'R': '0', 'N': '0', 'D': '2', 'C': '-4', 'Q': '2', 'E': '5', 'G': '-2', 'H': '0', 'I': '-3', 'L': '-3', 'K': '1', 'M': '-2', 'F': '-3', 'P': '-1', 'S': '0', 'T': '-1', 'W': '-3', 'Y': '-2', 'V': '-2', 'B': '1', 'Z': '4', 'X': '-1', '*': '-4'},
                 'G': {'A': '0', 'R': '-2', 'N': '0', 'D': '-1', 'C': '-3', 'Q': '-2', 'E': '-2', 'G': '6', 'H': '-2', 'I': '-4', 'L': '-4', 'K': '-2', 'M': '-3', 'F': '-3', 'P': '-2', 'S': '0', 'T': '-2', 'W': '-2', 'Y': '-3', 'V': '-3', 'B': '-1', 'Z': '-2', 'X': '-1', '*': '-4'},
                 'H': {'A': '-2', 'R': '0', 'N': '1', 'D': '-1', 'C': '-3', 'Q': '0', 'E': '0', 'G': '-2', 'H': '8', 'I': '-3', 'L': '-3', 'K': '-1', 'M': '-2', 'F': '-1', 'P': '-2', 'S': '-1', 'T': '-2', 'W': '-2', 'Y': '2', 'V': '-3', 'B': '0', 'Z': '0', 'X': '-1', '*': '-4'},
                 'I': {'A': '-1', 'R': '-3', 'N': '-3', 'D': '-3', 'C': '-1', 'Q': '-3', 'E': '-3', 'G': '-4', 'H': '-3', 'I': '4', 'L': '2', 'K': '-3', 'M': '1', 'F': '0', 'P': '-3', 'S': '-2', 'T': '-1', 'W': '-3', 'Y': '-1', 'V': '3', 'B': '-3', 'Z': '-3', 'X': '-1', '*': '-4'},
                 'L': {'A': '-1', 'R': '-2', 'N': '-3', 'D': '-4', 'C': '-1', 'Q': '-2', 'E': '-3', 'G': '-4', 'H': '-3', 'I': '2', 'L': '4', 'K': '-2', 'M': '2', 'F': '0', 'P': '-3', 'S': '-2', 'T': '-1', 'W': '-2', 'Y': '-1', 'V': '1', 'B': '-4', 'Z': '-3', 'X': '-1', '*': '-4'},
                 'K': {'A': '-1', 'R': '2', 'N': '0', 'D': '-1', 'C': '-3', 'Q': '1', 'E': '1', 'G': '-2', 'H': '-1', 'I': '-3', 'L': '-2', 'K': '5', 'M': '-1', 'F': '-3', 'P': '-1', 'S': '0', 'T': '-1', 'W': '-3', 'Y': '-2', 'V': '-2', 'B': '0', 'Z': '1', 'X': '-1', '*': '-4'},
                 'M': {'A': '-1', 'R': '-1', 'N': '-2', 'D': '-3', 'C': '-1', 'Q': '0', 'E': '-2', 'G': '-3', 'H': '-2', 'I': '1', 'L': '2', 'K': '-1', 'M': '5', 'F': '0', 'P': '-2', 'S': '-1', 'T': '-1', 'W': '-1', 'Y': '-1', 'V': '1', 'B': '-3', 'Z': '-1', 'X': '-1', '*': '-4'},
                 'F': {'A': '-2', 'R': '-3', 'N': '-3', 'D': '-3', 'C': '-2', 'Q': '-3', 'E': '-3', 'G': '-3', 'H': '-1', 'I': '0', 'L': '0', 'K': '-3', 'M': '0', 'F': '6', 'P': '-4', 'S': '-2', 'T': '-2', 'W': '1', 'Y': '3', 'V': '-1', 'B': '-3', 'Z': '-3', 'X': '-1', '*': '-4'},
                 'P': {'A': '-1', 'R': '-2', 'N': '-2', 'D': '-1', 'C': '-3', 'Q': '-1', 'E': '-1', 'G': '-2', 'H': '-2', 'I': '-3', 'L': '-3', 'K': '-1', 'M': '-2', 'F': '-4', 'P': '7', 'S': '-1', 'T': '-1', 'W': '-4', 'Y': '-3', 'V': '-2', 'B': '-2', 'Z': '-1', 'X': '-2', '*': '-4'},
                 'S': {'A': '1', 'R': '-1', 'N': '1', 'D': '0', 'C': '-1', 'Q': '0', 'E': '0', 'G': '0', 'H': '-1', 'I': '-2', 'L': '-2', 'K': '0', 'M': '-1', 'F': '-2', 'P': '-1', 'S': '4', 'T': '1', 'W': '-3', 'Y': '-2', 'V': '-2', 'B': '0', 'Z': '0', 'X': '0', '*': '-4'},
                 'T': {'A': '0', 'R': '-1', 'N': '0', 'D': '-1', 'C': '-1', 'Q': '-1', 'E': '-1', 'G': '-2', 'H': '-2', 'I': '-1', 'L': '-1', 'K': '-1', 'M': '-1', 'F': '-2', 'P': '-1', 'S': '1', 'T': '5', 'W': '-2', 'Y': '-2', 'V': '0', 'B': '-1', 'Z': '-1', 'X': '0', '*': '-4'},
                 'W': {'A': '-3', 'R': '-3', 'N': '-4', 'D': '-4', 'C': '-2', 'Q': '-2', 'E': '-3', 'G': '-2', 'H': '-2', 'I': '-3', 'L': '-2', 'K': '-3', 'M': '-1', 'F': '1', 'P': '-4', 'S': '-3', 'T': '-2', 'W': '11', 'Y': '2', 'V': '-3', 'B': '-4', 'Z': '-3', 'X': '-2', '*': '-4'},
                 'Y': {'A': '-2', 'R': '-2', 'N': '-2', 'D': '-3', 'C': '-2', 'Q': '-1', 'E': '-2', 'G': '-3', 'H': '2', 'I': '-1', 'L': '-1', 'K': '-2', 'M': '-1', 'F': '3', 'P': '-3', 'S': '-2', 'T': '-2', 'W': '2', 'Y': '7', 'V': '-1', 'B': '-3', 'Z': '-2', 'X': '-1', '*': '-4'},
                 'V': {'A': '0', 'R': '-3', 'N': '-3', 'D': '-3', 'C': '-1', 'Q': '-2', 'E': '-2', 'G': '-3', 'H': '-3', 'I': '3', 'L': '1', 'K': '-2', 'M': '1', 'F': '-1', 'P': '-2', 'S': '-2', 'T': '0', 'W': '-3', 'Y': '-1', 'V': '4', 'B': '-3', 'Z': '-2', 'X': '-1', '*': '-4'},
                 'B': {'A': '-2', 'R': '-1', 'N': '3', 'D': '4', 'C': '-3', 'Q': '0', 'E': '1', 'G': '-1', 'H': '0', 'I': '-3', 'L': '-4', 'K': '0', 'M': '-3', 'F': '-3', 'P': '-2', 'S': '0', 'T': '-1', 'W': '-4', 'Y': '-3', 'V': '-3', 'B': '4', 'Z': '1', 'X': '-1', '*': '-4'},
                 'Z': {'A': '-1', 'R': '0', 'N': '0', 'D': '1', 'C': '-3', 'Q': '3', 'E': '4', 'G': '-2', 'H': '0', 'I': '-3', 'L': '-3', 'K': '1', 'M': '-1', 'F': '-3', 'P': '-1', 'S': '0', 'T': '-1', 'W': '-3', 'Y': '-2', 'V': '-2', 'B': '1', 'Z': '4', 'X': '-1', '*': '-4'},
                 'X': {'A': '0', 'R': '-1', 'N': '-1', 'D': '-1', 'C': '-2', 'Q': '-1', 'E': '-1', 'G': '-1', 'H': '-1', 'I': '-1', 'L': '-1', 'K': '-1', 'M': '-1', 'F': '-1', 'P': '-2', 'S': '0', 'T': '0', 'W': '-2', 'Y': '-1', 'V': '-1', 'B': '-1', 'Z': '-1', 'X': '-1', '*': '-4'},
                 '*': {'A': '-4', 'R': '-4', 'N': '-4', 'D': '-4', 'C': '-4', 'Q': '-4', 'E': '-4', 'G': '-4', 'H': '-4', 'I': '-4', 'L': '-4', 'K': '-4', 'M': '-4', 'F': '-4', 'P': '-4', 'S': '-4', 'T': '-4', 'W': '-4', 'Y': '-4', 'V': '-4', 'B': '-4', 'Z': '-4', 'X': '-4', '*': '1'}}

        # TODO -> Обработчик ошибок не здесь(Не знаю, может и тут лучше, или в основном цикле)
        try:
            return int(align[s1][s2])
        except KeyError:
            # TODO -> Делать что-то другое. Возможно добавить свой обработчик ошибок!
            return None
    else:
        # TODO -> Делать что-то другое. Возможно добавить свой обработчик ошибок!
        return None


def sequence_global_alignment(s1: str, s2: str, mode: int = 0) -> Optional[int]:
    """Функция глобального выравнивания двух генетических цепочек
       по алгоритму Нидлмана-Вунша"""

    # TODO -> Сделать список в конфиге возможных таблиц выравнивания(режимов)(Возможно) + режими - не номера, а слова[Union]
    if mode not in [0, 1]:
        # TODO -> Делать что-то другое. Возможно добавить свой обработчик ошибок!
        return None

    table = [[0 for k in range(len(s2)+1)] for i in range(len(s1)+1)]

    table[0][0] = 0
    for i in range(1, len(s1)+1):
        table[i][0] = table[i-1][0] + count_cell_score(s1[i - 1], '*', mode)
    for j in range(1, len(s2)+1):
        table[0][j] = table[0][j-1] + count_cell_score('*', s2[j - 1], mode)

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            table[i][j] = max(table[i-1][j] + count_cell_score(s1[i - 1], '*', mode),
                              table[i][j-1] + count_cell_score('*', s2[j - 1], mode),
                              table[i-1][j-1] + count_cell_score(s1[i - 1], s2[j - 1], mode))

    print(np.matrix(table))
    # print(table[len(s1)][len(s2)])

    return table[len(s1)][len(s2)]


def sequence_local_alignment(s1: str, s2: str, mode: int = 0) -> Optional[int]:
    """Функция глокального выравнивания двух генетических цепочек
       по алгоритму Смита-Ватермана"""

    # TODO -> Сделать список в конфиге возможных таблиц выравнивания(режимов)(Возможно) + режими - не номера, а слова[Union]
    if mode not in [0, 1]:
        # TODO -> Делать что-то другое. Возможно добавить свой обработчик ошибок!
        return None

    table = [[0 for k in range(len(s2)+1)] for i in range(len(s1)+1)]

    table[0][0] = 0
    for i in range(1, len(s1)+1):
        table[i][0] = 0
    for j in range(1, len(s2)+1):
        table[0][j] = 0

    res = 0

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            table[i][j] = max(0,
                              table[i-1][j] + count_cell_score(s1[i - 1], '*', mode),
                              table[i][j-1] + count_cell_score('*', s2[j - 1], mode),
                              table[i-1][j-1] + count_cell_score(s1[i - 1], s2[j - 1], mode))
            if table[i][j] > res:
                res = table[i][j]

    print(np.matrix(table))
    return res
