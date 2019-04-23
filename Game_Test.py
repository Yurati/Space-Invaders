import pygame
import sys
import random
from pygame.locals import *


# kolor     R    G    B
WHITE 	= (255, 255, 255)
GREEN 	= (78, 255, 87)
BLUE 	= (80, 255, 239)
PURPLE 	= (203, 0, 255)
RED 	= (237, 28, 36)

# specjalna czcionka
FONT = "Font/space_invaders.ttf"


class Ship(pygame.sprite.Sprite):
    def __init__(self):  # konstruktor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Ship.png')  # załadowanie obrazka
        self.rect = self.image.get_rect(topleft=(340, 520))  # ustawianie współrzędnych i wykrywanie kolizji
        self.shipAlive = True  # statek nie został zniszczony
        self.shipDelay = 0

    def update(self):
        keys = pygame.key.get_pressed()  # sprawdza wciśnięte klawisze
        if keys[K_LEFT]:  # przesuwanie w lewo
            self.rect.x -= 3
            if self.rect.x <= 5:  # ograniczenie
                self.rect.x = 5
        if keys[K_RIGHT]:  # przesuwanie w prawo
            self.rect.x += 3
            if self.rect.x >= 720:  # ograniczenie
                self.rect.x = 720


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/laser.png')
        self.rect = self.image.get_rect()


class Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/shield.png')
        self.rect = self.image.get_rect()

    def create(self, quantity):
        shields = pygame.sprite.Group()
        for column in range(4):
            for n in range(quantity):
                shield = Shield()
                shield.rect.y = 500 - n * 5
                shield.rect.x = 50 + column * 200
                shields.add(shield)
        return shields


class Aliens(pygame.sprite.Sprite):
    def __init__(self):
        # parametry do kosmitów
        self.movement = 0  # licznik do wolniejszego poruszania
        self.directionRight = True
        self.directionLeft = False
        self.counter = 0  # licznik do lasera
        self.shooters = []  # lista do wybrania loswego strzelca
        self.points = 0  # punkty za zabijanie obcych
        self.velocity = None  # prędkość kosmitów
        self.delay = None
        self.multiply = None

    def update(self, aliens):
        self.movement += 1
        if self.movement == 3:  # wprowadzenie lekkiego opóźnienia - im więcej tym wolniej
            for alien in aliens:  # tyle ilu kosmitów jest
                alien.rect.x += self.velocity
                if alien.rect.x > 720 or alien.rect.x < 20:  # jeżeli dotrą do brzegu okna to linia w dół i zmiana kierunku
                    for alien_pos in aliens:
                        alien_pos.rect.y += 30  # przesunięcie w dół o linię
                    self.velocity *= -1  # zmiana kierunku
                    break
            self.movement = 0  # wyzerowanie licznka ruchu

    def shooterchoice(self, aliens, alienlaser, shipX):
        # funkcja sprawdza czy są jeszcze kosmici, jezeli ich nie ma to koniec gry
        for choice in aliens:  # zrobienie listy po to aby wybrać losowego strzelca
            self.shooters.append(choice)
        if len(self.shooters) == 0:
            return False
        else:
            shooter = self.shooters[random.randrange(len(self.shooters))]  # wybranie stzelca
            alienlaser.rect.x = shooter.rect.x + 20  # współrzędene początku lasera
            alienlaser.rect.y = shooter.rect.y + 40
            self.shooters.clear()  # wyczysczenie listy
            self.counter = 0  # odliczanie do strzału
            return True


class AlienWhite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemy1_2.png')
        self.rect = self.image.get_rect(topleft=(350, 50))
        self.score = 40

    def create(self):
        aliensWhite = pygame.sprite.Group()
        for column in range(10):
            alien = AlienWhite()
            alien.rect.x = 157 + (column * 50)
            aliensWhite.add(alien)
        return aliensWhite


