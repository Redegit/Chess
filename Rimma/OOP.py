class Figure():
    screen = [['.'] * 20 for _ in range(20)]

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @classmethod
    def draw(Figure):
        for i in Figure.screen:
            print(' '.join(i))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Rectangle(Figure):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def change_fill(self):
        for i in range(self.y, self.y + self.height):
            for j in range(self.x, self.x + self.width):
                Figure.screen[i][j] = '*'

    def change(self):
        for i in range(self.y, self.y + self.height):
            Figure.screen[i][self.x] = '*'
            Figure.screen[i][self.x+self.width-1] = '*'
        for j in range(self.x, self.x + self.width):
            Figure.screen[self.y][j] = '*'
            Figure.screen[self.y + self.height-1][j] = '*'


class Square():  # унаследовать
    pass


a = Rectangle(2, 2, 5, 7)
a.change()
a.draw()

