from __future__ import annotations
from copy import deepcopy
from typing import List, Tuple
from sys import stdin


class MatrixError(Exception):
    """
    Ошибка при операциях с матрицами типа Matrix
    """
    matrix1 = None
    matrix2 = None


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
        str_mtx = []
        for row in self.values:
            row = map(str, row)
            row = "\t".join(row)
            str_mtx.append(row)
        return "\n".join(str_mtx)

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
        if mtx.size() != self.size():
            MatrixError.matrix1 = self
            MatrixError.matrix2 = mtx
            raise MatrixError()

        new_mtx = []
        for row1, row2 in zip(self.values, mtx.values):
            new_row = []
            for el1, el2 in zip(row1, row2):
                result = el1 + el2
                new_row.append(result)
            new_mtx.append(new_row)
        return Matrix(new_mtx)

    def __mul__(self, scalar: float) -> Matrix:
        """
        Умножение матрицы на левое число или матрицу.
        Возвращает матрицу
        """
        if type(scalar) is Matrix:
            return self.__matmul(scalar)

        new_mtx = [[el * scalar for el in row] for row in self.values]
        return Matrix(new_mtx)

    def __rmul__(self, scalar: float) -> Matrix:
        """
        Умножение матрицы на правое число или матрицу.
        Возвращает матрицу
        """
        return self.__mul__(scalar)

    def transpose(self) -> Matrix:
        """
        Транспонирует исходную матрицу inplace
        """
        n_row, n_col = self.size()
        new_mtx = []
        for i in range(n_col):
            new_row = []
            for j in range(n_row):
                new_row.append(self.values[j][i])
            new_mtx.append(new_row)
        # не смог придумать как изменять прямо саму матрицу в транспонированную,
        # поэтому делаю дип копию
        self.values = deepcopy(new_mtx)
        return Matrix(self.values)

    @staticmethod
    def transposed(mtx: Matrix) -> Matrix:
        """
        Принимает объект типа Matrix
        Возвращает новую транспонированную матрицу типа Matrix
        """
        # не смог придумать как сделать через вызов метода mtx.transpose()
        # поэтому сделал то же самое но без дип копии
        n_row, n_col = mtx.size()
        new_mtx = []
        for i in range(n_col):
            new_row = []
            for j in range(n_row):
                new_row.append(mtx.values[j][i])
            new_mtx.append(new_row)
        return Matrix(new_mtx)

    def __matmul(self, mtx: Matrix) -> Matrix:
        """
        Умножение матриц
        """
        if self.size()[1] != mtx.size()[0]:
            MatrixError.matrix1 = self
            MatrixError.matrix2 = mtx
            raise MatrixError()

        new_mtx = []
        for row in self.values:
            new_row = []
            for col in list(zip(*mtx.values)):
                new_elem = sum(elem1 * elem2 for elem1, elem2 in zip(row, col))
                new_row.append(new_elem)
            new_mtx.append(new_row)
        return Matrix(new_mtx)


exec(stdin.read())
