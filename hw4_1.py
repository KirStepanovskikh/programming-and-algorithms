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


exec(stdin.read())
