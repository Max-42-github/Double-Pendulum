# intergarting pygame to the double pendulum code
import pygame
import numpy as np

pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont("Monaco", 12)

# Setting up the pygame window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Double Pendulum Simualtion ver 2.0")


BOB_MASS = 2

GREEN = (244,191,79)
BLACK = (0,0,0)


class Bob:

    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        

    def draw(self):
        bobSize = self.mass*10.0
        pygame.draw.circle(win, GREEN, (self.x, self.y), bobSize)



def main():

    bob = Bob(WIDTH // 2, HEIGHT // 2, BOB_MASS)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
        win.fill(BLACK)




        bob.draw()


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()