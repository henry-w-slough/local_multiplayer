import socket
import threading
import json

# List to keep track of connected clients
clients = []
client_socks = []
lock = threading.Lock()





def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    
    while True:
        try:
            # Waiting for a received message
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                # Handle empty messages (client disconnected)
                break
            
            # Checking for exit message
            if message.lower() == "exit":
                print(f"[DISCONNECT] {address} disconnected.")
                break
            
            #if a player is sending it's data info
            if json.loads(message)["id"]:
                player_data = json.loads(message)

                if player_data["id"] == "":
                    player_data["id"] = get_new_id()


            broadcast(message, client_socket)

                
                    
            
            

            

            
            broadcast(message, client_socket)

        except Exception as e:
            print(f"[ERROR] An error occurred with {address}: {e}")
            break
    
    # Cleanup after disconnect
    with lock:
        if client_socket in client_socks:
            client_socks.remove(client_socket)
    client_socket.close()




def broadcast(message, client_socket):
    with lock:
        for client in client_socks:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"[ERROR] Could not send message to {client}: {e}")
                    client.close()
                    client_socks.remove(client)




def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen()
    print("[SERVER STARTED] Listening for connections...")
    
    while True:
        client_socket, address = server.accept()
        with lock:
            client_socks.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()


def get_new_id():
    for socket in range(1, len(client_socks)):
        if socket == len(client_socks):
            return socket



if __name__ == "__main__":
    start_server()



