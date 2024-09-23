import socket
import threading

# List to keep track of connected clients
clients = []
lock = threading.Lock()



def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")

    #while handling a client (for every client)
    while True:
        try:
            #waiting for a recieved message
            message = client_socket.recv(1024).decode('utf-8')


            #getting exit message
            if message.lower() == "exit":

                print(f"[DISCONNECT] {address} disconnected.")
                with lock:
                    clients.remove(client_socket)
                client_socket.close()
                break

            else:
                broadcast(message, client_socket)
        except:
            print(f"[ERROR] An error occurred with {address}.")
            with lock:
                clients.remove(client_socket)
            client_socket.close()
            break



#fucntion to send message to all clients
def broadcast(message, client_socket):
    with lock:
        for client in clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    client.close()
                    clients.remove(client)




def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen()
    print("[SERVER STARTED] Listening for connections...")
    
    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()


start_server()


