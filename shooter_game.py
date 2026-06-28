#Create your own shooter

from pygame import *
from random import randint


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



font.init()
font2 = font.SysFont('Arial', 30)

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))








img_bullet = 'bullet.png'
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
max_lost=3
goal=10 

score = 0
lost = 0





class GameSprite(sprite.Sprite):
    def __init__(self,char_image, char_x, char_y, size_x, size_y, char_speed):
        sprite.Sprite.__init__(self,)
        self.image = transform.scale(image.load(char_image), (size_x, size_y))
        self.speed = char_speed
        self.rect = self.image.get_rect()
        self.rect.x = char_x
        self.rect.y = char_y
    def reset(self):
        window.blit(self.image,  (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:

            self.rect.x += self.speed
    



    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed


        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed



        if self.rect.y < 0:
            self.kill()     








win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
#creating a group of enemy sprites
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
bullets = sprite.Group()
#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#main game loop:
run = True #the flag is reset by the window close button
while run:
   #"Close" button press event
   for e in event.get():
       if e.type == QUIT:
           run = False
       #event of pressing the spacebar - the sprite shoots
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 #the game itself: actions of sprites, checking the rules of the game, redrawing
   if not finish:
       #update the background
       window.blit(background,(0,0))


       #launch sprite movements
       ship.update()
       monsters.update()
       bullets.update()


       #update them in a new location in each loop iteration
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       #check for a collision between a bullet and monsters (both monster and bullet disappear upon a touch)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           #this loop will repeat as many times as the number of monsters hit
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)


       #possible lose: missed too many monsters or the character collided with an enemy
       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
           finish = True #lose, set the background and no longer control the sprites.
           window.blit(lose, (200, 200))


       #win checking: how many points scored?
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))


       #write text on the screen
       text = font2.render("Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))


       display.update()
   #bonus: automatic restart of the game
   else:
       finish = False
       score = 0
       lost = 0
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()


       time.delay(3000)
       for i in range(1, 6):
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
      


   time.delay(50)
