import socket
import threading

def handle_client(client_socket, nickname):
    nicknames.append(nickname)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client(client_socket, nickname)
                break
            broadcast(message, nickname)
        except:
            remove_client(client_socket, nickname)
            break

def broadcast(message, sender):
    for client, nickname in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client, nickname)

def remove_client(client_socket, nickname):
    nicknames.remove(nickname)
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = '127.0.0.1' 
    server_port = 12345  
    server.bind((server_ip, server_port))
    server.listen(5)

    print("Server started listening on {}:{}".format(server_ip, server_port))

    while True:
        client_socket, client_address = server.accept()
        print("Connected from {}:{}".format(client_address[0], client_address[1]))

        client_socket.send("NICKNAME".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')

        client_thread = threading.Thread(target=handle_client, args=(client_socket, nickname))
        client_thread.start()
        clients.append((client_socket, nickname))

if __name__ == "__main__":
    nicknames = []
    clients = []
    main()