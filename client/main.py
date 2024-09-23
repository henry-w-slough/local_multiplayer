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
    def __init__(self, width, height, color, id):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.image.fill(color)

        self.data = {
            "id": id,
            "x": self.rect.x,
            "y": self.rect.y
        }


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



player = Player(32, 32, (255, 255, 255), "client_0")
sprites.add(player)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.start_client(client_socket)
client.send_message(str(player.data), client_socket)

all_messages = client.all_messages
all_clients = [0]


print(json.dumps(player.data))

#json.loads(json.dumps(player.data))
      
    

running = True
while running:
    
    

    for c in range(0, len(all_messages)):
        if c == (len(all_messages)-1):

            if all_messages == "osjnfsksdf":

                all_messages.remove(all_messages[c])
                sprites.add(Player(32, 32, (255, 0, 0)))


            
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client_socket.close()
            running = False



    sprites.update()

    screen.fill(screenColor)

    sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
