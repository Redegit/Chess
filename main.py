import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 800))
r = pygame.Rect(50, 50, 100, 200)
pygame.draw.rect(screen, (0, 150, 150), r, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()








