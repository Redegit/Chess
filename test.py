# from tabulate import tabulate


class Figure:
    screen = [['🙩']*8 for _ in range(8)]
    figures = []
    turn = "White"

    def __init__(self, name, x, y, color):
        self.icon = "🙾"
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.is_moved = False
        if self.name != "Non-existent":
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
            Figure.turn = "Black" if Figure.turn == "White" else "White"
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
        print(f"killing {self}")
        self.x, self.y = 8, 8

    @staticmethod
    def play():
        figure = Figure.check_for_figure(tuple(map(int, input("Выберите фигуру >> ").split())))
        if figure:
            if figure.color == Figure.turn:
                if sum(sum(j == "0" for j in i) for i in figure.possible_paths) == 63:
                    print("Этой фигуре некуда идти")
                    Figure.print_screen()
                    return
                Figure.print(figure.possible_paths)
                figure.move(tuple(map(int, (input("Введите новые координаты >> ")).split())))
            else:
                print(f"Сейчас ход {Figure.turn}")
            Figure.print_screen()
        else:
            print("there's no figure")

    @staticmethod
    def combine_paths(path1, path2):
        new_path = [["0"]*8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if path1[i][j] != "0":
                    new_path[i][j] = path1[i][j]
                if path2[i][j] != "0":
                    new_path[i][j] = path2[i][j]
        return new_path


class Pawn(Figure):  # пешка
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♙" if self.color == "White" else "♟"

    @property
    def possible_paths(self):
        paths = [['0'] * 8 for _ in range(8)]
        paths[self.y][self.x] = "P"
        direction = 1 if self.color == "White" else -1
        for i in range(2 - self.is_moved):
            t_y = self.y-(1 + i)*direction
            t_x = self.x
            if t_y < 0 or t_y > 7 or t_x < 0 or t_x > 7:
                return paths
            if_figure = Figure.check_for_figure((t_x, t_y))
            if if_figure:
                paths[t_y][t_x] = "0"
                break
            else:
                paths[t_y][t_x] = "1"
        for t_x in [self.x - 1, self.x + 1]:
            t_y = self.y - 1 * direction
            if_figure = Figure.check_for_figure((t_x, t_y))
            if if_figure:
                paths[t_y][t_x] = "2" if if_figure.color != self.color else "0"
        return paths


class Rook(Figure):  # ладья
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♖" if self.color == "White" else "♜"

    @property
    def possible_paths(self):
        paths = [['0'] * 8 for _ in range(8)]
        paths[self.y][self.x] = "R"
        directions = [1, -1]
        for x_dir in directions:
            for x in range(self.x + x_dir, 8 if x_dir == 1 else -1, x_dir):
                figure = Figure.check_for_figure((x, self.y))
                if figure:
                    paths[self.y][x] = "0" if figure.color == self.color else "2"
                    break
                paths[self.y][x] = "1"
        for y_dir in directions:
            for y in range(self.y + y_dir, 8 if y_dir == 1 else -1, y_dir):
                figure = Figure.check_for_figure((self.x, y))
                if figure:
                    paths[y][self.x] = "0" if figure.color == self.color else "2"
                    break
                paths[y][self.x] = "1"
        return paths


class Knight(Figure):  # конь
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♘" if self.color == "White" else "♞"

    @property
    def possible_paths(self):
        paths = [['0'] * 8 for _ in range(8)]
        paths[self.y][self.x] = "K"
        directions = [(1, -2), (1, 2), (-1, -2), (-1, 2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
        for x, y in directions:
            x, y = self.x + x, self.y + y
            if x > 7 or y > 7 or x < 0 or y < 0:
                continue
            figure = Figure.check_for_figure((x, y))
            if figure:
                paths[y][x] = "2" if figure.color != self.color else "0"
            else:
                paths[y][x] = "1"
        return paths


class Bishop(Figure):
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♗" if self.color == "White" else "♝"

    @property
    def possible_paths(self):
        paths = [['0'] * 8 for _ in range(8)]
        paths[self.y][self.x] = "B"
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            while 0 <= x <= 7 and 0 <= y <= 7:
                figure = Figure.check_for_figure((x, y))
                if figure:
                    paths[y][x] = "2" if figure.color != self.color else "0"
                    break
                else:
                    paths[y][x] = "1"
                    x += dx
                    y += dy
        return paths


class Queen(Figure):
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♕" if self.color == "White" else "♛"

    @property
    def possible_paths(self):
        paths1 = Bishop("Non-existent", self.x, self.y, self.color).possible_paths
        paths2 = Rook("Non-existent", self.x, self.y, self.color).possible_paths
        paths = Figure.combine_paths(paths1, paths2)
        paths[self.y][self.x] = "Q"
        return paths


class King(Figure):
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♔" if self.color == "White" else "♚"

    @property
    def possible_paths(self):
        paths = [['0'] * 8 for _ in range(8)]
        paths[self.y][self.x] = "K"
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            if 0 <= x <= 7 and 0 <= y <= 7:
                figure = Figure.check_for_figure((x, y))
                if figure:
                    paths[y][x] = "2" if figure.color != self.color else "0"
                else:
                    paths[y][x] = "1"
        return paths


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
for x_ in [0, 7]:
    figures[0][x_] = Rook("Rook", x_, 0, "Black")
    figures[0][x_].draw()
    figures[7][x_] = Rook("Rook", x_, 7, "White")
    figures[7][x_].draw()
for x_ in [1, 6]:
    figures[0][x_] = Knight("Knight", x_, 0, "Black")
    figures[0][x_].draw()
    figures[7][x_] = Knight("Knight", x_, 7, "White")
    figures[7][x_].draw()
for x_ in [2, 5]:
    figures[0][x_] = Bishop("Bishop", x_, 0, "Black")
    figures[0][x_].draw()
    figures[7][x_] = Bishop("Bishop", x_, 7, "White")
    figures[7][x_].draw()
figures[0][3] = Queen("Queen", 3, 0, "Black")
figures[0][3].draw()
figures[7][3] = Queen("Queen", 3, 7, "White")
figures[7][3].draw()
figures[0][4] = King("King", 4, 0, "Black")
figures[0][4].draw()
figures[7][4] = King("King", 4, 7, "White")
figures[7][4].draw()
# Figure.print(p.possible_paths)
# p.move(2, 0)
# Figure.print_screen()
# Figure.print(p.possible_paths)
# print(Figure.figures)
# print(Figure.figures[0].x)

Figure.print_screen()
while True:
    Figure.play()
# except:
#     for _ in Figure.figures:
#         print(_.x, _.y)
