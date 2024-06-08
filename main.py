import random
import pygame
import os



pygame.init()
os.environ['SDL_VIDEO_CENTERD'] = '1'
info = pygame.display.Info()
width = info.current_w
height = info.current_h
#screen
screen = pygame.display.set_mode((width,height-45),pygame.RESIZABLE)
#background define
bg = pygame.image.load('bg.png')
#backround
bg1 = pygame.image.load('GUIbg.jpg')
#edit eniemy
enemy_image = pygame.image.load('enimey.png')
scale_factor = 0.5
scaled_enemy_image = pygame.transform.scale(enemy_image, (int(enemy_image.get_width() * scale_factor), int(enemy_image.get_height() * scale_factor)))
rotated_enemy_image = pygame.transform.rotate(scaled_enemy_image, 180)
#edit ammo
ammo = pygame.image.load('ammo.png')
ammo_scaled_image = pygame.transform.scale(ammo, (int(enemy_image.get_width() * 0.1), int(enemy_image.get_height() * 0.1)))
#ammo for enemy
ammo_enemy = pygame.transform.rotate(ammo_scaled_image,90)
#ammo for hero
ammo_hero = pygame.transform.rotate(ammo_scaled_image,270)
#buttton for reset
button_img = pygame.image.load('reset.png')
#score
score = 0
#collide
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


#laser class
class Laser:
    def __init__(self,x,y,laser):
        self.x = x
        self.y = y
        self.img =  laser
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,win):
        win.blit(self.img,(self.x,self.y))

    def move(self,velocity):
        self.y += velocity
    def collision(self,obj):
        return collide(self,obj)
    def off_screen(self,height):
        return not(self.y <= height and self.y >=0 )
#absract class
class SHIP:
    COOLDOWN = 1
    def __init__(self,x,y):
        self.x = x
        self.image = None
        self.y = y
        self.cdc = 0
        self.blaster =[]

    def draw(self,window):
        window.blit(self.image,(self.x,self.y))
        for laser in self.blaster:
            laser.draw(window)


    def move_laser(self,velocity ,objs):
        for laser in self.blaster:
            laser.move(velocity)
            if laser.off_screen(height):
                self.blaster.remove(laser)
            elif laser.collision(objs):
                self.blaster.remove(laser)
    def cooldown(self):
        if self.cdc > 0:
            self.cdc += 1
            if self.cdc > self.COOLDOWN:  # Check if cooldown is over
                self.cdc = 0



#hero ship
class Hero(SHIP):
    def __init__(self ,x , y):
        super().__init__(x,y)
        self.x = x
        self.y = y
        self.image = pygame.image.load('bgbattleship.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.max_health = 100
        self.cdc = 0
        self.health = 100


    def move_laser(self,objs):
        global score
        for laser in self.blaster:
            laser.move(-25)
            if laser.off_screen(height):
                self.blaster.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        score += 1
                        print(score)

                        if laser in self.blaster:
                             self.blaster.remove(laser)

    def shoot(self):
        laser = Laser(self.x + 45, self.y, ammo_hero)
        self.blaster.append(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (width - 140, 80, self.image.get_width()+10, 20))
        pygame.draw.rect(window, (0, 255, 0), (
        width - 140,  80, (self.image.get_width()+10) * (self.health / self.max_health),
        20))

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()



        

#enemy class
class Enemy(SHIP):
    def __init__(self,x,y,):
        super().__init__(x,y)
        self.image = rotated_enemy_image
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.y += 5

    def shoot(self):
        laser = Laser( self.x + 145 , self.y + 130,ammo_enemy)
        self.blaster.append(laser)

def gameOver():
    global score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    score = 0
                    main()

        screen.blit(bg1, (0, 0))
        font = pygame.font.SysFont(None, 70)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        restart_text = font.render("Press 'N' to restart", True, (255, 255, 255))

        # Render text with border
        border_color = (0, 0, 0)  # Black border color
        border_thickness = 3
        border_game_over_text = font.render("Game Over", True, border_color)
        border_score_text = font.render("Score: " + str(score), True, border_color)
        border_restart_text = font.render("Press 'N' to restart", True, border_color)

        # Render the text itself over the border
        screen.blit(border_game_over_text, (width // 2 - border_game_over_text.get_width() // 2 - border_thickness, height // 2 - 50 - border_thickness))
        screen.blit(border_game_over_text, (width // 2 - border_game_over_text.get_width() // 2 + border_thickness, height // 2 - 50 - border_thickness))
        screen.blit(border_game_over_text, (width // 2 - border_game_over_text.get_width() // 2, height // 2 - 50 - border_thickness))
        screen.blit(border_game_over_text, (width // 2 - border_game_over_text.get_width() // 2, height // 2 - 50 + border_thickness))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))

        screen.blit(border_score_text, (width // 2 - border_score_text.get_width() // 2 - border_thickness, height // 2 - border_thickness))
        screen.blit(border_score_text, (width // 2 - border_score_text.get_width() // 2 + border_thickness, height // 2 - border_thickness))
        screen.blit(border_score_text, (width // 2 - border_score_text.get_width() // 2, height // 2 - border_thickness))
        screen.blit(border_score_text, (width // 2 - border_score_text.get_width() // 2, height // 2 + border_thickness))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))

        screen.blit(border_restart_text, (width // 2 - border_restart_text.get_width() // 2 - border_thickness, height // 2 + 50 - border_thickness))
        screen.blit(border_restart_text, (width // 2 - border_restart_text.get_width() // 2 + border_thickness, height // 2 + 50 - border_thickness))
        screen.blit(border_restart_text, (width // 2 - border_restart_text.get_width() // 2, height // 2 + 50 - border_thickness))
        screen.blit(border_restart_text, (width // 2 - border_restart_text.get_width() // 2, height // 2 + 50 + border_thickness))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))

        pygame.display.update()



def main():
    global score

   #other
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    #enemy
    enimes =list()




    #hero
    hero = Hero(710,580)
    def re_draw():

        screen.blit(bg,(0,0))
        hero.draw(screen)

        #score
        font = pygame.font.SysFont(None, 70)
        score_text = font.render('Score:' + str(score), True, (255, 255, 255))
        screen.blit(score_text, (width - score_text.get_width() - 10, 10))
        #enemy
        for enemy in enimes:
            enemy.draw(screen)
        pygame.display.update()

    while run:
        clock.tick(FPS)




        re_draw()
        if len(enimes) == 0:
            wave = random.randint(1, 5)
            for i in range(0,wave):
                enemy = Enemy(random.randint(100,1000),random.randint(-700,-100))
                enimes.append(enemy)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_LEFT] and hero.x > 0:
            hero.x -= 15
        if keys[pygame.K_RIGHT] and hero.x < width - hero.get_width() :
            hero.x += 15
        if keys[pygame.K_UP] and hero.y > 0:
            hero.y -= 7
        if keys[pygame.K_DOWN] and hero.y < height - hero.get_height() -70:
            hero.y += 7
        if keys[pygame.K_SPACE]:
            hero.shoot()
        for enemy in enimes:
            enemy.move()
            enemy.move_laser(10,hero)
            if random.randint(0,10) == 1:
                enemy.shoot()
            for laser in enemy.blaster:
                if laser.collision(hero):
                    hero.health -= 10

            if collide(enemy,hero):
                enimes.remove(enemy)
                hero.health -= 10

            elif enemy.y > height:
                enimes.remove(enemy)
        hero.move_laser(enimes)

        #game over
        if hero.health <= 0:
            gameOver()
            enimes.clear()
        pygame.display.update()
        clock.tick(60)

main()
