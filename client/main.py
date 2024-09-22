import pygame
from client import *

pygame.init()
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()


screen = pygame.display.set_mode((800, 800))
screenColor = (100, 100, 100)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.fill(color)

        self.pos = "0,0"


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5







player_one = Player(32, 32, (255, 255, 255))
sprites.add(player_one)



start_client(client_socket)

send_message("new_client", client_socket)


running = True  
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            send_message("exit", client_socket)
            running = False



    sprites.update()

    screen.fill(screenColor)

    sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)