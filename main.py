import pygame as pg
import time
import threading
import random

All_Bullets = []
All_asteroids = []
health = 100
class Asteriod:
    def __init__(self,x,y):
        self.asteroid=pg.image.load(r"C:\Users\ldogb\Desktop\spaceship_game\photos\asteroid.png")
        self.asteroid=pg.transform.scale(self.asteroid,(120,120))
        self.asteriod_rect= self.asteroid.get_rect()

        self.asteriod_rect.centerx=x
        self.asteriod_rect.y=y


    def move(self,speed):
        self.asteriod_rect.y += speed
        ran_num = random.randrange(1,3)
        if ran_num ==1:
            self.asteriod_rect.x += int(random.randrange(1,3))
        else:
            self.asteriod_rect.x -= int(random.randrange(1,3))

    def show(self,j):
        j.blit(self.asteroid,self.asteriod_rect)

All_asteroids.append(Asteriod(-80,-80))

class Bullet:
    def __init__(self,x,y):
        self.bullet = pg.image.load(r'C:\Users\ldogb\Desktop\spaceship_game\photos\bullet.png')
        self.bullet = pg.transform.scale(self.bullet,(20+20,30+30))
        self.bullet_rect = self.bullet.get_rect()

        self.bullet_rect.centerx = x  
        self.bullet_rect.top = y  

    def move(self,bullet_speed):
        self.bullet_rect.y -= bullet_speed

    def display(self,j):
        j.blit(self.bullet,self.bullet_rect)


def asteroids():
    global All_asteroids
    while 1:
        All_asteroids.append(Asteriod(random.randrange(1,1400),-20))
        time.sleep(random.randint(0,1))

t = threading.Thread(target=asteroids)
t.start()


score = 0

width, height = 1400, 900

pg.init()

# background = pg.image.load(r"C:\Users\ldogb\Desktop\spaceship_game\photos\background.png")
# background = pg.transform.scale(background,(1400,900))
display = pg.display.set_mode((width, height))
pg.display.set_caption('game game')


plane = pg.image.load(r'C:\Users\ldogb\Desktop\spaceship_game\photos\plane.png')

plane=pg.transform.scale(plane,(80,80))
plane_Start_x, plane_Start_y = round(width // 3) + 150, round(height // 1.25)-5

plane_rect = plane.get_rect(topleft=(plane_Start_x, plane_Start_y))

#have an asteroid always there going upwards so the bullets always render GENIUS//
clock = pg.time.Clock()
running = True


# def backgrounds(): #not sure of the issue for the background 
#     global background,display
#     display.blit(background,(0,0))
#     pg.display.update()
# t2=threading.Thread(target=backgrounds)
# t2.start()
# display.blit(background,(0,0)) 

while running:
    display.fill('purple')
    score_score = pg.font.Font(None, 50).render(f"Score: {score}", True, (255, 255, 255))
    display.blit(score_score,(10,10))

    health_health = pg.font.Font(None, 50).render(f"Health: {health}", True, (255, 20, 20))
    display.blit(health_health,(1400-200,10))

    # print(len(All_asteroids))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False        
        if event.type == pg.MOUSEBUTTONDOWN:
            # print('click')
            All_Bullets.append(Bullet(plane_rect.centerx,plane_rect.top))

    keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_w]:#up
        if plane_rect.y >0:
            plane_rect.y -= 5
    if keys_pressed[pg.K_s]:#down
        if plane_rect.bottom !=900:
            plane_rect.y += 5
    if keys_pressed[pg.K_a]:#left
        if plane_rect.x >0:
            plane_rect.x -= 5
    if keys_pressed[pg.K_d]:#right
        if plane_rect.right < 1400:
            plane_rect.x += 5

    # display.blit(background,(0,0)) 

    for k in All_asteroids[:]:
        if plane_rect.colliderect(k.asteriod_rect):
            running = False
        try:
            if k == All_asteroids[0]:
                k.move(-2)
            else:
                k.move(2)

            if k.asteriod_rect.top >900:
                All_asteroids.remove(k)
                health -= 5
                if health <=0:
                    running = False
            else:
                k.show(display)
# 2 speed down
            for i in All_Bullets[:]:#to create a list aswell so it auto updates and i do not modify something where there is nothing which would cause an index error. probs would cause problems otherwise
                if k.asteriod_rect.colliderect(i.bullet_rect):
                    score += 1
                    All_asteroids.remove(k)
                    All_Bullets.remove(i)
                if k == All_asteroids[0]:
                    i.move(5)
                if i.bullet_rect.bottom < 0:
                    All_Bullets.remove(i)
                else:
                    i.display(display)
        except ValueError:
            print('val error')


    display.blit(plane, plane_rect)
    
    pg.display.update()

    clock.tick(60)  

pg.quit()
quit()
