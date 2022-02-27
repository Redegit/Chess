import pygame as pg

import sys

from test import Figure
pg.font.init()

pg.display.set_caption("CHESS")
clock = pg.time.Clock()

background = pg.image.load('фон.jpg')

font = pg.font.Font('CASEFONT.TTF', 72)
text1 = font.render('p', True, (71, 51, 51))
sc = pg.display.set_mode((800, 700))
sc.blit(background,(0, 0))
image = pg.image.load('main.jpg')
image = pg.transform.scale(image, (606, 600))
sc.blit(image, (100, 50))
sc.blit(text1, (135, 550))
pg.display.update()

while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if 137 < pg.mouse.get_pos()[0] < 681 and 70 < pg.mouse.get_pos()[1] < 612:
                print(pg.mouse.get_pos()[0]//69-2, pg.mouse.get_pos()[1]//70-1)
            print(pg.mouse.get_pos())
    clock.tick(60)
