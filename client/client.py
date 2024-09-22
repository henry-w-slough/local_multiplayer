import socket
import threading



def receive_messages(client_socket):
    #while the user is still inputting
    while True:
        #getting the input from server
        try:
            #recieving any input from other clients
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[MESSAGE] {message}")
            else:
                break
        #catching unexpected errors (error also given from exit)
        except:
            print("[ERROR] An error occurred while receiving messages.")
            break



def start_client(client_socket):
    client_socket.connect(('127.0.0.1', 12345))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    

def send_message(message, client_socket):
                
        #breaking connection from server
        if message.lower() == "exit":
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
        #if the message isn't exit, then send it to server
        else:
            client_socket.send(message.encode('utf-8'))


