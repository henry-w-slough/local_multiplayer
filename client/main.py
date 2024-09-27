import socket
import pygame
import client
import json

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
            "id": "",
            "x": self.rect.x,
            "y": self.rect.y
        }



sprites.add(Player(32, 32, (255, 255, 255)))



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.start_client(client_socket)

      
    

running = True
while running:
    client.send_message(json.dumps(sprites.sprites()[0].data), client_socket)

    print(client.newest_message)
    
    
    if client.newest_message != "":
        incoming_data = json.loads(client.newest_message)

        if incoming_data["id"] == sprites.sprites()[sprites.__len__()+1]:
            print("likjdfns")
            sprites.add(Player(32, 32, (255, 255, 255)))
        else:
            sprites.sprites()[incoming_data["id"]].rect.x = incoming_data["x"]
            sprites.sprites()[incoming_data["id"]].rect.y = incoming_data["y"]
                
            






    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        sprites.sprites()[0].rect.y -= 5
    if keys[pygame.K_s]:
        sprites.sprites()[0].rect.y += 5
    if keys[pygame.K_a]:
        sprites.sprites()[0].rect.x -= 5
    if keys[pygame.K_d]:
        sprites.sprites()[0].rect.x += 5
                


            
    
    
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
