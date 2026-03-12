import socket
import threading

HOST = "127.0.0.1"
PORT = 4100

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print("Server started...")

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            broadcast(message)

            # Server auto reply
            if b"hi" in message.lower():
                broadcast(b"Server: hi")

        except:
            index = clients.index(client)
            username = usernames[index]

            clients.remove(client)
            usernames.remove(username)

            broadcast(f"{username} left the chat".encode())

            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with", address)

        client.send(b"USERNAME")
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print("Username:", username)

        broadcast(f"{username} joined chat".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive()