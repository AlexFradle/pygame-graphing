import math
import pygame
from enum import Enum
from dataclasses import dataclass
from typing import overload
from type_aliases import GridLineList, CoordPointList, IorF
from maths import Vector2


class Colours(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


@dataclass
class Point:
    coord: list[IorF, IorF] | tuple[IorF, IorF] | Vector2
    colour: Colours

    def __getitem__(self, item):
        if item > 1: raise IndexError("Index greater than 1")
        if isinstance(self.coord, Vector2):
            return [self.coord.x, self.coord.y][item]
        return self.coord[item]


class Graph(pygame.Surface):
    def __init__(self, width: int, height: int) -> None:
        super().__init__((width, height))
        self.__height = height
        self.__width = width
        self.style = {
            "axis_colour": Colours.RED.value
        }
        self.__offset = (width // 2, height // 2)
        self.__resolution = 10
        self.__grid_lines_x = self.__generate_x_grid_lines()
        self.__grid_lines_y = self.__generate_y_grid_lines()

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def __conv_coord(self, x, y) -> tuple[IorF, IorF]:
        return (
            (x * self.__resolution) + self.__offset[0],
            (-y * self.__resolution) - self.__offset[1] + self.__height
        )

    @overload
    def _convert_to_surface_coords(self, p: list[IorF, IorF]) -> list[IorF, IorF]:
        ...

    @overload
    def _convert_to_surface_coords(self, p: tuple[IorF, IorF]) -> tuple[IorF, IorF]:
        ...

    @overload
    def _convert_to_surface_coords(self, p: Vector2) -> Vector2:
        ...

    @overload
    def _convert_to_surface_coords(self, p: Point) -> Point:
        ...

    @overload
    def _convert_to_surface_coords(self, l: list[Point]) -> list[Point]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: list[Vector2]) -> list[Vector2]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: tuple[Point, ...]) -> tuple[Point, ...]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: tuple[Vector2, ...]) -> tuple[Vector2, ...]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: list[list[IorF, IorF]]) -> list[list[IorF, IorF]]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: list[tuple[IorF, IorF]]) -> list[tuple[IorF, IorF]]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: tuple[list[IorF, IorF]]) -> tuple[list[IorF, IorF]]:
        ...

    @overload
    def _convert_to_surface_coords(self, l: tuple[tuple[IorF, IorF]]) -> tuple[tuple[IorF, IorF]]:
        ...

    @overload
    def _convert_to_surface_coords(self, *args: list[IorF, IorF]) -> list[list[IorF, IorF]]:
        ...

    @overload
    def _convert_to_surface_coords(self, *args: tuple[IorF, IorF]) -> list[tuple[IorF, IorF]]:
        ...

    @overload
    def _convert_to_surface_coords(self, *args: Point) -> list[Point]:
        ...

    @overload
    def _convert_to_surface_coords(self, *args: Vector2) -> list[Vector2]:
        ...

    def _convert_to_surface_coords(self, *args):
        args_head = args[0]
        list_funcs = {
            Point: lambda c: [Point(type(p.coord)(self.__conv_coord(*p.coord)), p.colour) for p in c],
            Vector2: lambda c: [Vector2(self.__conv_coord(*v)) for v in c],
            list: lambda c: [list(self.__conv_coord(*l)) for l in c],
            tuple: lambda c: [self.__conv_coord(*t) for t in items]
        }
        match args:
            # list[IorF, IorF] -> list[IorF, IorF]
            case ([x1, y1],) if isinstance(args_head, list) and isinstance(x1, IorF):
                return list(self.__conv_coord(x1, y1))

            # tuple[IorF, IorF] -> tuple[IorF, IorF]
            case ((x1, y1),) if isinstance(args_head, tuple) and isinstance(x1, IorF):
                return self.__conv_coord(x1, y1)

            # Vector2 -> Vector2
            case (v,) if isinstance(v, Vector2):
                return Vector2(self.__conv_coord(*v))

            # Point -> Point
            case (p,) if isinstance(p, Point):
                return Point(type(p.coord)(self.__conv_coord(*p.coord)), p.colour)

            # C[T] -> C[T] | n * T, n > 1 -> list[n * T]
            case ([*items],) | [*items]:
                # tuple[T] -> tuple[T]
                if isinstance(args_head, tuple):
                    return tuple(list_funcs[type(items[0])](items))

                # list[T] -> list[T] | n * T -> list[n * T]
                else:
                    return list_funcs[type(items[0])](items)

            case _:
                raise TypeError("Incorrect types provided")

    def __generate_x_grid_lines(self) -> GridLineList:
        base = [
            [
                [0, self.__height - self.__offset[1] - (i * self.__resolution)],
                [self.__width, self.__height - self.__offset[1] - (i * self.__resolution)]
            ] for i in range(self.__height // self.__resolution + 1)
        ]
        shift_amount = 0
        for i in base:
            if i[0][1] < 0:
                shift_amount += 1
            elif i[0][1] > self.__height:
                shift_amount -= 1

        return [
            [
                [i[0][0], i[0][1] + (shift_amount * self.__resolution)],
                [i[1][0], i[1][1] + (shift_amount * self.__resolution)],
            ] for i in base
        ]

    def __generate_y_grid_lines(self) -> GridLineList:
        base = [
            [
                [self.__offset[0] + (i * self.__resolution), self.__height],
                [self.__offset[0] + (i * self.__resolution), 0]
            ] for i in range(self.__width // self.__resolution + 1)
        ]
        shift_amount = 0
        for i in base:
            if i[0][0] < 0:
                shift_amount += 1
            elif i[0][0] > self.__width:
                shift_amount -= 1
        return [
            [
                [i[0][0] + (shift_amount * self.__resolution), i[0][1]],
                [i[1][0] + (shift_amount * self.__resolution), i[1][1]],
            ] for i in base
        ]

    def incr_offset(self, incr_x=0, incr_y=0):
        self.__offset = (self.__offset[0] + incr_x, self.__offset[1] + incr_y)

    def change_res(self, amount):
        self.__resolution += amount

    def draw(self) -> None:
        self.fill((0, 0, 0))

        # x coord lines
        self.__grid_lines_x = self.__generate_x_grid_lines()
        for xcl in self.__grid_lines_x:
            pygame.draw.line(self, (60, 60, 60), xcl[0], xcl[1])

        # y coord lines
        self.__grid_lines_y = self.__generate_y_grid_lines()
        for ycl in self.__grid_lines_y:
            pygame.draw.line(self, (60, 60, 60), ycl[0], ycl[1])

        # x axis
        pygame.draw.line(self, self.style["axis_colour"], (0, self.__height - self.__offset[1]), (self.__width, self.__height - self.__offset[1]))

        # y axis
        pygame.draw.line(self, self.style["axis_colour"], (self.__offset[0], self.__height), (self.__offset[0], 0))


class LineGraph(Graph):
    def __init__(self, width: int, height: int, points: list[tuple[IorF, IorF] | list[IorF, IorF] | Point | Vector2] = None) -> None:
        super().__init__(width, height)
        self.points = points

    def draw(self) -> None:
        super().draw()
        window_coords = self._convert_to_surface_coords(self.points)
        for wc in window_coords:
            pygame.draw.circle(self, (255, 0, 0) if not isinstance(wc, Point) else wc.colour, wc, 2)

        for i in range(1, len(window_coords)):
            pygame.draw.line(self, (0, 255, 0), tuple(window_coords[i - 1]), tuple(window_coords[i]))

