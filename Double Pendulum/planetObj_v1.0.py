# pygame first code
import pygame
import math

pygame.init()

# Setting up the pygame window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pygame sim v0.1")


## Some constant values for the simulation
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100

WHITE = (255,255,255)
GREEN = (0,100,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)


class Planet:

    def __init__(self,x,y,mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        pygame.draw.circle(win, GREEN, (self.x, self.y), PLANET_SIZE)


class spacecraft:

    def __init__(self,x,y,vel_x,vel_y,mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def draw(self):
        pygame.draw.circle(win, WHITE, (int(self.x), int(self.y)), OBJ_SIZE)

    def move(self, planet = None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = G * (self.mass * planet.mass) / (distance**2)
        acceleration = force / self.mass

        theta = math.atan2(planet.y - self.y, planet.x - self.x)

        acc_x = acceleration * math.cos(theta)
        acc_y = acceleration * math.sin(theta)

        self.vel_x += acc_x
        self.vel_y += acc_y

        self.x += self.vel_x
        self.y += self.vel_y
    

def create_obj(position,mouse_position):
    t_x, t_y = position
    m_x, m_y = mouse_position
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj


def main():
    clock = pygame.time.Clock()

    # Call the planet
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    # Temp location of the object
    temp_obj_pos = None

    running = True
    objects = []

    while running:
        clock.tick(FPS)

        # Check the mouse position in the window @ 60 ticks per sec
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_obj(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                    
                else :
                    temp_obj_pos = mouse_pos
        
        mouse_pos = pygame.mouse.get_pos()

        
        win.fill(BLACK)

        if temp_obj_pos:
            pygame.draw.line(win, YELLOW, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, WHITE, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)

            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collison = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) < PLANET_SIZE

            if off_screen or collison:
                objects.remove(obj)

        
        planet.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()