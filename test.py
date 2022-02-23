# from tabulate import tabulate


class Figure:
    screen = [['🙩']*8 for _ in range(8)]
    figures = []

    def __init__(self, name, x, y, color):
        self.icon = "🙾"
        self.x = x
        self.y = y
        self.name = name
        self.paths = [['0']*8 for _ in range(8)]
        self.color = color
        self.is_moved = False
        Figure.figures.append(self)

    def __str__(self):
        return f"Объект класса {self.name}, координаты ({self.x}, {self.y})"

    def draw(self):
        print(f"Drawing {self.color} {self.name} at {self.x, self.y}")
        Figure.screen[self.y][self.x] = self.icon

    def move(self, coord):
        new_x, new_y = coord[0], coord[1]
        path = self.possible_paths[new_y][new_x]
        if path == "1" or path == "2":
            if self.possible_paths[new_y][new_x] == "2":
                Figure.check_for_figure((new_x, new_y)).kill()
            Figure.screen[self.y][self.x] = "🙩"
            print(f"Moving {self.color} {self.name} from {self.x, self.y} to {new_x, new_y}")
            self.x, self.y = new_x, new_y
            if type(self) == Pawn:
                self.is_moved = True
            self.draw()
        else:
            print(f"Невозможно переместить {self.name} в эту точку")

    @classmethod
    def print_screen(cls):
        for _ in range(8):
            print("  ".join(cls.screen[_]))
        print()

    @property
    def possible_paths(self):
        return [['1']*8 for _ in range(8)]

    @staticmethod
    def choose_figure(coord):
        print(coord)
        _ = Figure.check_for_figure(coord)
        if _:
            print(len(Figure.figures))
            Figure.print(_.possible_paths)
            return _
        else:
            return False

    @staticmethod
    def check_for_figure(coord):
        x, y = coord[0], coord[1]
        for _ in Figure.figures:
            if (x, y) == (_.x, _.y):
                return _
        return False

    @staticmethod
    def print(screen):
        for _ in range(8):
            print("  ".join(screen[_]))
        print()

    def kill(self):
        print(len(Figure.figures))
        print(f"killing {self}")
        self.x, self.y = 8, 8
        print(len(Figure.figures))


class Pawn(Figure):
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♙" if self.color == "White" else "♟"
        self.is_moved = False

    @property
    def possible_paths(self):
        self.paths = [['0'] * 8 for _ in range(8)]
        self.paths[self.y][self.x] = "P"
        direction = 1 if self.color == "White" else -1
        for i in range(2 - self.is_moved):
            t_y = self.y-(1 + i)*direction
            t_x = self.x
            if t_y < 0 or t_y > 7 or t_x < 0 or t_x > 7:
                return self.paths
            print("paths", t_x, t_y)
            if_figure = Figure.check_for_figure((t_x, t_y))
            if if_figure:
                print(if_figure)
                if if_figure.color != self.color:
                    self.paths[t_y][t_x] = "0"
                break
            else:
                self.paths[t_y][t_x] = "1"
        for t_x in [self.x - 1, self.x + 1]:
            t_y = self.y - 1 * direction
            if_figure = Figure.check_for_figure((t_x, t_y))
            if if_figure:
                self.paths[t_y][t_x] = "2"
        return self.paths


# fig = Figure("Figure", 1, 1, "Black")
# fig.move(5, 5)
# Figure.print_screen()
figures = [[None]*8 for _ in range(8)]
# p = Pawn("Pawn", 2, 3, "Black")
# p.draw()
# Figure.print_screen()
for x_ in range(8):
    figures[1][x_] = Pawn("Pawn", x_, 1, "Black")
    figures[1][x_].draw()
    figures[6][x_] = Pawn("Pawn", x_, 6, "White")
    figures[6][x_].draw()

# Figure.print(p.possible_paths)
# p.move(2, 0)
# Figure.print_screen()
# Figure.print(p.possible_paths)
# print(Figure.figures)
# print(Figure.figures[0].x)

Figure.print_screen()

while True:
    Figure.choose_figure(tuple(map(int, input("Выберите фигуру >> ").split()))).move(tuple(map(int, (input("Введите новые координаты >> ")).split())))
    Figure.print_screen()
# except:
#     for _ in Figure.figures:
#         print(_.x, _.y)
