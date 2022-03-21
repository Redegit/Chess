# from tabulate import tabulate
import pygame as pg
import sys


class Figure:
    screen = [['🙩']*8 for _ in range(8)]
    figures = []
    kings = []
    rooks = []
    turn = "White"

    def __init__(self, name, x, y, color):
        self.icon = "🙾"
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.is_moved = False
        self.status = "Alive"
        if self.name != "Non-existent":
            Figure.figures.append(self)

    def __str__(self):
        return f"Объект класса {self.name}, координаты ({self.x}, {self.y})"

    def draw(self):
        if self.status == "Killed":
            return
        font = pg.font.Font('CASEFONT.TTF', 72)
        icon = self.icon[1]
        text1 = font.render(icon, True, (26, 13, 0))
        sc.blit(text1, (120 + self.x * 70, 70 + self.y * 70))

    def move(self, coord):
        paths = self.paths
        global counter, turns, per, minus
        new_x, new_y = coord[0], coord[1]
        path = paths[new_y][new_x]
        s = self.icon[0]
        sep = '-'
        end = ''
        path = self.possible_paths[new_y][new_x]
        if path in ["1", "2", "3"]:
            castling = False
            if path == "2":
                Figure_to_kill = Figure.check_for_figure((new_x, new_y))
                Figure_to_kill.kill()
                sep = ':'
            if path == "3":
                castling = True  # прикрутить к записи ходов
                rook = Figure.check_for_figure((0 if new_x == 2 else 7, self.y))
                rook.x = (self.x + new_x) // 2
                rook.draw()
            temp_x, temp_y = self.x, self.y
            self.x, self.y = new_x, new_y
            for K in Figure.kings:
                if K.color == self.color:
                    if K.strike_check()[0]:
                        end = '+'
                        print(f"Figure can't be placed here, {K.color} {K.name} is under attack!")
                        self.x, self.y = temp_x, temp_y
                        turns[counter] = s + chr(coords[0] + 97) + str(8 - coords[1]) + sep + chr(new_x + 97) + str(8 - new_y) + end
                        return
            print(f"Moving {self.color} {self.name} from {temp_x, temp_x} to {new_x, new_y}")
            self.x, self.y = new_x, new_y
            counter += 1
            if type(self) in [Pawn, Rook, King]:
                self.is_moved = True
            self.draw()
            if counter % 2 != 0:
                # turns[counter] = s + chr(coords[0] + 97) + str(8 - coords[1]) + sep + chr(new_x + 97) + str(8 - new_y) + end
                per = s + chr(coords[0] + 97) + str(8 - coords[1]) + sep + chr(new_x + 97) + str(8 - new_y) + end
            else:
                minus += 1
                turns[counter-minus] = per + ' ' + s + chr(coords[0] + 97) + str(8 - coords[1]) + sep + chr(new_x + 97) + str(8 - new_y) + end
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
        global stat
        print(f"killing {self}")
        self.status = "Killed"
        self.x, self.y = 8, 8

    @staticmethod
    def play():
        global coords
        figure = Figure.check_for_figure(((pg.mouse.get_pos()[0]-120)//70, (pg.mouse.get_pos()[1]-70)//70))
        if figure:
            coords = ((pg.mouse.get_pos()[0]-120)//70, (pg.mouse.get_pos()[1]-70)//70)
            if figure.color == Figure.turn:
                paths = figure.paths
                if sum(sum(j == "0" for j in i) for i in paths) == 63:
                    print("Этой фигуре некуда идти")
                    return
                highlight = pg.image.load("highlight.png")
                sc.blit(highlight, (coords[0] * 70 + 120, coords[1] * 70 + 70))
                pg.display.update()
                b_circle = pg.image.load('blue.png')
                r_circle = pg.image.load('red.png')
                castling_circle = pg.image.load('castling.png')
                for i in range(8):
                    for j in range(8):
                        if paths[i][j] == '1':
                            sc.blit(b_circle, (j * 70 + 120, i * 70 + 70))
                        elif paths[i][j] == '2':
                            sc.blit(r_circle, (j * 70 + 120, i * 70 + 70))
                        elif paths[i][j] == '3':
                            sc.blit(castling_circle, (j * 70 + 120, i * 70 + 70))
                pg.display.update()
                print(figure)
                Figure.print(paths)
                k = 0
                while k != 1:
                    for i in pg.event.get():
                        if i.type == pg.MOUSEBUTTONDOWN:
                            figure.move(((pg.mouse.get_pos()[0]-120)//70, (pg.mouse.get_pos()[1]-70)//70))
                            k += 1
                            update(figures, background, image, counter)
                            pg.display.update()
            else:
                print(f"Сейчас ход {Figure.turn}")
        else:
            print("there's no figure")
        d_circle = pg.image.load('danger.png')
        check = pg.image.load('check.png')
        if figure:
            K = figure.enemy_king
            king_check = K.strike_check()[0]
            if king_check:
                sc.blit(check, (K.x * 70 + 120, K.y * 70 + 70))
            if Figure.checkmate():
                ch = f"Checkmate, {'Black' if Figure.turn == 'White' else 'White'} wins!"
                checkmate_str = norm_font.render(ch, True, (230, 0, 0))
                sc.blit(checkmate_str, (0, 320))
            for enemy in Figure.figures:
                if enemy.status == 'Alive':
                    if enemy.color != Figure.turn:
                        for y in range(8):
                            for x in range(8):
                                if enemy.possible_paths[y][x] == '2':
                                    if (x, y) != (K.x, K.y):
                                        sc.blit(d_circle, (x * 70 + 120, y * 70 + 70))
                                    pg.display.update()

    @staticmethod
    def checkmate():
        for figure in Figure.figures:
            if (figure.color, figure.status) == (Figure.turn, "Alive"):
                for row in figure.paths:
                    if "1" in row or "2" in row:
                        return False
        return True

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

    def strike_check(self):
        threatening_figures = []
        for figure in Figure.figures:
            if figure.status == "Alive":
                if figure.color != self.color:
                    print(figure.x, figure.y, figure.status, self.x, self.y, figure.possible_paths)
                    if figure.possible_paths[self.y][self.x] == "2":
                        threatening_figures.append(figure)
        if threatening_figures:
            return True, threatening_figures
        else:
            return False, []

    def check(self, x, y):
        temp_x, temp_y = self.x, self.y
        self.x, self.y = x, y
        K = self.king
        if K.strike_check()[0]:
            self.x, self.y = temp_x, temp_y
            return '0'
        else:
            self.x, self.y = temp_x, temp_y
            return '1'

    def kill_check(self, x, y):
        to_kill = Figure.check_for_figure((x, y))
        if to_kill.name == 'King':
            return '0'
        t_x, t_y = to_kill.x, to_kill.y
        to_kill.kill()
        check = self.check(x, y)
        to_kill.status, to_kill.x, to_kill.y = "Alive", t_x, t_y
        if check == '1':
            return '2'
        else:
            return '0'

    @property
    def king(self):
        for K in Figure.kings:
            if K.color == self.color:
                return K

    @property
    def enemy_king(self):
        for K in Figure.kings:
            if K.color != self.color:
                return K

    @property
    def paths(self):
        paths = list(self.possible_paths)
        for y in range(8):
            for x in range(8):
                if paths[y][x] == '1':
                    paths[y][x] = self.check(x, y)
                elif paths[y][x] == '2':
                    paths[y][x] = self.kill_check(x, y)
                elif paths[y][x] == '3':
                    paths[y][x] = '3' if self.check(x, y) else '0'
                else:
                    pass
        if self.name == "King":
            check = self.strike_check()[0]
            for y in [0, 7]:
                for x in [2, 6]:
                    if paths[y][x] == '3':
                        if check:
                            paths[y][x] = '0'
                        elif paths[y][(4+x)//2] == "0":
                            paths[y][x] = '0'
        return paths


class Pawn(Figure):  # пешка
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = 'pp' if self.color == "White" else "po"

    @property
    def possible_paths(self):
        print(f'paths {self}')
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
                break
            else:
                paths[t_y][t_x] = '1'
        for t_x in [self.x - 1, self.x + 1]:
            t_y = self.y - 1 * direction
            if_figure = Figure.check_for_figure((t_x, t_y))
            if if_figure:
                print(if_figure)
                if if_figure.color != self.color:
                    paths[t_y][t_x] = '2'
        return paths


class Rook(Figure):  # ладья
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "rr" if self.color == "White" else "rt"
        if self.name != "Non-existent":
            Figure.rooks.append(self)

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
        self.icon = "nn" if self.color == "White" else "nm"

    @property
    def possible_paths(self):
        paths = [['0'] * 8 for _ in range(8)]
        paths[self.y][self.x] = "N"
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


class Bishop(Figure): # слон
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "bb" if self.color == "White" else "bv"

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


class Queen(Figure): # королева
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "qq" if self.color == "White" else "qw"

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
        self.icon = "kk" if self.color == "White" else "kl"
        if self.name != "Non-existent":
            Figure.kings.append(self)

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
        # Castling / рокировка
        if not self.is_moved:
            for rook in Figure.rooks:
                if (not rook.is_moved) and (rook.color == self.color):
                    if (rook.x, rook.y) == (0, self.y):
                        k = 0
                        for x in range(self.x - 1, 0, -1):
                            if Figure.check_for_figure((x, self.y)):
                                k += 1
                        if k == 0:
                            paths[self.y][2] = '3'
                    elif (rook.x, rook.y) == (7, self.y):
                        k = 0
                        for x in range(self.x + 1, 7, 1):
                            if Figure.check_for_figure((x, self.y)):
                                k += 1
                        if k == 0:
                            paths[self.y][6] = '3'
        return paths


def update(figures, background, image, counter):
    text_counter = norm_font.render(str(counter), True, (200, 200, 200))
    sc.blit(background,(0, 0))
    sc.blit(image, (85, 35))
    sc.blit(text_counter, (740, 50))
    for x in range(8):
        for y in range(8):
            if figures[x][y]:
                figures[x][y].draw()


pg.font.init()
turns = {}

pg.display.set_caption("CHESS")
clock = pg.time.Clock()

background = pg.image.load('wood.jpg')


font = pg.font.Font('CASEFONT.TTF', 72)
norm_font = pg.font.Font('arial.ttf', 72)
sc = pg.display.set_mode((800, 700))
sc.blit(background, (0, 0))
image = pg.image.load('main5.jpg')
image = pg.transform.scale(image, (630, 630))
sc.blit(image, (85, 35))
pg.display.update()
c = 0
minus = 0
# Счётчик ходов
counter = 0
text_counter = norm_font.render(str(counter), True, (200, 200, 200))
sc.blit(text_counter, (740, 50))


stat = {
    'Pawn': 0,
    'Knight': 0,
    'Bishop': 0,
    'Rook': 0,
    'Queen': 0,
    'King': 0
}

while True:
    for i in pg.event.get():
        if c == 0:
            figures = [[None] * 8 for _ in range(8)]
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
            print(figures[1][1].__dict__)
            c += 1
            pg.display.update()
        if i.type == pg.QUIT:
            sys.exit() # (120 + self.x * 70, 70 + self.y * 70)
        if i.type == pg.MOUSEBUTTONDOWN:
            if 120 < pg.mouse.get_pos()[0] < 680 and 70 < pg.mouse.get_pos()[1] < 630:
                new_x, new_y = (pg.mouse.get_pos()[0] - 120) // 70, (pg.mouse.get_pos()[1] - 70) // 70
                print(new_x, new_y)
                Figure.play()
                # update(figures, background, image)
            print(pg.mouse.get_pos())
    clock.tick(10)

    with open('result.txt', mode = 'w') as file:
        for i in turns.items():
            file.write(str(i[0])+ ' ' + i[1] + '\n')


