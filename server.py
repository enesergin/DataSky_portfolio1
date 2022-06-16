import argparse
import socket
import threading
import time

# parser that checks if the user has written the needed arguments, which in this case is the port number
parser = argparse.ArgumentParser(description='You can start a server and listen for incoming connections.'
                                             '\nExample of how: "python3 system.py 1234"')
parser.add_argument('port', type=int,
                    help='Argument 1: Port number you want the server running on. Write it in numbers only!')
args = parser.parse_args()
port = args.port

# creating a server socket, binding the ip address and the port given by user and listening for connections
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind(('localhost', port))
socketServer.listen()

# keeping track of clients and names
clients = []
clientsName = []


# broadcasting/sending message from host clients to the other clients
def broadcast(msg, client):
    for i in clients:
        # we don't want to send the message back to the original writer of the message
        if i is not client:
            i.send(msg)


# Handling of all the clients sending messages or disconnecting
def server_client_handling(client):
    while True:
        try:
            msg = client.recv(1024)
            split = msg.decode().split(": ")

            if split[1] == "KICKALL":  # this does not work as intended,
                # but removing it also causes other problems that I don't have the time to solve
                time.sleep(0.1)
                print("Disconnecting all the clients!")
                for i in clients:
                    i.close()

            else:
                time.sleep(0.5)
                broadcast(msg, client)
        except:
            # removing client and clientName from the lists
            index = clients.index(client)
            clients.remove(client)
            name = clientsName[index]
            clientsName.remove(name)
            client.close()
            broadcast(f'{name} has disconnected from the chat!'.encode('utf-8'),
                      client)  # broadcasting to all the other connected clients
            print(f'{name} has disconnected from the chat!')  # prints to server window
            break


# connects the clients to the server.
def client_connecting():
    print('Server is running! Currently listening to connections...\n')
    while True:
        client, address = socketServer.accept()  # accepting connection from the client
        client.send('not_connected'.encode('utf-8'))  # sending 'not_connected'
        # which is used for checking if a client is connected or not in client side
        name = client.recv(1024).decode('utf-8')  # receives name from the client
        clients.append(client)
        clientsName.append(name)
        print(f'{name} has connected to the chat!')  # prints to server window
        broadcast(f'{name} has connected to the chat!'.encode('utf-8'),
                  client)  # broadcasts to all currently connected clients
        client.send(
            'You have connected to the chat!\nYou can disconnect from the chat by closing the window.'.encode(
                'utf-8'))  # prints it to the original writer
        handling_thread = threading.Thread(target=server_client_handling, args=(client,))
        handling_thread.start()


client_connecting()
