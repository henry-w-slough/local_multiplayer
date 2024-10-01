import socket
import pygame
import client
import json
import uuid

pygame.init()
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()

screen = pygame.display.set_mode((800, 800))
screenColor = (100, 100, 100)



class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.fill(color)

        self.data = {
            "id": str(uuid.uuid4()),
            "x": self.rect.x,
            "y": self.rect.y
        }



sprites.add(Player(32, 32, (255, 255, 255)))

player = sprites.sprites()[0]



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.start_client(client_socket)

all_messages = client.all_messages




running = True
while running:
    client.send_message(json.dumps(player.data), client_socket)

                
            






    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.rect.y -= 5
    if keys[pygame.K_s]:
        player.rect.y += 5
    if keys[pygame.K_a]:
        player.rect.x -= 5
    if keys[pygame.K_d]:
        player.rect.x += 5

    player.data["x"] = player.rect.x
    player.data["y"] = player.rect.y

                


            
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client_socket.send("exit".encode("utf-8"))
            client_socket.close()
            running = False



    sprites.update()

    screen.fill(screenColor)

    sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
