import math
from type_aliases import IorF


class Vector2:
    def __init__(self, coord: list[IorF, IorF] | tuple[IorF, IorF]):
        self.__x = coord[0]
        self.__y = coord[1]
        self.__coord = coord
        self.__recalculate()

    @property
    def x(self) -> IorF:
        return self.__x

    @x.setter
    def x(self, value: IorF) -> None:
        self.__x = value
        self.__recalculate()

    @property
    def y(self) -> IorF:
        return self.__y

    @y.setter
    def y(self, value: IorF) -> None:
        self.__y = value
        self.__recalculate()

    @property
    def coord(self) -> list[IorF, IorF] | tuple[IorF, IorF]:
        return self.__coord

    @coord.setter
    def coord(self, value: list[IorF, IorF] | tuple[IorF, IorF]) -> None:
        self.__y = value
        self.__recalculate()

    def __recalculate(self) -> None:
        self.magnitude = math.sqrt(self.__x ** 2 + self.__y ** 2)
        self.unit = Vector2((self.__x / self.magnitude, self.__y / self.magnitude))

    def __iter__(self) -> IorF:
        yield from [self.__x, self.__y]

    def __getitem__(self, item: int) -> IorF:
        return [self.__x, self.__y][item]