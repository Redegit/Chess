from copy import deepcopy
import numpy as np
from random import choice
from math import sqrt

    ##### Класс поля, на котором размещаются фигуры


class Field():
    def __init__(self, char="o", space='·', size=20):
        self._space = space
        self.char = char
        self.size = size
        self.screen = [[self._space] * size for _ in range(self.size)]
        self.default_screen = deepcopy(self.screen)

    def draw(self, screen, area=0):
        for y in range(len(screen)):
            for x, i in enumerate(screen[y], 0):
                if i != self._space:
                    self.screen[y][x] = self.char

    def print_screen(self):
        for line in self.screen:
            for symb in line:
                print(symb, end='  ')
            print()

    def clear(self):
        self.screen = deepcopy(self.default_screen)

    def __str__(self):
        return f"Это поле размером {self.size}x{self.size} для размещения на нем фигур"


field = Field(size=15, space="(:")

print(field)
field.print_screen()


##### Класс Charp (точка)

class Sharp(Field):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def draw(self, master):
        self.screen = deepcopy(master.default_screen)
        self.screen[self.__y][self.__x] = master.char
        master.draw(self.screen)

    @property
    def area(self):
        return 0

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __str__(self):
        return f"Это точка с координатами ({self.__x}, {self.__y})"


field0 = Field(size=5)
sh = Sharp(1, 3)

sh.draw(field0)  # при вызове метода draw необходимо указать поле, на котором будет рисоваться фигура
print(sh)
field0.print_screen()


##### Класс линии

