# pygame first code
import pygame
import math
import random

pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont("Monaco", 12)

# Setting up the pygame window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pygame sim v1.1")


## Some constant values for the simulation
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100
TRAIL_SIZE = 2

WHITE = (255,255,255)
GREEN = (244,191,79)
YELLOW = (255,255,0)
BLACK = (0,0,0)
CYAN = (0,255,255)

def random_color():
    color = ((random.randint(4,17) * 15), (random.randint(4,17) * 15), (random.randint(4,17) * 15))
    return color

class Planet:

    def __init__(self,x,y,mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        pygame.draw.circle(win, GREEN, (self.x, self.y), PLANET_SIZE)


class spacecraft:

    def __init__(self,x,y,vel_x,vel_y,mass,count):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.trail = []
        self.color = random_color()
        self.count = count

    def draw(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), OBJ_SIZE)

    def draw_trail(self):
        for i,pos in enumerate(self.trail):
            alpha = int(255 * (i/len(self.trail))) if len(self.trail) > 0 else 255
            trail_x, trail_y = pos
            trail_surface = pygame.Surface((TRAIL_SIZE*2,TRAIL_SIZE*2), pygame.SRCALPHA)
            r,g,b = self.color
            trail_color = (r,g,b,alpha)
            pygame.draw.circle(trail_surface, trail_color, (TRAIL_SIZE,TRAIL_SIZE), TRAIL_SIZE)

            win.blit(trail_surface, (int(pos[0]) - TRAIL_SIZE, int(pos[1]) - TRAIL_SIZE))

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

        self.trail.append((self.x, self.y))
        if len(self.trail) > 20:
            self.trail.pop(0)
    

def create_obj(position,mouse_position,count):
    t_x, t_y = position
    m_x, m_y = mouse_position
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS, count)
    return obj

def draw_text(window, text, position, color = (255,255,255)):
    label = FONT.render(text, True, color)
    win.blit(label, position)

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
                    count = len(objects) + 1
                    obj = create_obj(temp_obj_pos, mouse_pos, count)
                    objects.append(obj)
                    temp_obj_pos = None
                    
                else :
                    temp_obj_pos = mouse_pos
        
        mouse_pos = pygame.mouse.get_pos()

        
        win.fill(BLACK)

        if temp_obj_pos:

            # line magnitude
            t_x, t_y = temp_obj_pos
            mouse_x, mouse_y = mouse_pos

            line_mag = math.sqrt((mouse_x-t_x)**2+(mouse_y-t_y)**2)

            # To display the pointer coorinate
            draw_text(win,f"({mouse_x-t_x}, {(-1)*(mouse_y-t_y)})",(10, HEIGHT - 25))
            # line length
            draw_text(win,f"{round(line_mag,2)}",(t_x+((mouse_x-t_x)/2)+10,t_y+((mouse_y-t_y)/2)+10))

            pygame.draw.line(win, YELLOW, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, WHITE, temp_obj_pos, OBJ_SIZE)
        
        

        for obj in objects[:]:
            obj.draw_trail()
            obj.draw()
            obj.move(planet)

            if obj:
                vel_mag = math.sqrt(obj.vel_x**2 + obj.vel_y**2)
                draw_text(win, f"obj{obj.count} velocity = {round(vel_mag,2)}", (WIDTH - 160, (30 +(obj.count) * 20)), color = obj.color)

            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collison = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) < PLANET_SIZE

            if off_screen or collison:
                objects.remove(obj)


        
        planet.draw()

        # Display FPS count
        draw_text(win, f"FPS : {int(clock.get_fps())}", (WIDTH - 80, 10))

        # Simulation parameters : 
        draw_text(win, "SIMULATION PARAMETERS", (10, 10), (255,200,200))
        draw_text(win, f"Planet Mass : {PLANET_MASS}", (10, 25))
        draw_text(win, f"Object Mass : {SHIP_MASS}", (10, 40))
        draw_text(win, f"Planet Size : {PLANET_SIZE}", (10, 55))
        draw_text(win, f"Object Size : {OBJ_SIZE}", (10, 70))
        draw_text(win, f"Gravitational Constant G : {G}", (10, 85))
        
        

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()