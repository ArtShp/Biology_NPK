from config import BLOSUM62_TABLE
from exceptions import *
from typing import Optional


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


        # TODO -> Обработчик ошибок не здесь(Не знаю, может и тут лучше, или в основном цикле)
        try:
            return int(BLOSUM62_TABLE[s1][s2])
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

    # print(np.matrix(table))
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

    # print(np.matrix(table))
    return res
