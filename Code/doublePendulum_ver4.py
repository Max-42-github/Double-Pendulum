# intergarting pygame to the double pendulum code
import pygame
import numpy as np
from scipy.integrate  import odeint
import matplotlib.pyplot as plt



pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont("Monaco", 12)

# Setting up the pygame window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Double Pendulum Simualtion ver 2.0")

FPS = 60

butPosx = 700
butPosy = 50

butWidth = 60
butHeight = 40



lenButWidth = 25
lenButHeight = 25

len1Butx1 = 710
len1Buty1 = 470
len1Butx2 = 750
len1Buty2 = 470

len2Butx1 = 710
len2Buty1 = 500
len2Butx2 = 750
len2Buty2 = 500

mass1Butx1 = 710
mass1Buty1 = 530
mass1Butx2 = 750
mass1Buty2 = 530

mass2Butx1 = 710
mass2Buty1 = 560
mass2Butx2 = 750
mass2Buty2 = 560


strlen1 = 210#20 * (10)
strlen2 = 150#10 * (10)

MAX_LENGTH = 350
MIN_LENGTH = 10
MAX_MASS = 9
MIN_MASS = 0.3

BOB_MASS1 = 3
BOB_MASS2 = 2
STRING_WIDTH = 2

TRAIL_SIZE = 10

TOP_WIDTH = 5

