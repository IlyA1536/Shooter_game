
from pygame import *
from random import randint
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#подключение звуков выстрела
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font1 = font.SysFont("Arial", 60)
win_text = font1.render('YOU WIN!', True, (255, 255, 255))
win_text2 = font1.render('SPACE для перезапуска', True, (255, 255, 255))
lose_text = font1.render('Ты проиграл!', True, (180, 0, 0))
lose_text2 = font1.render('SPACE для перезапуска', True, (180, 0, 0))
font2 = font.SysFont("Arial", 20)

#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_bullet = 'bullet.png' # снаряд

score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
 
#группа для снарядов
bullets = sprite.Group()

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        keys = key.get_pressed()
        if keys[K_SPACE]:
            fire_sound.play()
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20 , -15)
            bullets.add(bullet)

#класс спрайта-врага  
class Enemy(GameSprite):
  	#движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
#скорость и удаление пули
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаём спрайты
ship = Player(img_hero, 300, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна      
end_game = False
game_win = False
game_lost = False

while run:
    #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire() 
    
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
 
        #пишем текст на экране (счётчик)
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50)) 
        
        #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
 
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        #условие поражения
        if lost == 3 or sprite.spritecollide(ship, monsters, False):
            game_lost = True
           
        if game_lost == True:
            window.blit(lose_text, (200, 200))
            window.blit(lose_text2, (10, 250))
            end_game = True
            mixer.music.stop()

        #условие победы
        if score == 10:
            game_win = True

        if game_win == True:
            window.blit(win_text, (200, 200))
            window.blit(win_text2, (10, 250))
            end_game = True
            mixer.music.stop()

        #убить врага пулей
        if sprite.groupcollide(monsters, bullets, True, True):    
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            score = score + 1

        if end_game == True:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    game_win = False
                    game_lost = False
                    end_game = False
                    score = 0
                    lost = 0
                    mixer.music.play()

        display.update()
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)