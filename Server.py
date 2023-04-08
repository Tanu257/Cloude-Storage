import pickle
import socket
import threading
import os
import time

# Main Variables

storagePath = "YOUR STORAGE FOLDER PATH"
FileNameList = []
# Variables

host = socket.gethostname()
port = 12345

client_sockets_list = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initializing

server.bind((host, port))

server.listen(4)


# Functions
def receiveCommands(client_socket: socket.socket):
    while True:
        try:
            fetched_command = pickle.loads(client_socket.recv(5688962))

            if fetched_command[0] == "g":

                with open(storagePath + "/" + fetched_command[1], 'rb') as f:
                    data = f.read(408008)

                    while data:
                        client_socket.send(pickle.dumps(['1', data]))
                        data = f.read(408008)
                        time.sleep(0.09)

                    client_socket.send(pickle.dumps(['0']))

            elif fetched_command[0] == "r":
                refreshFilesLog()
                client_socket.send(pickle.dumps(FileNameList))
            elif fetched_command[0] == "u":

                with open(storagePath + "/" + fetched_command[1], 'wb') as f:
                    while True:
                        got = pickle.loads(client_socket.recv(4180080))

                        if got[0] == '0':
                            break
                        else:
                            f.write(got[1])
        except:
            break


def receiveConnections(server_socket: socket.socket, client_socket_list: list):
    while True:
        connected_socket, address = server_socket.accept()

        client_socket_list.append(connected_socket)

        connected_socket.send(pickle.dumps(FileNameList))

        threading.Thread(target=receiveCommands, args=(connected_socket,)).run()


def refreshFilesLog():
    global FileNameList
    FileNameList = os.listdir(storagePath)


# Pre Processes

refreshFilesLog()
# Main Threads
threading.Thread(target=receiveConnections, args=(server, client_sockets_list)).run()