RED = (244,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

GREEN = (0,244,0)
YELLOW = (244,244,0)

# Simulation parameter
g = 9.8

m1 = BOB_MASS1
m2 = BOB_MASS2
l1 = strlen1
l2 = strlen2


def settingInitialCond(strlen1, strlen2, BOB_MASS1, BOB_MASS2, theta1 = False, theta2 = False):
    # Setting the initial position of the bob
    # (200 pixel down from the fixed top)
    y1Down = strlen2*0.4
    y2Down = strlen2*0.9

    if theta1:
        theta1 = theta1
    else:
        theta1 = np.arcsin(y1Down/(strlen1))

    b1_posx = strlen1*(np.sin(theta1))
    b1_posy = strlen1*(np.cos(theta1))

    if theta2:
        theta2 = theta2
    else:
        theta2 = np.arcsin(y2Down/(strlen2))

    b2_posx = (strlen2*(np.sin(theta2)))
    b2_posy = (strlen2*(np.cos(theta2)))

    # Cordinate off set :
    X1_OFFSET = (WIDTH//2)
    Y1_OFFSET = (HEIGHT//2)-(HEIGHT//3)
    #X2_OFFSET = (WIDTH//2)+b2_posx
    #Y2_OFFSET = (HEIGHT//4)+b2_posy
    
    bob1 = Bob(X1_OFFSET+b1_posx, Y1_OFFSET+b1_posy, BOB_MASS1)
    bob2 = Bob(X1_OFFSET+b1_posx+b2_posx, Y1_OFFSET+b1_posy+b2_posy, BOB_MASS2)
    

    # Setting up the initial position array :
    X0 = [theta1, 0, theta2, 0]

    string1 = String(X1_OFFSET, Y1_OFFSET, X1_OFFSET+b1_posx, Y1_OFFSET+b1_posy, STRING_WIDTH)
    string2 = String(X1_OFFSET+b1_posx, Y1_OFFSET+b1_posy, X1_OFFSET+b1_posx+b2_posx, Y1_OFFSET+b1_posy+b2_posy, STRING_WIDTH)
    
    return [X0, bob1, bob2, string1, string2]


def doublePendulum(X,t):
	t1, omega1, t2, omega2 = X


	t1Dot = omega1
	t2Dot = omega2

	deno1 = ((m1+m2)*(l1)) - (m1*l1*(np.cos(t2-t1)**2))

	t1DDot = ((m2*l1*(t1Dot**2)*(np.sin(t2-t1))*(np.cos(t2-t1)))+(m2*g*(np.sin(t2))*(np.cos(t2-t1)))+(m2*l2*(t2Dot**2)*(np.sin(t2-t1)))-((m1+m2)*g*(np.sin(t1))))/(deno1)

	deno2 = ((m1+m2)*(l2)) - (m2*l2*(np.cos(t2-t1)**2))

	t2DDot = ((m2*l2*(t2Dot**2)*(np.sin(t2-t1))*(np.cos(t2-t1)))+((m1+m2)*((g*(np.sin(t1))*(np.cos(t2-t1)))-(l1*(t2Dot**2)*(np.sin(t2-t1)))-(g*(np.sin(t2))))))/(deno2)

	return [t1Dot, t1DDot, t2Dot, t2DDot]





class Bob:

    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.trail = []


    def draw(self):
        bobSize = self.mass*5.0
        pygame.draw.circle(win, GREEN, (self.x, self.y), bobSize)

    
    def draw_trail(self):
        for i,pos in enumerate(self.trail):
            print(len(self.trail))
            alpha = int(255 * (i/len(self.trail))) if len(self.trail) > 0 else 255
            trail_x, trail_y = pos
            trail_surface = pygame.Surface((TRAIL_SIZE*2,TRAIL_SIZE*2), pygame.SRCALPHA)
            r,g,b = self.color
            trail_color = (r,g,b,alpha)
            pygame.draw.circle(trail_surface, trail_color, (TRAIL_SIZE,TRAIL_SIZE), TRAIL_SIZE)

            win.blit(trail_surface, (int(pos[0]) - TRAIL_SIZE, int(pos[1]) - TRAIL_SIZE))

    def move(self, X0):
        #X0 = [self.x, 0, self.y, 0]

        deltaTime = 0.01
        X1_OFFSET = (WIDTH//2)
        Y1_OFFSET = (HEIGHT//2)-(HEIGHT//3)

        # Main bob movement
        endTime_eachframe = 0.15
        tArr = np.arange(0,endTime_eachframe,deltaTime)
        solution = odeint(doublePendulum,X0,tArr)
        #TotalTime += endTime_eachframe


        y1 = solution[:,0]
        y1dot = solution[:,1]
        y2 = solution[:,2]
        y2dot = solution[:,3]


        X0 = [y1[-1], y1dot[-1], y2[-1], y2dot[-1]]

        pos1x = (strlen1*(np.sin(y1[-1]))) + X1_OFFSET
        pos1y = (strlen1*(np.cos(y1[-1]))) + Y1_OFFSET

        pos2x = (strlen2*(np.sin(y2[-1]))) + (pos1x)
        pos2y = (strlen2*(np.cos(y2[-1]))) + (pos1y)

        self.trail.append((pos2x, pos2y))
        if len(self.trail) > 20:
            self.trail.pop(0)

        return [pos1x, pos1y, pos2x, pos2y, X0]




class String:

    def __init__(self, xi, yi, xf, yf, width):
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf
        self.width = width

    def draw(self):
        pygame.draw.line(win, WHITE, (self.xi, self.yi), (self.xf, self.yf), self.width)

class Button:

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        rect1 = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, self.color, rect1)
        
        return rect1
    
def draw_text(win, text, position, color = (255,255,255), size = 12):
    FONT = pygame.font.SysFont("Monaco", size)
    label = FONT.render(text, True, color)
    win.blit(label, position)


def main():

    clock = pygame.time.Clock()

    # Time increment
    deltaTime = 0.01
    TotalTime = 0
    endTime_eachframe = 0.15


    # Play and pause button
    pause = True
    play = False
    playButton = Button(butPosx, butPosy, butWidth, butHeight, RED)
    buttonRect = playButton.draw()

    # Initial condition button
    lengthPlus1 = Button(len1Butx1, len1Buty1, lenButWidth, lenButHeight, YELLOW)
    lengthMinus1 = Button(len1Butx2, len1Buty2, lenButWidth, lenButHeight, YELLOW)
    lengthPlus2 = Button(len2Butx1, len2Buty1, lenButWidth, lenButHeight, YELLOW)
    lengthMinus2 = Button(len2Butx2, len2Buty2, lenButWidth, lenButHeight, YELLOW)

    massPlus1 = Button(mass1Butx1, mass1Buty1, lenButWidth, lenButHeight, YELLOW)
    massMinus1 = Button(mass1Butx2, mass1Buty2, lenButWidth, lenButHeight, YELLOW)
    massPlus2 = Button(mass2Butx1, mass2Buty1, lenButWidth, lenButHeight, YELLOW)
    massMinus2 = Button(mass2Butx2, mass2Buty2, lenButWidth, lenButHeight, YELLOW)

    lenP1_Rect = lengthPlus1.draw()
    lenM1_Rect = lengthMinus1.draw()
    lenP2_Rect = lengthPlus2.draw()
    lenM2_Rect = lengthMinus2.draw()

    massP1_Rect = massPlus1.draw()
    massM1_Rect = massMinus1.draw()
    massP2_Rect = massPlus2.draw()
    massM2_Rect = massMinus2.draw()

    #initialization
    initialReturn = settingInitialCond(strlen1,strlen2,BOB_MASS1,BOB_MASS2)

    # Cordinate off set :
    X1_OFFSET = (WIDTH//2)
    Y1_OFFSET = (HEIGHT//2)-(HEIGHT//3)

    X0 = initialReturn[0]
    bob1 = initialReturn[1]
    bob2 = initialReturn[2]
    string1 = initialReturn[3]
    string2 = initialReturn[4]

    y1 = np.array([X0[0]])
    y1dot = np.array([0])
    y2 = np.array([X0[2]])
    y2dot = np.array([0])
    
    

    fixedTop = String((WIDTH//2)-(WIDTH//4),(HEIGHT//2)-(HEIGHT//3),(WIDTH//2)+(WIDTH//4),(HEIGHT//2)-(HEIGHT//3), TOP_WIDTH)

    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if buttonRect.collidepoint(pygame.mouse.get_pos()):
                    print('Clicked')

                    if playButton.draw():
                        if pause == True:
                            pause = False
                            play = True
                            playButton = Button(butPosx, butPosy, butWidth, butHeight, GREEN)
                        elif play == True:
                            play = False
                            pause = True
                            playButton = Button(butPosx, butPosy, butWidth, butHeight, RED)


                if pause:
                    temp_strlen1 = strlen1
                    temp_strlen2 = strlen2
                    temp_BOB_MASS1 = BOB_MASS1
                    temp_BOB_MASS2 = BOB_MASS2
                    
                    if lenP1_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('l1p')
                        main()
                        if temp_strlen1 >= MAX_LENGTH:
                            continue
                        else:
                            temp_strlen1 += 10
                            

                    if lenM1_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('l1m')
                        if temp_strlen1 <= MIN_LENGTH:
                            continue
                        else:
                            temp_strlen1 -= 10
                            

                    if lenP2_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('l2p')
                        if temp_strlen2 >= MAX_LENGTH:
                            continue
                        else:
                            temp_strlen2 += 10
                            

                    if lenM2_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('l2m')
                        if temp_strlen2 <= MIN_LENGTH:
                            continue
                        else:
                            temp_strlen2 -= 10
                            

                    if massP1_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('m1p')
                        if temp_BOB_MASS1 >= MAX_MASS:
                            continue
                        else:
                            temp_BOB_MASS1 += 0.3
                            

                    if massM1_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('m1m')
                        if temp_BOB_MASS1 <= MIN_MASS:
                            continue
                        else:
                            temp_BOB_MASS1 += 0.3
                        

                    if massP2_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('m2p')
                        if temp_BOB_MASS2 >= MAX_MASS:
                            continue
                        else:
                            temp_BOB_MASS2 += 0.3
                            

                    if massM2_Rect.collidepoint(pygame.mouse.get_pos()):
                        print('m2p')
                        if temp_BOB_MASS2 <= MIN_MASS:
                            continue
                        else:
                            temp_BOB_MASS2 += 0.3


                    initialReturn = settingInitialCond(temp_strlen1,temp_strlen2,temp_BOB_MASS1,temp_BOB_MASS2,y1[-1],y2[-1])

                    X0 = initialReturn[0]
                    bob1 = initialReturn[1]
                    bob2 = initialReturn[2]
                    string1 = initialReturn[3]
                    string2 = initialReturn[4]
        
        win.fill(BLACK)   

        if play:
            
            #moving the bob
            TotalTime += endTime_eachframe



            posOutput = bob2.move(X0)
            pos1x = posOutput[0]
            pos1y = posOutput[1]
            pos2x = posOutput[2]
            pos2y = posOutput[3]
            X0 = posOutput[4]
            

            bob1 = Bob(pos1x, pos1y, BOB_MASS1)
            bob2 = Bob(pos2x, pos2y, BOB_MASS2)
            string1 = String(WIDTH//2, (HEIGHT//2)-(HEIGHT//3), pos1x, pos1y, STRING_WIDTH)
            string2 = String(pos1x, pos1y,pos2x, pos2y, STRING_WIDTH)
    

            

            #print(f'BOB X : {pos1x} and BOB Y : {pos1y}')
            #print(f'\nBOB X : {pos2x} and BOB Y : {pos2y}')
        

        

        # Display FPS count
        draw_text(win, f"FPS : {int(clock.get_fps())}", (20, 20))

        draw_text(win, f"Time(t) : {round(TotalTime/10,1)} s", ((WIDTH//2)-5, 20))

        draw_text(win, 'Play/Pause', (butPosx-5, butPosy-20))
        
        draw_text(win, f"Length 1 : {strlen1} units", (20, HEIGHT-25-15-20-15))
        draw_text(win, f"Length 2 : {strlen2} units", (20, HEIGHT-25-15-20))
        draw_text(win, f"Mass 1 : {BOB_MASS1} units", (20, HEIGHT-25-15))
        draw_text(win, f"Mass 2 : {BOB_MASS2} units", (20, HEIGHT-25))
        

        playButton.draw()
        lengthPlus1.draw()
        lengthMinus1.draw()
        lengthPlus2.draw()
        lengthMinus2.draw()
        massPlus1.draw()
        massMinus1.draw()
        massPlus2.draw()
        massMinus2.draw()

        textBuffer = 75

        draw_text(win, "Length 1 : ", (len1Butx1-textBuffer,len1Buty1+3))
        draw_text(win, "Length 2 : ", (len2Butx1-textBuffer,len2Buty1+3))
        draw_text(win, "Mass 1 : ", (mass1Butx1-textBuffer,mass1Buty1+3))
        draw_text(win, "Mass 2 : ", (mass2Butx1-textBuffer,mass2Buty1+3))

        draw_text(win, '-', (len1Butx1+7,len1Buty1), BLACK, 16)
        draw_text(win, '+', (len1Butx2+7,len1Buty2), BLACK, 16)
        draw_text(win, '-', (len2Butx1+7,len2Buty1), BLACK, 16)
        draw_text(win, '+', (len2Butx2+7,len2Buty2), BLACK, 16)

        draw_text(win, '-', (mass1Butx1+7,mass1Buty1), BLACK, 16)
        draw_text(win, '+', (mass1Butx2+7,mass1Buty2), BLACK, 16)
        draw_text(win, '-', (mass2Butx1+7,mass2Buty1), BLACK, 16)
        draw_text(win, '+', (mass2Butx2+7,mass2Buty2), BLACK, 16)


        fixedTop.draw()
        string1.draw()
        string2.draw()

        bob1.draw()

        bob2.draw_trail()
        bob2.draw()
        


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()