class Line(Field):
    def __init__(self, st_point, end_point):
        self.x = [st_point[0], end_point[0]]
        self.y = [st_point[1], end_point[1]]

    def draw(self, master):
        self.screen = deepcopy(master.default_screen)
        if self.x[0] <= self.x[1]:
            left_x = self.x[0]
            left_y = self.y[0]
            right_x = self.x[1]
            right_y = self.y[1]
        else:
            left_x = self.x[1]
            left_y = self.y[1]
            right_x = self.x[0]
            right_y = self.y[0]
        left_is_higher = True if left_y < right_y else False
        self.x_range = right_x - left_x + 1
        self.y_range = abs(right_y - left_y) + 1
        if self.x_range == 1:
            if left_y > right_y:
                left_y = right_y
        if self.x_range < self.y_range:
            needs_transpose = True
            self.x_range, self.y_range = self.y_range, self.x_range
            if left_is_higher:
                left_y, left_x = left_x, left_y
            else:
                left_y, left_x = right_x, right_y
        else:
            needs_transpose = False
        len_list = [self.x_range // self.y_range for _ in range(self.y_range)]
        remainder = self.x_range % self.y_range
        # блок с распределением остатков ПЕРЕПИСАТЬ
        while remainder > 0:
            choicer = choice([i for i in range(len(len_list))])
            if len_list[choicer] == self.x_range // self.y_range:
                len_list[choicer] += 1
                remainder -= 1
                #
        points_lost = 0
        for r in len_list:
            for x in range(r):
                try:
                    self.screen[left_y][x + left_x] = master.char
                except IndexError:
                    points_lost += 1
            left_y = left_y + 1 if left_is_higher else left_y - 1
            left_x += r
        if points_lost:
            print(f"Фигура выходит за границу поля")
        if needs_transpose:
            self.screen = np.transpose(self.screen)
        master.draw(self.screen)

    def __str__(self):
        return (f"Линия длиной {self.length()}")

    def length(self):
        x_range = abs(self.x[0] - self.x[1]) + 1
        y_range = abs(self.y[0] - self.y[1]) + 1
        l = sqrt((x_range ** 2 if x_range != 1 else 0) + \
                 (y_range ** 2 if y_range != 1 else 0))
        return l

    def __str__(self):
        return f"Это отрезок с точкам ({self.x[0]}, {self.y[0]}) и ({self.x[1]}, {self.y[1]})"


field1 = Field()
l = Line((2, 2), (18, 5))

l.draw(master=field1)
print(str(l))
field1.print_screen()


##### Класс прямоугольника

class Rectangle(Sharp):  # класс прямоугольника
    def __init__(self, x, y, w, h):
        super().__init__(x, y)
        self.__x = x
        self.__y = y
        self.__width = w
        self.__height = h

    def draw(self, master):  # отрисовка границы прямоугольника
        self.screen = deepcopy(master.default_screen)
        for i in range(self.__y, self.__y + self.__height):
            self.screen[i][self.__x] = master.char
        for i in range(self.__y, self.__y + self.__height):
            self.screen[i][self.__x + self.__width - 1] = master.char
        for i in range(self.__x, self.__x + self.__width):
            self.screen[self.__y][i] = master.char
        for i in range(self.__x, self.__x + self.__width):
            self.screen[self.__y + self.__height - 1][i] = master.char
        master.draw(self.screen)

    def draw_fill(self, master):  # отрисовка с заполнением
        self.screen = deepcopy(master.default_screen)
        for j in range(self.__x, self.__x + self.__width):
            for i in range(self.__y, self.__y + self.__height):
                self.screen[i][j] = master.char
        master.draw(self.screen)

    @property
    def area(self):
        return self.__width * self.__height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __str__(self):
        return f"Это прямоугольник с левой верхней точкой ({self.__x}, {self.__y}), \
шириной {self.__width} и высотой {self.__height}"


field2 = Field()
rectangle = Rectangle(1, 10, 3, 4)
rectangle1 = Rectangle(10, 1, 5, 4)

rectangle.draw(master=field2)
rectangle1.draw_fill(master=field2)
print(str(rectangle))
print(str(rectangle1))
field2.print_screen()


##### Класс квадрата (наследник прямоугольника)

class Square(Rectangle):  # класс квадрата
    def __init__(self, x, y, w):
        super().__init__(x, y, w, w)

    def __str__(self):
        return f"Это квадрат с левой верхней точкой \
({self._Rectangle__x}, {self._Rectangle__y}) и стороной {self._Rectangle__width}"


field3 = Field(size=10)
sq = Square(1, 2, 5)

sq.draw(field3)
print(str(sq))
field3.print_screen()


##### Класс треугольника

class Triangle(Sharp):
    def __init__(self, *coord):
        self.A = coord[0]
        self.B = coord[1]
        self.C = coord[2]
        self.a = Line(self.B, self.C)
        self.b = Line(self.A, self.C)
        self.c = Line(self.A, self.B)

    def draw(self, master):
        for _ in [self.a, self.b, self.c]:
            _.draw(master)

    @property
    def area(self):
        a_len = self.a.length()
        b_len = self.b.length()
        c_len = self.c.length()
        p = (a_len + b_len + c_len) / 2
        area = sqrt(p * (p - a_len) * (p - b_len) * (p - c_len))
        return area

    def __str__(self):
        return f"Это треугольник с вершинами {self.A}, {self.B}, {self.C}"


field4 = Field(size=30)
tri = Triangle((1, 1), (27, 6), (8, 28))

print(tri.area)
tri.draw(field4)
print(str(tri))
field4.print_screen()

##### Пример размещения нескольких фигур в одном поле

f = Field()
s1 = Sharp(5, 16)
s2 = Line((1, 3), (13, 1))
s3 = Rectangle(2, 7, 5, 3)
s4 = Triangle((9, 6), (18, 10), (10, 19))

for _ in [s1, s2, s3, s4]:
    _.draw(f)
    print(_)
f.print_screen()

##### Нахождение суммы площадей нескольких фигур

a1 = Triangle((0, 0), (0, 9), (4, 9))  # area = 25.0
a2 = Rectangle(0, 0, 5, 4)  # area = 20
a3 = Square(0, 0, 10)  # area = 100
a4 = Sharp(0, 0)  # area = 0

a_area = 0
a = [a1, a2, a3, a4]
for _ in a:
    a_area += _.area
print(a_area)

##### Проверка принадлежности к классу Sharp и его подклассам

b1 = Triangle((5, 4), (5, 13), (9, 13))  # area = 25.0
b2 = Rectangle(0, 0, 5, 4)  # area = 20
b3 = Square(0, 0, 10)  # area = 100
b4 = Sharp(0, 0)  # area = 0
line = Line((0, 0), (1, 1))  # no attribute area

b_area = 0
b = [b1, b2, b3, b4, line]
for _ in b:
    if isinstance(_, Sharp):
        b_area += _.area
print(b_area)

##### Класс ромба

class Rhomb(Rectangle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def draw(self, master):
        self.A = (self.x, self.y)
        self.C = (self.x+self.width-1, self.y)
        self.B = (self.x+(self.width//2), self.y-(self.height//2))
        self.D = (self.x+(self.width//2), self.y+(self.height//2))
        a = Line(self.A, self.B)
        b = Line(self.B, self.C)
        c = Line(self.C, self.D)
        d = Line(self.D, self.A)
        for _ in [a, b, c, d]:
            _.draw(master)


field5 = Field()
rh = Rhomb(4, 9, 11, 11)
rh.draw(field5)
field5.print_screen()

# class Sharp(object):
#     def __init__(self,x,y):
#         self.__x = x
#         self.__y = y
#         self.screen=[['.']*20 for _ in range(20)]

#     def print_screen(self):
#         for line in self.screen:
#             for symb in line:
#                 print(symb, end='')
#             print()

#     @property
#     def x(self):
#         return self.__x

#     @property
#     def y(self):
#         return self.__y

#     def draw(self):
#         self.screen=[['.']*20 for _ in range(20)]
#         self.screen[self.__y][self.__x]='*'
#         self.print_screen()

#     def __str__(self):
#         return f'Это точка с координатами ({self.x};{self.y})'

#     def area(self):
#         return 0
