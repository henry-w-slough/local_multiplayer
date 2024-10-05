import socket
import pygame
import client
import json
import uuid

pygame.init()
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
all_clients = []

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


def last_element(list):
    if len(list) == 0:
        return 0
    else:
        return len(list)-1



sprites.add(Player(32, 32, (255, 255, 255)))

player = sprites.sprites()[0]



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.start_client(client_socket)

newest_message = client.newest_message




running = True
while running:
    #print(all_clients)
    client.send_message(json.dumps(player.data), client_socket)
 
    print(json.dumps(player.data))



    #if the outside client is already created
    if newest_message != "":
        print("Message")
        if json.loads(newest_message)["id"] != player.data["id"]:
            print("DATA: "+newest_message)
            if json.loads(newest_message)["id"] in all_clients:

                for sprite in sprites:
                    #iterating over every sprite till the id matches
                    if sprite.data["id"] == json.loads(newest_message)["id"]:
                        #changing position
                        sprite.rect.x = json.loads(newest_message)["x"]
                        sprite.rect.y = json.loads(newest_message)["y"]
            elif json.loads(newest_message)["id"] not in all_clients:
                print("new player")
                #making new player
                sprites.add(Player(32, 32, (255, 0, 0)))
                all_clients.append(sprites.sprites(sprites.__len__()).data["id"])

                
            






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



    #newest_message = ""

    sprites.update()

    screen.fill(screenColor)

    sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)
