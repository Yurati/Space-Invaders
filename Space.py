import pygame
import sys
import time
from pygame.locals import *


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
ship = pygame.image.load('Images/Ship.png')
laser = pygame.image.load('Images/laser.png')
alien = pygame.image.load('Images/enemy1_2.png')
alien = pygame.transform.scale(alien, (40, 40))  # zmiana wymiarów
# pobieramy informacje o ekranie - tle
screen = pygame.display.get_surface()
# przypisanie grafiki do określonego miejsca ekranu
# blit - obiekt typu Surface, współrzędne
screen.blit(background, (0, 0))
pygame.display.flip()

# lista kolorow R G B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# czcionka do tekstów
basicFont = pygame.font.SysFont(None, 48)

# pozycja początkowa
shipPositionX = 350
shipPositionY = 520
start_alienPositionX = 50
start_alienPositionY = 100
alienPositionY = start_alienPositionY
movement = 0

window.blit(ship, (shipPositionX, shipPositionY))  # statek

# laser
shipLaser = False

pygame.display.update()  # musimy dokonać odświeżenia, aby coś się wyświetliło

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
                    # początkowe miejsce lasera
                    shipLaserX = shipPositionX + 34
                    shipLaserY = shipPositionY - 12

    keys = pygame.key.get_pressed()  # sprawdza wciśnięte klawisze
    if keys[K_LEFT]:  # przesuwanie w lewo
        shipPositionX -= 3
        if shipPositionX <= 5:  # ograniczenie
            shipPositionX = 5
    if keys[K_RIGHT]:  # przesuwanie w prawo
        shipPositionX += 3
        if shipPositionX >= 720:  # ograniczenie
            shipPositionX = 720

    # wyświetlanie obiektów
    screen.blit(background, (0, 0))
    window.blit(ship, (shipPositionX, shipPositionY))
    # rząd kosmitów
    for aliens in range(14):
        if alienPositionX > 40:
            alienPositionX = start_alienPositionX + 50*aliens + movement
        elif alienPositionX > 720:
            alienPositionY -= 10
            alienPositionX = start_alienPositionX + 50*aliens - movement
        window.blit(alien, (alienPositionX, alienPositionY))
    movement += 1
    # jeżeli został naciśnięty strzał
    if shipLaser is True:
        window.blit(laser, (shipLaserX, shipLaserY))
        shipLaserY -= 5
        if shipLaserY < 20:
            shipLaserY = shipPositionY - 12
            shipLaser = False

    pygame.display.update()  # odświeżenie obrazu
