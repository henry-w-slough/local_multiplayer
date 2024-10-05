import socket
import threading
import json


client_socks = []
all_clients = []
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

            if json.loads(message)["id"] in all_clients:    
                broadcast(message)
            else:
                all_clients.append(json.loads(message)["id"])



        except Exception as e:
            print(f"[ERROR] An error occurred with {address}: {e}")
            break
    
    # Cleanup after disconnect
    with lock:
        if client_socket in client_socks:
            client_socks.remove(client_socket)

    client_socket.close()




def broadcast(message):
    with lock:
        for client in client_socks:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:  
                print(f"[ERROR] Could not broadcast message to {client}: {e}")
                client.close()
                client_socks.remove(client)

def send_message(message, client_socket):
    with lock:
        try:
            client_socket.send(message)
        except Exception as e:
            print(f"[ERROR] Could not send message to {client_socket}: {e}")





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



if __name__ == "__main__":
    start_server()



