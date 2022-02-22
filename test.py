# from tabulate import tabulate


class Figure:
    screen = [['🙩']*8 for _ in range(8)]

    def __init__(self, name, x, y, color):
        self.icon = "🙾"
        self.x = x
        self.y = y
        self.name = name
        self.color = color

    def __str__(self):
        return f"Объект класса {self.name}, координаты ({self.x}, {self.y})"

    def draw(self):
        print(f"Drawing {self.color} {self.name} at {self.x, self.y}")
        Figure.screen[self.y][self.x] = self.icon

    def move(self, x_new, y_new):
        Figure.screen[self.y][self.x] = "🙩"
        print(f"Moving {self.color} {self.name} from {self.x, self.y} to {x_new, y_new}")
        self.x, self.y = x_new, y_new
        self.draw()

    @classmethod
    def print_screen(cls):
        for _ in range(8):
            print("  ".join(cls.screen[_]))
        print()


class Pawn(Figure):
    def __init__(self, name, x, y, color):
        super().__init__(name, x, y, color)
        self.icon = "♙" if self.color == "White" else "♟"


# fig = Figure("Figure", 1, 1, "Black")
# fig.move(5, 5)
# Figure.print_screen()
p = Pawn("Pawn", 2, 3, "Black")
p.draw()
Figure.print_screen()