class AlienAzure(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemy2_1.png')
        self.rect = self.image.get_rect(topleft=(350, 95))
        self.score = 30

    def create(self):
        aliensAzure = pygame.sprite.Group()
        for column in range(10):
            alien = AlienAzure()
            alien.rect.x = 157 + (column * 50)
            aliensAzure.add(alien)
        return aliensAzure


class AlienGreen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemy3_1.png')
        self.rect = self.image.get_rect(topleft=(350, 130))
        self.score = 20

    def create(self):
        aliensGreen = pygame.sprite.Group()
        for column in range(10):
            alien = AlienGreen()
            alien.rect.x = 157 + (column * 50)
            aliensGreen.add(alien)
        return aliensGreen


class AlienPurple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemy1_1.png')
        self.image = pygame.transform.scale(self.image, (40, 38))
        self.rect = self.image.get_rect(topleft=(350, 175))
        self.score = 10

    def create(self):
        aliensPurple = pygame.sprite.Group()
        for column in range(10):
            alien = AlienPurple()
            alien.rect.x = 157 + (column * 50)
            aliensPurple.add(alien)
        return aliensPurple


class AlienLaser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemylaser.png')
        self.rect = self.image.get_rect()


class Life(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('Images/Ship.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(750, 20))
        self.lives = 3


class Mystery(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images/mystery.png')
        self.image = pygame.transform.scale(self.image, (45, 30))
        self.rect = self.image.get_rect(topleft=(0, 50))
        self.score = random.randrange(1000)
        self.velocity = 2.5


# wyjście z gry
def end():
    pygame.quit()
    sys.exit()


def main():
    # inicjalizacja PyGame
    pygame.init()
    headFont = pygame.font.Font(FONT, 60)
    subFont = pygame.font.Font(FONT, 30)
    game_name = headFont.render('Space Invaders', False, WHITE)
    presskey = subFont.render('Press 1 for easy, 2 for medium 3 for hard!', False, WHITE)
    game_over = headFont.render('Game Over', False, WHITE)
    # utworzenie okna
    windowWidth = 800
    windowHeight = 600
    window = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)

    # nazwa gry na górnym pasku
    pygame.display.set_caption('Space Invaders')
    # załadowanie tła i grafik
    background = pygame.image.load('Images/Background.jpg')

    # instancje klas
    ship = Ship()
    laser = Laser()
    alienlaser = AlienLaser()
    mystery = Mystery()
    shield = Shield()

    enemies = Aliens()
    aliensWhite = AlienWhite()
    aliensPurple = AlienPurple()
    aliensAzure = AlienAzure()
    aliensGreen = AlienGreen()

    life = Life()

    # pobieramy informacje o ekranie - tle
    screen = pygame.display.get_surface()
    # przypisanie grafiki do określonego miejsca ekranu
    # blit - obiekt typu Surface, współrzędne
    screen.blit(background, (0, 0))

    # strzelanie laserem
    shipLaser = False
    enemyLaser = False
    protection = False  # ochrona po zestrzeleniu
    protectionCounter = 301

    # BONUS
    mysteryAlive = False
    bonusTime = 0  # licznik do bonusu
    bonus = pygame.sprite.Group()

    # tworzenie kosmitów
    aliens = pygame.sprite.Group()
    aliensWhiteGroup = aliensWhite.create()
    aliensAzureGroup = aliensAzure.create()
    aliensGreenGroup = aliensGreen.create()
    aliensPurpleGroup = aliensPurple.create()

    # dodanie do grupy wszystkich kosmitów
    aliens.add(aliensWhiteGroup)
    aliens.add(aliensAzureGroup)
    aliens.add(aliensGreenGroup)
    aliens.add(aliensPurpleGroup)

    # ustawienie tarczy - w zaleznosci od poziomu trudnosci
    shields = shield.create(5)

    # utworzenie grupy statku do wykrycia kolizji
    ship_group = pygame.sprite.Group(ship)

    # utworzenie grupy lasera do wykrycia kolizji laserów
    laser_group = pygame.sprite.Group(alienlaser)

    # dźwięki
    soundLaser = pygame.mixer.Sound('sounds/shoot.wav')
    soundAlienLaser = pygame.mixer.Sound('sounds/shoot2.wav')
    soundShipDestroyed = pygame.mixer.Sound('sounds/shipexplosion.wav')
    soundAlienDestroyed = pygame.mixer.Sound('sounds/invaderkilled.wav')
    soundMystery = pygame.mixer.Sound('sounds/mysteryentered.wav')
    soundMysteryKilled = pygame.mixer.Sound('sounds/mysterykilled.wav')
    effectsPlay = True  # żeby można było wyłączyć efekty dźwiękowe podczas gry

    # muzyka w tle
    musicPlay = True  # żeby można było wyłączyć dźwięk główny podczas gry
    pygame.mixer.music.load('sounds/spaceinvaders1.wav')
    pygame.mixer.music.play(-1, 0.0)

# ----------------------------------------------------------------------------------------

    # oczekiwanie na rozpoczęcie gry
    gameStart = False
    while gameStart is False:
        window.blit(game_name, (120, 100))  # wyświetlenie nazwy gry

        # wyświetlenie grafik i wartości punktowych poszczególnuch kosmitów
        alien = AlienWhite()
        window.blit(alien.image, (300, 200))
        value = subFont.render(' = 40 PTS', False, WHITE)
        window.blit(value, (350, 200))

        alien = AlienGreen()
        window.blit(alien.image, (300, 250))
        value = subFont.render(' = 30 PTS', False, GREEN)
        window.blit(value, (350, 250))

        alien = AlienAzure()
        window.blit(alien.image, (300, 300))
        value = subFont.render(' = 20 PTS', False, BLUE)
        window.blit(value, (350, 300))

        alien = AlienPurple()
        window.blit(alien.image, (300, 350))
        value = subFont.render(' = 10 PTS', False, PURPLE)
        window.blit(value, (350, 350))

        window.blit(mystery.image, (300, 400))
        value = subFont.render(' = ?? PTS', False, RED)
        window.blit(value, (350, 400))

        window.blit(presskey, (11, 450))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT - zamknięcie programu
                end()
            if event.type == KEYDOWN:
                if event.key == K_1:
                   enemies.velocity = 1
                   enemies.delay = 100
                   enemies.multiply = 1
                   gameStart = True
                elif event.key == K_2:
                    enemies.velocity = 2
                    enemies.delay = 50
                    enemies.multiply = 1.5
                    gameStart = True
                elif event.key == K_3:
                    enemies.velocity = 3
                    enemies.delay = 25
                    enemies.multiply = 2
                    gameStart = True

# -----------------------------------------------------------------------------------------

    # pętla główna gry
    while gameStart:
        for event in pygame.event.get():  # obsługa zdarzeń
            if event.type == QUIT:  # QUIT - zamknięcie programu
                end()
            if event.type == KEYDOWN:
                # strzelanie laserem
                if ship.shipAlive is True:
                    if shipLaser is False:  # dzięki temu można strzelić dopiero jak laser zniknie
                        if event.key == K_SPACE:  # strzał po naciśnięciu spacji
                            shipLaser = True
                            if effectsPlay is True:
                                soundLaser.play()
                            # początkowe miejsce lasera - wierzchołek statku
                            laser.rect.x = ship.rect.x + 34
                            laser.rect.y = ship.rect.y - 12
                if event.key == K_m:  # klawisz m włącza i wyłącza muzykę oraz efekty
                    if musicPlay is True:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlay = not musicPlay  # zmiana wartości na przeciwną
                    effectsPlay = not effectsPlay

        # ruch statku
        ship.update()

        # wyświetlanie statku i tła po resecie
        screen.blit(background, (0, 0))
        score = subFont.render('SCORE: %d' %enemies.points, False, WHITE)  # wyświetlnie punktów
        window.blit(score, (0, 0))

        # jeżeli nie był znisczony to wyświetl normalnie
        if protection is False:
            window.blit(ship.image, (ship.rect.x, ship.rect.y))
        else:
            ship.shipDelay += 1
            if ship.shipDelay > 30:
                window.blit(ship.image, (ship.rect.x, ship.rect.y))
            if ship.shipDelay == 60:
                ship.shipDelay = 0

        # wyświetlanie pozostałych żyć
        life.rect.x = 750
        for i in range(life.lives):  # po trafeinu zycie -1
            window.blit(life.image, (life.rect.x, life.rect.y))
            life.rect.x -= 40

        # wyświetlenie kosmitów
        aliens.draw(window)

        # tarcze
        shields.draw(window)

        # jeżeli został naciśnięty strzał
        if shipLaser is True:
            window.blit(laser.image, (laser.rect.x, laser.rect.y))  # laser
            # kolizje lasera z obcym
            hitEnemyWhite = pygame.sprite.spritecollide(laser, aliensWhiteGroup, True)
            hitEnemyAzure = pygame.sprite.spritecollide(laser, aliensAzureGroup, True)
            hitEnemyGreen = pygame.sprite.spritecollide(laser, aliensGreenGroup, True)
            hitEnemyPurple = pygame.sprite.spritecollide(laser, aliensPurpleGroup, True)

            # punkty za zabicie obcych
            if hitEnemyWhite:
                if effectsPlay is True:
                    soundAlienDestroyed.play()
                enemies.points += aliensWhite.score * enemies.multiply
            if hitEnemyAzure:
                if effectsPlay is True:
                    soundAlienDestroyed.play()
                enemies.points += aliensAzure.score * enemies.multiply
            if hitEnemyGreen:
                if effectsPlay is True:
                    soundAlienDestroyed.play()
                enemies.points += aliensGreen.score * enemies.multiply
            if hitEnemyPurple:
                if effectsPlay is True:
                    soundAlienDestroyed.play()
                enemies.points += aliensPurple.score * enemies.multiply

            # jeżeli tarcza zostanie trafiona to zniszcz
            self_shield_hit = pygame.sprite.spritecollide(laser, shields, True)

            laser.rect.y -= 7  # ruch lasera
            if laser.rect.y < 20 or hitEnemyWhite or hitEnemyAzure\
                    or hitEnemyGreen or hitEnemyPurple or self_shield_hit:  # zniknięcie pocisku
                laser.rect.y = ship.rect.y - 12
                shipLaser = False

        # przemieszczanie się kosmitów
        enemies.update(aliens)

        # jeżeli kosmici są odpowiednio nisko niech pojawi się bonus
        bonusTime += 1
        if bonusTime == 700:
            mystery = Mystery()
            if effectsPlay is True:
                soundMystery.play()
            mysteryAlive = True
            bonus.add(mystery)

        if mysteryAlive is True:
            bonus.draw(window)
            mystery.rect.x += mystery.velocity
            hitBonus = pygame.sprite.spritecollide(laser, bonus, True)
            if hitBonus:
                if effectsPlay is True:
                    soundMysteryKilled.play()
                shipLaser = False
                enemies.points += mystery.score * enemies.multiply
                mysteryAlive = False
                mystery.rect.x = 0
                bonusTime = 0

        # strzelanie obcych
        if enemyLaser is False:
            if enemies.counter < enemies.delay:  # żeby kosmici nie strzelali od razu po zniknięciu lasera
                enemies.counter += 1
                if enemies.counter == enemies.delay:
                    enemyLaser = True
                    if effectsPlay is True:
                        soundAlienLaser.play()
                    gameStart = enemies.shooterchoice(aliens, alienlaser, ship.rect.x)

        if enemyLaser is True:  # strzał
            window.blit(alienlaser.image, (alienlaser.rect.x, alienlaser.rect.y))  # laser obcych
            ship_hit = pygame.sprite.spritecollide(alienlaser, ship_group, True)
            enemy_shield_hit = pygame.sprite.spritecollide(alienlaser, shields, True)
            if ship_hit:  # statek dostał od kosmitów
                if effectsPlay is True:
                    soundShipDestroyed.play()
                life.lives -= 1  # odjęcie życia
                # ustawienie na początkowej pozycji
                ship.rect.x = 340
                ship.rect.y = 520
                protection = True
                protectionCounter = 0
                if life.lives == 0:
                    gameStart = False  # wyjście z pętli gry
            alienlaser.rect.y += 4
            if alienlaser.rect.y > 570 or ship_hit or enemy_shield_hit:  # zniknięcie pocisku
                enemyLaser = False

        # ochrona po zestrzeleniu
        if protection is True:
            protectionCounter += 1  # okres ochorny
            if protectionCounter == 200:
                ship_group.add(ship)  # ponowne dodanie do grupy
                protection = False

        # kolizja laserów i ich zniknięcie
        if pygame.sprite.spritecollide(laser, laser_group, False):
            shipLaser = False
            enemyLaser = False

        # kolizja statku i kosmitów - koniec gry
        if pygame.sprite.spritecollide(ship, aliens, False):
            gameStart = False

        pygame.display.update()  # odświeżenie obrazu

    # ekran końcowy
    while True:
        screen.blit(background, (0, 0))  # wyczyszczenie ekranu
        window.blit(game_over, (210, 270))
        window.blit(score, (310, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT - zamknięcie programu
                end()


if __name__ == '__main__':
    main()
