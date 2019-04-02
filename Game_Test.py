import pygame
import sys
import random
from pygame.locals import *


class Ship(pygame.sprite.Sprite):
    def __init__(self):  # konstruktor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/Ship.png')  # załadowanie obrazka
        self.rect = self.image.get_rect(topleft=(340, 520))  # ustawianie współrzędnych i wykrywanie kolizji


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/laser.png')
        self.rect = self.image.get_rect()


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemy1_2.png')
        self.rect = self.image.get_rect(topleft=(350, 50))


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/enemylaser.png')
        self.rect = self.image.get_rect()


def main():
    # inicjalizacja PyGame
    pygame.init()

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
    alienlaser = EnemyLaser()

    # pobieramy informacje o ekranie - tle
    screen = pygame.display.get_surface()
    # przypisanie grafiki do określonego miejsca ekranu
    # blit - obiekt typu Surface, współrzędne
    screen.blit(background, (0, 0))

    # czcionka do tekstów
    basicFont = pygame.font.SysFont(None, 48)

    # strzelanie laserem
    shipLaser = False
    enemyLaser = False

    # tworzenie kosmitów
    aliens = pygame.sprite.Group()
    for row in range(3):
        for column in range(10):
            alien = Alien()
            alien.rect.x = 157 + (column * 50)
            alien.rect.y = alien.rect.y + (row * 45)
            aliens.add(alien)

    # parametry do kosmitów
    movement = 0  # licznik do wolniejszego poruszania
    directionRight = True
    directionLeft = False
    counter = 0  # licznik do lasera
    shooters = []  # lista do wybrania loswego strzelca

    # utworzenie grupy statku do wykrycia kolizji
    ship_group = pygame.sprite.Group(ship)
    # pętla główna gry
    while True:
        for event in pygame.event.get():  # obsługa zdarzeń
            if event.type == QUIT:  # QUIT - zamknięcie programu
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # strzelanie laserem
                if shipLaser is False:  # dzięki temu można strzelić dopiero jak laser zniknie
                    if event.key == K_SPACE:
                        shipLaser = True
                        # początkowe miejsce lasera - wierzchołek statku
                        laser.rect.x = ship.rect.x + 34
                        laser.rect.y = ship.rect.y - 12

        keys = pygame.key.get_pressed()  # sprawdza wciśnięte klawisze
        if keys[K_LEFT]:  # przesuwanie w lewo
            ship.rect.x -= 3
            if ship.rect.x <= 5:  # ograniczenie
                ship.rect.x = 5
        if keys[K_RIGHT]:  # przesuwanie w prawo
            ship.rect.x += 3
            if ship.rect.x >= 720:  # ograniczenie
                ship.rect.x = 720

        # wyświetlanie statku i tła po resecie
        screen.blit(background, (0, 0))
        window.blit(ship.image, (ship.rect.x, ship.rect.y))

        # wyświetlenie kosmitów
        aliens.draw(window)

        # jeżeli został naciśnięty strzał
        if shipLaser is True:
            window.blit(laser.image, (laser.rect.x, laser.rect.y))  # laser
            hit = pygame.sprite.spritecollide(laser, aliens, True)  # wystąpienie kolizji i usunięcie obcego
            laser.rect.y -= 5
            if laser.rect.y < 20 or hit:  # zniknięcie pocisku
                laser.rect.y = ship.rect.y - 12
                shipLaser = False

        # przemieszczanie się kosmitów
        if directionRight is True:  # ruch w prawo
            movement += 1
            if movement == 2:
                for alien in aliens:  # tyle ilu kosmitów jest
                    alien.rect.x += 1
                    if alien.rect.x > 720:  # jeżeli dotrą do brzegu okna to linia w dół i zmiana kierunku
                        for alien_pos in aliens:
                            alien_pos.rect.y += 30
                        directionRight = False
                        directionLeft = True
                        break
                movement = 0
        elif directionLeft is True:  # ruch w lewo
            movement += 1
            if movement == 2:
                for alien in aliens:
                    alien.rect.x -= 1
                    if alien.rect.x < 20:
                        for alien_pos in aliens:
                            alien_pos.rect.y += 30
                        directionRight = True
                        directionLeft = False
                        break
                movement = 0

        # strzelanie obcych
        if enemyLaser is False:
            if counter < 30:
                counter += 1
                if counter == 30:
                    enemyLaser = True
                    n = 0
                    for choice in aliens:  # zrobienie listy po to aby wybrać losowego strzelca
                        shooters.append(choice)
                    shooter = shooters[random.randrange(len(shooters) - 1)]  # wybranie stzelca
                    alienlaser.rect.x = shooter.rect.x + 20
                    alienlaser.rect.y = shooter.rect.y + 40
                    shooters.clear()
                    counter = 0

        if enemyLaser is True:
            window.blit(alienlaser.image, (alienlaser.rect.x, alienlaser.rect.y))  # laser obcyh
            if pygame.sprite.spritecollide(alienlaser, ship_group, True):  # wystąpienie kolizji i usunięcie obcego
                 pygame.quit()
                 sys.exit()
            alienlaser.rect.y += 3
            if alienlaser.rect.y > 570:  # zniknięcie pocisku
                enemyLaser = False

        # kolizja statku i kosmitów
        if pygame.sprite.spritecollide(ship, aliens, False):
            pygame.quit()
            sys.exit()

        pygame.display.update()  # odświeżenie obrazu


if __name__ == '__main__':
    main()
