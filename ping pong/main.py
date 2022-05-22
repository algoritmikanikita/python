from pygame import *
import random
'''Необходимые классы'''
 
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (wight, height)) #вместе 55,55 - параметры
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
   def update_r(self):
       keys = key.get_pressed()
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 155:
           self.rect.y += self.speed
   def update_l(self):
       keys = key.get_pressed()
       if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_s] and self.rect.y < win_height - 155:
           self.rect.y += self.speed
 
#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)
 
#флаги, отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

player1_score = 0
player2_score = 0

mixer.init()
kick_sound = mixer.Sound('kick.ogg')

#создания мяча и ракетки   
racket1 = Player('racket.png', 30, 200, 4, 50, 150) 
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

font.init()
font_regular = font.SysFont('Corbel', 35)
font_subtitles = font.SysFont('Corbel', 35, True)
lose1 = font_regular.render('PLAYER 2 WIN!', True, (255, 5, 16))
lose2 = font_regular.render('PLAYER 1 WIN!', True, (61, 255, 24))
score = font_regular.render(str(player1_score)+'           Очки            '+str(player2_score), True, (0,0,0))
restart = font_subtitles.render('R - перезапуск', True, (0, 0, 0))
 
speed_x = 3
speed_y = 3

def win_lose_yes_no():
    global player1_score, player2_score, score, finish,display
    window.fill(back)
    if ball.rect.x < 0:
        window.blit(lose1, (200, 200))
        player2_score+=1
    elif ball.rect.x > win_width-50:
        window.blit(lose2, (200, 200))
        player1_score+=1
    score = font_regular.render(str(player1_score)+'           Очки            '+str(player2_score), True, (0,0,0))
    window.blit(score, (180, 25))
    window.blit(restart, (180, 250))
    finish = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False   
        elif e.type == KEYDOWN:
            if e.key == K_q:
                game = False
            elif e.key == K_r and finish:
                speed_x = random.randint(-3,3)
                speed_y = random.randint(-3,3)
                racket1 = Player('racket.png', 30, 200, 4, 50, 150) 
                racket2 = Player('racket.png', 520, 200, 4, 50, 150)
                ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)
                finish = False
    if finish != True:
        window.fill(back)
        window.blit(score, (180, 25))
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
 
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            kick_sound.play()
            speed_x *= -1
            speed_y *= 1
      
       #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
        
       #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            win_lose_yes_no()
 
       #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width-50:
            win_lose_yes_no()
    
        score = font_regular.render(str(player1_score)+'           Очки            '+str(player2_score), True, (0,0,0))
        window.blit(score, (180, 25))
        

        racket1.reset()
        racket2.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)