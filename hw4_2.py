from __future__ import annotations
from copy import deepcopy
from typing import List, Tuple
from sys import stdin


class Matrix:
    def __init__(self, values: List[List[float]]) -> None:
        """
        Конструктор принимает список списков.
        Все списки не пустые, заполнены числами.
        Во всех списках равное количество элементов.
        """
        self.values = deepcopy(values)

    def __str__(self) -> str:
        """
        Метод переводит матрицу в строку так, что
        элементы строки отбиваются табуляцией,
        а строки отбиваются переносом строки
        """
        str_lines = []
        for line in self.values:
            line = map(str, line)
            line = "\t".join(line)
            str_lines.append(line)
        return "\n".join(str_lines)

    def size(self) -> Tuple[int, int]:
        """
        Метод выдает размер матрицы вида (число строк, число столбцов)
        """
        return len(self.values), len(self.values[0])

    def __add__(self, mtx: Matrix) -> Matrix:
        """
        Поэлементное сложение матриц.
        Возвращает матрицу
        """
        new_mtx = []
        for line1, line2 in zip(self.values, mtx.values):
            new_line = []
            for el1, el2 in zip(line1, line2):
                result = el1 + el2
                new_line.append(result)
            new_mtx.append(new_line)
        return Matrix(new_mtx)

    def __mul__(self, scalar: float) -> Matrix:
        """
        Умножение матрицы на левое число.
        Возвращает матрицу
        """
        new_mtx = [[el * scalar for el in line] for line in self.values]
        return Matrix(new_mtx)

    def __rmul__(self, scalar: float) -> Matrix:
        """
        Умножение матрицы на правое число.
        Возвращает матрицу
        """
        return self.__mul__(scalar)


exec(stdin.read())
