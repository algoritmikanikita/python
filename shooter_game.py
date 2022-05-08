from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (255, 255, 255))
font2 = font.SysFont('Times New Roman', 36)
mixer.init()
#mixer.music.load("showdown.ogg")
#mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#картинки:
img_back = "showdown.jpg" #фон игры
img_hero = "Shelly.png" #герой
img_enemy = "elprima.png" #злодей
img_bullet = "bullet.png" #пуля
img_ast = "asteroid.png" #астероид

life = 3
goal = 10
score = 0
lost = 0
max_lost = 3

class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (77, 150))
        self.speed = player_speed
        
        # каждый спрайт должен хранить свойство rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Boss(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 50:
            self.direction = 'right'
        if self.rect.x >= width - 500:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    def fireboss(self):
        for i in range(1,3):
            attack = Enemy('boss.png',self.rect.centerx,self.rect.top,2,70,70)
            bossenemy.add(attack)
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 5,  10,  -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

win_width = 1000
win_height = 800
window = display.set_mode((win_width, win_height))# Создать игровую сцену размером 700x500
display.set_caption("Showdown")# Название игры
background = transform.scale(image.load(img_back),(win_width, win_height))# Фон

#персонажи
ship = Player(img_hero, 5, win_height  - 150, 80, 100, 15)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2,7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))

bullets = sprite.Group()

finish = False

run = True

rel_time = False

num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type  == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 5 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()
                    
                    if num_fire >= 5 and rel_time == False :
                        last_time = timer()
                        rel_time = True

    if not finish:
        window.blit(background,(0,0))

        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
    
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Reloading...', 1, (150, 0, 0))
                window.blit(reload, (0, 0))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters,  bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish  = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish =  True
            window.blit(win, (200,200))

        text = font2.render("Счёт: " + str(score), 1, True, (0, 0, 0))
        window.blit(text, (10,100))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (0, 0, 0))
        window.blit(text_lose, (10,130))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)
            
    time.delay(50)