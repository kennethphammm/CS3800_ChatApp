import socket
import threading

SERVER_IP = 'localhost'
PORT = 12345
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_client(client, nickname):
    print(f"[NEW CONNECTION] {nickname} connected.")
    
    connected = True
    while connected:
        try:
            message = client.recv(1024)
            if message == DISCONNECT_MESSAGE.encode(FORMAT):
                connected = False
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode(FORMAT), client)
            nicknames.remove(nickname)
            break
    
    print(f"[DISCONNECTED] {nickname} disconnected.")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{PORT}")
    while True:
        if len(clients) < 10:
            client, addr = server.accept()
            client.send("NICK".encode(FORMAT))
            nickname = client.recv(1024).decode(FORMAT)
            nicknames.append(nickname)
            clients.append(client)
            
            print(f"[CONNECTION] {addr} connected as {nickname}")
            
            broadcast(f"{nickname} joined the chat!".encode(FORMAT), client)
            client.send('Connected to the server!'.encode(FORMAT))
            
            thread = threading.Thread(target=handle_client, args=(client,nickname,))
            thread.start()
            
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        else:
            print("[FULL] The server is full. Please try again later.")

if __name__ == "__main__":
    start()
