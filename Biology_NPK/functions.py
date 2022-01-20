from config import BLOSUM62_TABLE
from typing import Optional


def _count_cell_score(s1: str, s2: str, mode: int = 0) -> Optional[int]:
    """Функция для подсчёта стоимости текущей ячейки."""
    """ВАЖНО! Передаются только символы, а не строки"""

    if mode == 0:
        """Используем BLOSUM62"""
        return int(BLOSUM62_TABLE[s1][s2])  # Возвращаем значение из таблицы
    elif mode == 1:
        """Используем базовую схему"""
        if '*' in [s1, s2]:
            return -1
        elif s1 == s2:
            return 1
        else:
            return -1


def sequence_global_alignment(s1: str, s2: str, mode: int = 0) -> Optional[int]:
    """Функция глобального выравнивания двух генетических цепочек
       по алгоритму Нидлмана-Вунша"""

    """Инициализация и заполнение таблицы"""
    table = [[0 for k in range(len(s2)+1)] for i in range(len(s1)+1)]

    table[0][0] = 0
    for i in range(1, len(s1)+1):
        table[i][0] = table[i-1][0] + _count_cell_score(s1[i - 1], '*', mode)
    for j in range(1, len(s2)+1):
        table[0][j] = table[0][j-1] + _count_cell_score('*', s2[j - 1], mode)

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            table[i][j] = max(table[i-1][j] + _count_cell_score(s1[i - 1], '*', mode),
                              table[i][j-1] + _count_cell_score('*', s2[j - 1], mode),
                              table[i-1][j-1] + _count_cell_score(s1[i - 1], s2[j - 1], mode))

    return table[len(s1)][len(s2)]


def sequence_local_alignment(s1: str, s2: str, mode: int = 0) -> Optional[int]:
    """Функция глокального выравнивания двух генетических цепочек
       по алгоритму Смита-Ватермана"""

    """Инициализация и заполнение таблицы"""
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
                              table[i-1][j] + _count_cell_score(s1[i - 1], '*', mode),
                              table[i][j-1] + _count_cell_score('*', s2[j - 1], mode),
                              table[i-1][j-1] + _count_cell_score(s1[i - 1], s2[j - 1], mode))
            if table[i][j] > res:
                res = table[i][j]

    return res
